/*
 ___license_placeholder___
 */

#include "linsolve.hpp"

#include <cmath>

namespace steps::math {

int linsolve(int n, int rhs_num, double a[]) {
    // SOURCE: I forgot. Probably Numerical Recipes.

    // Precompute n+ rhs_num
    int n_plus_rhs_num = n + rhs_num;

    // Loop over all rows.
    for (int j = 0; j < n; ++j) {
        // Choose a pivot row: first we select j.
        int ipivot = j;
        double apivot = a[j + j * n];
        // But we really want the largest.
        for (int i = j + 1; i < n; ++i) {
            if (std::abs(apivot) < std::abs(a[i + j * n])) {
                apivot = a[i + j * n];
                ipivot = i;
            }
        }

        // Singular system: report!
        if (apivot == 0.0) {
            return j;
        }

        // Swap.
        for (int i = 0; i < n_plus_rhs_num; ++i) {
            double temp = a[ipivot + i * n];
            a[ipivot + i * n] = a[j + i * n];
            a[j + i * n] = temp;
        }

        // a[j,j] becomes 1.
        // a[j + j * n] = 1.0;
        for (int k = j; k < n_plus_rhs_num; ++k) {
            a[j + k * n] = a[j + k * n] / apivot;
        }

        // a[i,j] becomes 0.
        for (int i = 0; i < n; ++i) {
            if (i != j) {
                double factor = a[i + j * n];
                // a[i + j * n] = 0.0;
                for (int k = j; k < n_plus_rhs_num; ++k) {
                    a[i + k * n] = a[i + k * n] - factor * a[j + k * n];
                }
            }
        }
    }

    return 0;
}

}  // namespace steps::math
