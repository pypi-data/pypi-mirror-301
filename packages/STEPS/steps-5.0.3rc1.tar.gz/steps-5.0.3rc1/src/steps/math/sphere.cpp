/*
 ___license_placeholder___
 */

#include <cassert>
#include <cmath>

// STEPS headers.
#include "math/point.hpp"
#include "math/sphere.hpp"

namespace steps::math {

position_rel_to_ves sphere_unit_randsurfpos(rng::RNGptr rng) {
    // Positions are relative to the centre of the sphere
    // Initial position is randomised
    double r1 = rng->getUnfII() * 2 - 1;
    double r2 = rng->getUnfII() * 2 - 1;

    // First part of the algorithm is to ensure the sum of the squares
    // are less than 1
    while ((r1 * r1) + (r2 * r2) >= 1.0) {
        r1 = rng->getUnfII() * 2 - 1;
        r2 = rng->getUnfII() * 2 - 1;
    }

    double x = 2 * r1 * std::sqrt(1 - (r1 * r1) - (r2 * r2));
    double y = 2 * r2 * std::sqrt(1 - (r1 * r1) - (r2 * r2));
    double z = 1 - 2 * ((r1 * r1) + (r2 * r2));

    position_rel_to_ves ran_loc{x, y, z};

    return ran_loc;
}

}  // namespace steps::math
