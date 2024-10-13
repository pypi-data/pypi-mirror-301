
/*
 * block2: Efficient MPO implementation of quantum chemistry DMRG
 * Copyright (C) 2020-2021 Huanchen Zhai <hczhai@caltech.edu>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 */

#pragma once

#include "../core/expr.hpp"
#include "../core/hamiltonian.hpp"
#include "../core/operator_tensor.hpp"
#include "../core/symbolic.hpp"
#include "../core/tensor_functions.hpp"
#include "mpo.hpp"
#include <cassert>
#include <memory>

using namespace std;

namespace block2 {

template <typename, typename, typename = void> struct NPC1MPOQC;

// "MPO" for charge/spin correlation (non-spin-adapted)
// NN[0~3] = n_{p,sp} x n_{q,sq}
// NN[4] = ad_{pa} a_{pb} x ad_{qb} a_{qa}
// NN[5] = ad_{pb} a_{pa} x ad_{qa} a_{qb}
template <typename S, typename FL>
struct NPC1MPOQC<S, FL, typename S::is_sz_t> : MPO<S, FL> {
    NPC1MPOQC(const shared_ptr<Hamiltonian<S, FL>> &hamil,
              const string &tag = "1NPC")
        : MPO<S, FL>(hamil->n_sites, tag) {
        const auto n_sites = MPO<S, FL>::n_sites;
        shared_ptr<OpExpr<S>> i_op = make_shared<OpElement<S, FL>>(
            OpNames::I, SiteIndex(), hamil->vacuum);
        shared_ptr<OpElement<S, FL>> zero_op = make_shared<OpElement<S, FL>>(
            OpNames::Zero, SiteIndex(), hamil->vacuum);
#ifdef _MSC_VER
        vector<vector<shared_ptr<OpExpr<S>>>> b_op(
            n_sites, vector<shared_ptr<OpExpr<S>>>(4));
        vector<vector<vector<shared_ptr<OpExpr<S>>>>> nn_op(
            n_sites, vector<vector<shared_ptr<OpExpr<S>>>>(
                         n_sites, vector<shared_ptr<OpExpr<S>>>(6)));
        vector<vector<vector<shared_ptr<OpExpr<S>>>>> pdm1_op(
            n_sites, vector<vector<shared_ptr<OpExpr<S>>>>(
                         n_sites, vector<shared_ptr<OpExpr<S>>>(6)));
#else
        shared_ptr<OpExpr<S>> b_op[n_sites][4];
        shared_ptr<OpExpr<S>> nn_op[n_sites][n_sites][6];
        shared_ptr<OpExpr<S>> pdm1_op[n_sites][n_sites][6];
#endif
        const int sz_minus[4] = {0, -2, 2, 0};
        for (uint16_t m = 0; m < n_sites; m++)
            for (uint8_t s = 0; s < 4; s++)
                b_op[m][s] = make_shared<OpElement<S, FL>>(
                    OpNames::B,
                    SiteIndex({m, m}, {(uint8_t)(s & 1), (uint8_t)(s >> 1)}),
                    S(0, sz_minus[s], 0));
        for (uint16_t i = 0; i < n_sites; i++)
            for (uint16_t j = 0; j < n_sites; j++) {
                for (uint8_t s = 0; s < 4; s++) {
                    SiteIndex sidx({i, j},
                                   {(uint8_t)(s & 1), (uint8_t)(s >> 1)});
                    nn_op[i][j][s] = make_shared<OpElement<S, FL>>(
                        OpNames::NN, sidx, hamil->vacuum);
                    pdm1_op[i][j][s] = make_shared<OpElement<S, FL>>(
                        OpNames::PDM1, sidx, hamil->vacuum);
                }
                for (uint8_t s = 0; s < 2; s++) {
                    SiteIndex sidx({i, j},
                                   {(uint8_t)s, (uint8_t)0, (uint8_t)1});
                    nn_op[i][j][4 + s] = make_shared<OpElement<S, FL>>(
                        OpNames::NN, sidx, hamil->vacuum);
                    pdm1_op[i][j][4 + s] = make_shared<OpElement<S, FL>>(
                        OpNames::PDM1, sidx, hamil->vacuum);
                }
            }
        MPO<S, FL>::hamil = hamil;
        MPO<S, FL>::const_e = (typename const_fl_type<FL>::FL)0.0;
        MPO<S, FL>::op = zero_op;
        MPO<S, FL>::left_vacuum = hamil->vacuum;
        MPO<S, FL>::schemer = nullptr;
        MPO<S, FL>::tf = make_shared<TensorFunctions<S, FL>>(hamil->opf);
        MPO<S, FL>::site_op_infos = hamil->site_op_infos;
        for (uint16_t m = 0; m < n_sites; m++) {
            int lshape = m != n_sites - 1 ? 1 + 10 * (m + 1) : 1;
            int rshape = m != n_sites - 1 ? 1 : 11;
            // left operator names
            shared_ptr<SymbolicRowVector<S>> plop =
                make_shared<SymbolicRowVector<S>>(lshape);
            (*plop)[0] = i_op;
            if (m != n_sites - 1)
                for (uint16_t j = 0; j <= m; j++) {
                    for (uint8_t s = 0; s < 4; s++)
                        (*plop)[1 + (m + 1) * s + j] = b_op[j][s];
                    for (uint8_t s = 0; s < 6; s++)
                        (*plop)[1 + (m + 1) * (4 + s) + j] = nn_op[j][m][s];
                }
            this->left_operator_names.push_back(plop);
            // right operator names
            shared_ptr<SymbolicColumnVector<S>> prop =
                make_shared<SymbolicColumnVector<S>>(rshape);
            (*prop)[0] = i_op;
            if (m == n_sites - 1) {
                for (uint8_t s = 0; s < 6; s++)
                    (*prop)[1 + s] = nn_op[m][m][s];
                for (uint8_t s = 0; s < 4; s++)
                    (*prop)[7 + s] = b_op[m][s];
            }
            this->right_operator_names.push_back(prop);
            // middle operators
            if (m != n_sites - 1) {
                int mshape = m != n_sites - 2 ? 6 * (2 * m + 1) : 24 * (m + 1);
                shared_ptr<SymbolicColumnVector<S>> pmop =
                    make_shared<SymbolicColumnVector<S>>(mshape);
                shared_ptr<SymbolicColumnVector<S>> pmexpr =
                    make_shared<SymbolicColumnVector<S>>(mshape);
                int p = 0;
                for (uint8_t s = 0; s < 6; s++) {
                    for (uint16_t j = 0; j <= m; j++) {
                        shared_ptr<OpExpr<S>> expr = nn_op[j][m][s] * i_op;
                        (*pmop)[p + 2 * j] = pdm1_op[j][m][s];
                        (*pmexpr)[p + 2 * j] = expr;
                        if (j != m) {
                            (*pmop)[p + 2 * j + 1] =
                                s < 4 ? pdm1_op[m][j][((s & 1) << 1) | (s >> 1)]
                                      : pdm1_op[m][j][s ^ 1];
                            (*pmexpr)[p + 2 * j + 1] = expr;
                        }
                    }
                    p += 2 * m + 1;
                }
                if (m == n_sites - 2) {
                    for (uint8_t s = 0; s < 4; s++) {
                        for (uint16_t j = 0; j <= m; j++) {
                            shared_ptr<OpExpr<S>> expr =
                                b_op[j][(s & 1) | ((s & 1) << 1)] *
                                b_op[m + 1][(s >> 1) | ((s >> 1) << 1)];
                            (*pmop)[p + 2 * j] = pdm1_op[j][m + 1][s];
                            (*pmop)[p + 2 * j + 1] =
                                pdm1_op[m + 1][j][((s & 1) << 1) | (s >> 1)];
                            (*pmexpr)[p + 2 * j] = (*pmexpr)[p + 2 * j + 1] =
                                expr;
                        }
                        (*pmop)[p + 2 * (m + 1)] = pdm1_op[m + 1][m + 1][s];
                        (*pmexpr)[p + 2 * (m + 1)] =
                            i_op * nn_op[m + 1][m + 1][s];
                        p += 2 * m + 3;
                    }
                    for (uint8_t s = 0; s < 2; s++) {
                        for (uint16_t j = 0; j <= m; j++) {
                            shared_ptr<OpExpr<S>> expr =
                                b_op[j][s | ((!s) << 1)] *
                                b_op[m + 1][(!s) | (s << 1)];
                            (*pmop)[p + 2 * j] = pdm1_op[j][m + 1][s + 4];
                            (*pmop)[p + 2 * j + 1] =
                                pdm1_op[m + 1][j][(s + 4) ^ 1];
                            (*pmexpr)[p + 2 * j] = (*pmexpr)[p + 2 * j + 1] =
                                expr;
                        }
                        (*pmop)[p + 2 * (m + 1)] = pdm1_op[m + 1][m + 1][s + 4];
                        (*pmexpr)[p + 2 * (m + 1)] =
                            i_op * nn_op[m + 1][m + 1][s + 4];
                        p += 2 * m + 3;
                    }
                    assert(p == mshape);
                }
                this->middle_operator_names.push_back(pmop);
                this->middle_operator_exprs.push_back(pmexpr);
                this->save_middle_operators(m);
                this->unload_middle_operators(m);
            }
            // site tensors
            shared_ptr<OperatorTensor<S, FL>> opt =
                make_shared<OperatorTensor<S, FL>>();
            int llshape = 1 + 10 * m;
            int lrshape = m != n_sites - 1 ? 1 + 10 * (m + 1) : 1;
            shared_ptr<Symbolic<S>> plmat = nullptr, prmat = nullptr;
            if (m == 0)
                plmat = make_shared<SymbolicRowVector<S>>(lrshape);
            else if (m == n_sites - 1)
                plmat = make_shared<SymbolicColumnVector<S>>(llshape);
            else
                plmat = make_shared<SymbolicMatrix<S>>(llshape, lrshape);
            (*plmat)[{0, 0}] = i_op;
            if (m != n_sites - 1) {
                int pi = 0, pb[4] = {1, 1 + m, 1 + m + m, 1 + m + m + m}, p = 1;
                for (uint8_t s = 0; s < 4; s++) {
                    for (uint16_t i = 0; i < m; i++)
                        (*plmat)[{pb[s] + i, p + i}] = i_op;
                    (*plmat)[{pi, p + m}] = b_op[m][s];
                    p += m + 1;
                }
                for (uint8_t s = 0; s < 4; s++) {
                    for (uint16_t i = 0; i < m; i++)
                        (*plmat)[{pb[(s & 1) | ((s & 1) << 1)] + i, p + i}] =
                            b_op[m][(s >> 1) | ((s >> 1) << 1)];
                    (*plmat)[{pi, p + m}] = nn_op[m][m][s];
                    p += m + 1;
                }
                for (uint8_t s = 0; s < 2; s++) {
                    for (uint16_t i = 0; i < m; i++)
                        (*plmat)[{pb[s | ((!s) << 1)] + i, p + i}] =
                            b_op[m][(!s) | (s << 1)];
                    (*plmat)[{pi, p + m}] = nn_op[m][m][s + 4];
                    p += m + 1;
                }
                assert(p == lrshape);
            }
            if (m == n_sites - 1) {
                prmat = make_shared<SymbolicColumnVector<S>>(11);
                prmat->data[0] = i_op;
                for (uint8_t s = 0; s < 6; s++)
                    prmat->data[1 + s] = nn_op[m][m][s];
                for (uint8_t s = 0; s < 4; s++)
                    prmat->data[7 + s] = b_op[m][s];
            } else {
                if (m == n_sites - 2)
                    prmat = make_shared<SymbolicMatrix<S>>(1, 11);
                else if (m == 0)
                    prmat = make_shared<SymbolicRowVector<S>>(1);
                else
                    prmat = make_shared<SymbolicMatrix<S>>(1, 1);
                (*prmat)[{0, 0}] = i_op;
            }
            opt->lmat = plmat, opt->rmat = prmat;
            hamil->filter_site_ops(m, {opt->lmat, opt->rmat}, opt->ops);
            this->tensors.push_back(opt);
            this->save_left_operators(m);
            this->save_right_operators(m);
            this->save_tensor(m);
            this->unload_left_operators(m);
            this->unload_right_operators(m);
            this->unload_tensor(m);
        }
    }
    void deallocate() override {}
    // here, since this is static, real qc_ncorr can use complex method
    // s == 0: n_{p,sp} x n_{q,sq} s == 1: ad_{pa} a_{pb} x ad_{qb}
    // a_{qa} / ad_{pb} a_{pa} x ad_{qa} a_{qb}
    static GMatrix<FL> get_matrix(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        GMatrix<FL> r(nullptr, n_orbs * 2, n_orbs * 2);
        r.allocate();
        r.clear();
        for (auto &v : expectations)
            for (auto &x : v) {
                shared_ptr<OpElement<S, FL>> op =
                    dynamic_pointer_cast<OpElement<S, FL>>(x.first);
                assert(op->name == OpNames::PDM1);
                if ((s == 0 && op->site_index.s(2) == 0) ||
                    (s == 1 && op->site_index.s(2) == 0 &&
                     op->site_index.s(0) == op->site_index.s(1)))
                    r(2 * op->site_index[0] + op->site_index.s(0),
                      2 * op->site_index[1] + op->site_index.s(1)) = x.second;
                else if (s == 1 && op->site_index.s(2) == 1)
                    r(2 * op->site_index[0] + op->site_index.s(0),
                      2 * op->site_index[1] + !op->site_index.s(0)) = x.second;
            }
        return r;
    }
    // s == 0: sum_(sp,sq) n_{p,sp} x n_{q,sq}
    // s == 1: sum_(sp,sq) ad_{psp} a_{psq} x ad_{qsq} a_{qsp}
    static GMatrix<FL> get_matrix_spatial(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        GMatrix<FL> r(nullptr, n_orbs, n_orbs);
        r.allocate();
        r.clear();
        GMatrix<FL> t = get_matrix(s, expectations, n_orbs);
        for (uint16_t i = 0; i < n_orbs; i++)
            for (uint16_t j = 0; j < n_orbs; j++)
                r(i, j) = t(2 * i + 0, 2 * j + 0) + t(2 * i + 1, 2 * j + 1) +
                          t(2 * i + 0, 2 * j + 1) + t(2 * i + 1, 2 * j + 0);
        t.deallocate();
        return r;
    }
};

// "MPO" for charge/spin correlation (spin-adapted)
// NN[0] = B0 x B0
// NN[1] = B1 x B1
// e_pqqp = 2 * XX[0] - delta_pq Epq
// e_pqpq = sqrt(3) * XX[1] - XX[0] + 2 * delta_pq Epq
// where Epq = 1pdm spatial
template <typename S, typename FL>
struct NPC1MPOQC<S, FL, typename S::is_su2_t> : MPO<S, FL> {
    NPC1MPOQC(const shared_ptr<Hamiltonian<S, FL>> &hamil,
              const string &tag = "1NPC")
        : MPO<S, FL>(hamil->n_sites, tag) {
        const auto n_sites = MPO<S, FL>::n_sites;
        shared_ptr<OpExpr<S>> i_op = make_shared<OpElement<S, FL>>(
            OpNames::I, SiteIndex(), hamil->vacuum);
        shared_ptr<OpElement<S, FL>> zero_op = make_shared<OpElement<S, FL>>(
            OpNames::Zero, SiteIndex(), hamil->vacuum);
#ifdef _MSC_VER
        vector<vector<shared_ptr<OpExpr<S>>>> b_op(
            n_sites, vector<shared_ptr<OpExpr<S>>>(2));
        vector<vector<vector<shared_ptr<OpExpr<S>>>>> nn_op(
            n_sites, vector<vector<shared_ptr<OpExpr<S>>>>(
                         n_sites, vector<shared_ptr<OpExpr<S>>>(2)));
        vector<vector<vector<shared_ptr<OpExpr<S>>>>> pdm1_op(
            n_sites, vector<vector<shared_ptr<OpExpr<S>>>>(
                         n_sites, vector<shared_ptr<OpExpr<S>>>(2)));
#else
        shared_ptr<OpExpr<S>> b_op[n_sites][2];
        shared_ptr<OpExpr<S>> nn_op[n_sites][n_sites][2];
        shared_ptr<OpExpr<S>> pdm1_op[n_sites][n_sites][2];
#endif
        for (uint16_t m = 0; m < n_sites; m++)
            for (uint8_t s = 0; s < 2; s++)
                b_op[m][s] = make_shared<OpElement<S, FL>>(
                    OpNames::B, SiteIndex(m, m, s), S(0, s * 2, 0));
        for (uint16_t i = 0; i < n_sites; i++)
            for (uint16_t j = 0; j < n_sites; j++)
                for (uint8_t s = 0; s < 2; s++) {
                    nn_op[i][j][s] = make_shared<OpElement<S, FL>>(
                        OpNames::NN, SiteIndex(i, j, s), hamil->vacuum);
                    pdm1_op[i][j][s] = make_shared<OpElement<S, FL>>(
                        OpNames::PDM1, SiteIndex(i, j, s), hamil->vacuum);
                }
        MPO<S, FL>::hamil = hamil;
        MPO<S, FL>::const_e = (typename const_fl_type<FL>::FL)0.0;
        MPO<S, FL>::op = zero_op;
        MPO<S, FL>::left_vacuum = hamil->vacuum;
        MPO<S, FL>::schemer = nullptr;
        MPO<S, FL>::tf = make_shared<TensorFunctions<S, FL>>(hamil->opf);
        MPO<S, FL>::site_op_infos = hamil->site_op_infos;
        for (uint16_t m = 0; m < n_sites; m++) {
            int lshape = m != n_sites - 1 ? 1 + 4 * (m + 1) : 1;
            int rshape = m != n_sites - 1 ? 1 : 5;
            // left operator names
            shared_ptr<SymbolicRowVector<S>> plop =
                make_shared<SymbolicRowVector<S>>(lshape);
            (*plop)[0] = i_op;
            if (m != n_sites - 1)
                for (uint16_t j = 0; j <= m; j++) {
                    for (uint8_t s = 0; s < 2; s++)
                        (*plop)[1 + (m + 1) * s + j] = b_op[j][s];
                    for (uint8_t s = 0; s < 2; s++)
                        (*plop)[1 + (m + 1) * (2 + s) + j] = nn_op[j][m][s];
                }
            this->left_operator_names.push_back(plop);
            // right operator names
            shared_ptr<SymbolicColumnVector<S>> prop =
                make_shared<SymbolicColumnVector<S>>(rshape);
            (*prop)[0] = i_op;
            if (m == n_sites - 1) {
                (*prop)[1] = nn_op[m][m][0];
                (*prop)[2] = nn_op[m][m][1];
                (*prop)[3] = b_op[m][0];
                (*prop)[4] = b_op[m][1];
            }
            this->right_operator_names.push_back(prop);
            // middle operators
            if (m != n_sites - 1) {
                int mshape = m != n_sites - 2 ? 2 * (2 * m + 1) : 8 * (m + 1);
                shared_ptr<SymbolicColumnVector<S>> pmop =
                    make_shared<SymbolicColumnVector<S>>(mshape);
                shared_ptr<SymbolicColumnVector<S>> pmexpr =
                    make_shared<SymbolicColumnVector<S>>(mshape);
                int p = 0;
                for (uint8_t s = 0; s < 2; s++) {
                    for (uint16_t j = 0; j <= m; j++) {
                        shared_ptr<OpExpr<S>> expr = nn_op[j][m][s] * i_op;
                        (*pmop)[p + 2 * j] = pdm1_op[m][j][s],
                                        (*pmexpr)[p + 2 * j] = expr;
                        if (j != m)
                            (*pmop)[p + 2 * j + 1] = pdm1_op[j][m][s],
                                                (*pmexpr)[p + 2 * j + 1] = expr;
                    }
                    p += 2 * m + 1;
                }
                if (m == n_sites - 2) {
                    for (uint8_t s = 0; s < 2; s++) {
                        for (uint16_t j = 0; j <= m; j++) {
                            shared_ptr<OpExpr<S>> expr =
                                b_op[j][s] * b_op[m + 1][s];
                            (*pmop)[p + 2 * j] = pdm1_op[j][m + 1][s];
                            (*pmop)[p + 2 * j + 1] = pdm1_op[m + 1][j][s];
                            (*pmexpr)[p + 2 * j] = (*pmexpr)[p + 2 * j + 1] =
                                expr;
                        }
                        p += 2 * (m + 1);
                        (*pmop)[p] = pdm1_op[m + 1][m + 1][s];
                        (*pmexpr)[p] = i_op * nn_op[m + 1][m + 1][s];
                        p++;
                    }
                }
                this->middle_operator_names.push_back(pmop);
                this->middle_operator_exprs.push_back(pmexpr);
                this->save_middle_operators(m);
                this->unload_middle_operators(m);
            }
            // site tensors
            shared_ptr<OperatorTensor<S, FL>> opt =
                make_shared<OperatorTensor<S, FL>>();
            int llshape = 1 + 4 * m;
            int lrshape = m != n_sites - 1 ? 1 + 4 * (m + 1) : 1;
            shared_ptr<Symbolic<S>> plmat = nullptr, prmat = nullptr;
            if (m == 0)
                plmat = make_shared<SymbolicRowVector<S>>(lrshape);
            else if (m == n_sites - 1)
                plmat = make_shared<SymbolicColumnVector<S>>(llshape);
            else
                plmat = make_shared<SymbolicMatrix<S>>(llshape, lrshape);
            (*plmat)[{0, 0}] = i_op;
            if (m != n_sites - 1) {
                int pi = 0, pb[2] = {1, 1 + m}, p = 1;
                for (uint8_t s = 0; s < 2; s++) {
                    for (uint16_t i = 0; i < m; i++)
                        (*plmat)[{pb[s] + i, p + i}] = i_op;
                    (*plmat)[{pi, p + m}] = b_op[m][s];
                    p += m + 1;
                }
                for (uint8_t s = 0; s < 2; s++) {
                    for (uint16_t i = 0; i < m; i++)
                        (*plmat)[{pb[s] + i, p + i}] = b_op[m][s];
                    (*plmat)[{pi, p + m}] = nn_op[m][m][s];
                    p += m + 1;
                }
                assert(p == lrshape);
            }
            if (m == n_sites - 1) {
                prmat = make_shared<SymbolicColumnVector<S>>(5);
                prmat->data[0] = i_op;
                prmat->data[1] = nn_op[m][m][0];
                prmat->data[2] = nn_op[m][m][1];
                prmat->data[3] = b_op[m][0];
                prmat->data[4] = b_op[m][1];
            } else {
                if (m == n_sites - 2)
                    prmat = make_shared<SymbolicMatrix<S>>(1, 5);
                else if (m == 0)
                    prmat = make_shared<SymbolicRowVector<S>>(1);
                else
                    prmat = make_shared<SymbolicMatrix<S>>(1, 1);
                (*prmat)[{0, 0}] = i_op;
            }
            opt->lmat = plmat, opt->rmat = prmat;
            hamil->filter_site_ops(m, {opt->lmat, opt->rmat}, opt->ops);
            this->tensors.push_back(opt);
            this->save_left_operators(m);
            this->save_right_operators(m);
            this->save_tensor(m);
            this->unload_left_operators(m);
            this->unload_right_operators(m);
            this->unload_tensor(m);
        }
    }
    void deallocate() override {}
    static shared_ptr<GTensor<FL>> get_matrix_reduced(
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        shared_ptr<GTensor<FL>> r =
            make_shared<GTensor<FL>>(vector<MKL_INT>{n_orbs, n_orbs, 2});
        r->clear();
        for (auto &v : expectations)
            for (auto &x : v) {
                shared_ptr<OpElement<S, FL>> op =
                    dynamic_pointer_cast<OpElement<S, FL>>(x.first);
                assert(op->name == OpNames::PDM1);
                (*r)({op->site_index[0], op->site_index[1],
                      op->site_index.ss()}) = x.second;
            }
        return r;
    }
    static GMatrix<FL> get_matrix(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        GMatrix<FL> r(nullptr, n_orbs * 2, n_orbs * 2);
        r.allocate();
        r.clear();
        assert(false); // not implemented
        return r;
    }
    // s == 0: sum_(sp,sq) n_{p,sp} x n_{q,sq}
    // s == 2: sum_(sp,sq) ad_{psp} a_{psq} x ad_{qsq} a_{qsp}
    static GMatrix<FL> get_matrix_spatial(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        GMatrix<FL> r(nullptr, n_orbs, n_orbs);
        r.allocate();
        r.clear();
        shared_ptr<GTensor<FL>> t = get_matrix_reduced(expectations, n_orbs);
        for (uint16_t i = 0; i < n_orbs; i++)
            for (uint16_t j = 0; j < n_orbs; j++) {
                if (s == 0)
                    r(i, j) = (FL)2.0 * (*t)({i, j, 0});
                else
                    r(i, j) = (*t)({i, j, 0}) - (FL)sqrt(3) * (*t)({i, j, 1});
            }
        return r;
    }
};

// "MPO" for charge/spin correlation (general spin)
template <typename S, typename FL>
struct NPC1MPOQC<S, FL, typename S::is_sg_t> : MPO<S, FL> {
    NPC1MPOQC(const shared_ptr<Hamiltonian<S, FL>> &hamil,
              const string &tag = "1NPC")
        : MPO<S, FL>(hamil->n_sites, tag) {
        throw runtime_error("Not implemented for general spin!");
    }
    void deallocate() override {}
    static GMatrix<FL> get_matrix(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        throw runtime_error("Not implemented for general spin!");
        GMatrix<FL> r(nullptr, n_orbs, n_orbs);
        return r;
    }
    static GMatrix<FL> get_matrix_spatial(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        throw runtime_error("Not implemented for general spin!");
        GMatrix<FL> r(nullptr, n_orbs / 2, n_orbs / 2);
        return r;
    }
};

// "MPO" for charge/spin correlation (arbitrary symmetry)
template <typename S, typename FL>
struct NPC1MPOQC<S, FL, typename S::is_sany_t> : MPO<S, FL> {
    NPC1MPOQC(const shared_ptr<Hamiltonian<S, FL>> &hamil,
              const string &tag = "1NPC")
        : MPO<S, FL>(hamil->n_sites, tag) {
        throw runtime_error("Not implemented for arbitrary symmetry!");
    }
    void deallocate() override {}
    static GMatrix<FL> get_matrix(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        throw runtime_error("Not implemented for arbitrary symmetry!");
        GMatrix<FL> r(nullptr, n_orbs, n_orbs);
        return r;
    }
    static GMatrix<FL> get_matrix_spatial(
        uint8_t s,
        const vector<vector<pair<shared_ptr<OpExpr<S>>, FL>>> &expectations,
        uint16_t n_orbs) {
        throw runtime_error("Not implemented for arbitrary symmetry!");
        GMatrix<FL> r(nullptr, n_orbs / 2, n_orbs / 2);
        return r;
    }
};

} // namespace block2
