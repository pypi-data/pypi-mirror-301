/*
 ___license_placeholder___
 */

#include "bdsystem_lapack.hpp"

#include <algorithm>

namespace steps::solver::efield {

extern "C" {
extern void dgbsv_(int* n,
                   int* kl,
                   int* ku,
                   int* nrhs,
                   double* ab,
                   int* ldab,
                   int* ipiv,
                   double* b,
                   int* ldb,
                   int* info);
}

void BDSystemLapack::solve() {
    auto n = static_cast<int>(pN);
    auto h = static_cast<int>(pHalfBW);
    int nrhs = 1;
    int ldab = 3 * h + 1;
    int info = 0;

    std::copy(pb.begin(), pb.end(), px.begin());
    dgbsv_(&n, &h, &h, &nrhs, pA.data(), &ldab, &pwork[0], &px[0], &n, &info);
}

}  // namespace steps::solver::efield
