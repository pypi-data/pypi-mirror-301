/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "math/point.hpp"
#include "rng/rng.hpp"

namespace steps::math {

/** Generate random position on unit sphere tetrahedron barycentre.
 *
 * \param r1, r1 Uniform random numbers on -1, 1.
 * \return random point on surface.
 */
position_rel_to_ves sphere_unit_randsurfpos(rng::RNGptr rng);

}  // namespace steps::math
