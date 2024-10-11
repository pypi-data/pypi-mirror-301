/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "rng.hpp"

namespace steps::rng {

/// Create a random number generator with name rng_name and return as RNG object.
///
/// \param rng_name Name of the random number generator.
/// \param buffsize Size of buffer.
RNGptr create(const std::string& rng_name, uint bufsize);

/// Create a MT19937 random number generator and return as RNG object.
///
/// \param buffsize Size of buffer.
RNGptr create_mt19937(uint bufsize);

}  // namespace steps::rng
