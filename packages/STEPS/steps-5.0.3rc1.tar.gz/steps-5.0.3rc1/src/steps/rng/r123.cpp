/*
 ___license_placeholder___
 */

// Standard library & STL headers.
#include <cassert>
#include <cstdint>
#include <sstream>
#include <string>

// STEPS headers.
#include "r123.hpp"
// util
#include "util/error.hpp"
// logging
////////////////////////////////////////////////////////////////////////////////

namespace steps::rng {

/// Increment the first 2 values of ctr, translated to 64-bit
void ctr_increment(R123::r123_type::ctr_type& ctr) {
    uint64_t x = ctr[0] + (static_cast<uint64_t>(ctr[1]) << 32);
    x++;
    ctr[0] = x;
    ctr[1] = x >> 32;
}

////////////////////////////////////////////////////////////////////////////////
void R123::concreteInitialize(unsigned long seed) {
    key.fill(0);
    ctr[0] = 0;           /// Incrementing the counter
    ctr[1] = 0;           /// Incrementing the counter
    ctr[2] = seed;        /// First 32 bits of 64-bit seed
    ctr[3] = seed >> 32;  /// Last 32 bits of the seed
}

////////////////////////////////////////////////////////////////////////////////

/// Fills the buffer with random numbers on [0,0xffffffff]-interval.
void R123::concreteFillBuffer() {
    uint* b;
    for (b = rBuffer.get(); b + 4 <= rEnd; b += 4) {
        /// Getting 4 new random numbers
        r123_type::ctr_type rn = r(ctr, key);
        ctr_increment(ctr);
        b[0] = rn[0];
        b[1] = rn[1];
        b[2] = rn[2];
        b[3] = rn[3];
    }

    if (b == rEnd) {
        return;
    }

    AssertLog(b + 4 > rEnd);
    r123_type::ctr_type rn = r(ctr, key);
    ctr_increment(ctr);
    for (int i = 0; b < rEnd; ++b, ++i) {
        *b = rn[i];
    }
}

////////////////////////////////////////////////////////////////////////////////

void R123::checkpoint(std::ostream& cp_file) const {
    RNG::checkpoint(cp_file);
    CLOG(INFO, "general_log")
        << "Warning - r123 checkpointing is not implemented, runs might not be reproducible "
        << std::endl;
    // TODO Implement checkpoint for r123
}

////////////////////////////////////////////////////////////////////////////////

void R123::restore(std::istream& cp_file) {
    RNG::restore(cp_file);
    // TODO Implement checkpoint for r123
}

}  // namespace steps::rng
