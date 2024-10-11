/*
 ___license_placeholder___
 */

#include "mt19937.hpp"

#include "util/checkpointing.hpp"

namespace steps::rng {

void MT19937::concreteInitialize(ulong seed) {
    pState[0] = seed & 0xffffffffUL;
    for (pStateInit = 1; pStateInit < MT_N; pStateInit++) {
        pState[pStateInit] =
            (1812433253UL * (pState[pStateInit - 1] ^ (pState[pStateInit - 1] >> 30)) + pStateInit);
        // See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier.
        // In the previous versions, MSBs of the seed affect
        // only MSBs of the array pState[].
        // 2002/01/09 modified by Makoto Matsumoto
        pState[pStateInit] &= 0xffffffffUL;
        // for >32 bit machines
    }
}

////////////////////////////////////////////////////////////////////////////////

/// Fills the buffer with random numbers on [0,0xffffffff]-interval.
void MT19937::concreteFillBuffer() {
    ulong y;
    static ulong mag01[2] = {0x0UL, MT_MATRIX_A};
    // mag01[x] = x * MATRIX_A  for x=0,1

    for (uint* b = rBuffer.get(); b < rEnd; ++b) {
        if (pStateInit >= MT_N) {
            // Generate N words at one time
            int kk;

            // If init_genrand() has not been called, a default
            // initial seed is used.
            if (pStateInit == MT_N + 1) {
                initialize(5489UL);
            }

            for (kk = 0; kk < MT_N - MT_M; ++kk) {
                y = (pState[kk] & MT_UPPER_MASK) | (pState[kk + 1] & MT_LOWER_MASK);
                pState[kk] = pState[kk + MT_M] ^ (y >> 1) ^ mag01[y & 0x1UL];
            }
            for (; kk < MT_N - 1; ++kk) {
                y = (pState[kk] & MT_UPPER_MASK) | (pState[kk + 1] & MT_LOWER_MASK);
                pState[kk] = pState[kk + (MT_M - MT_N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
            }
            y = (pState[MT_N - 1] & MT_UPPER_MASK) | (pState[0] & MT_LOWER_MASK);
            pState[MT_N - 1] = pState[MT_M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

            pStateInit = 0;
        }

        y = pState[pStateInit++];

        // Tempering.
        y ^= (y >> 11);
        y ^= (y << 7) & 0x9d2c5680UL;
        y ^= (y << 15) & 0xefc60000UL;
        y ^= (y >> 18);

        *b = static_cast<uint>(y);
    }
}

////////////////////////////////////////////////////////////////////////////////

MT19937::MT19937(uint bufsize)
    : RNG(bufsize) {}

////////////////////////////////////////////////////////////////////////////////

MT19937::~MT19937() = default;

////////////////////////////////////////////////////////////////////////////////

void MT19937::checkpoint(std::ostream& cp_file) const {
    RNG::checkpoint(cp_file);
    util::checkpoint(cp_file, pState, MT_N);
    util::checkpoint(cp_file, pStateInit);
}

////////////////////////////////////////////////////////////////////////////////

void MT19937::restore(std::istream& cp_file) {
    RNG::restore(cp_file);
    util::restore(cp_file, pState, MT_N);
    util::restore(cp_file, pStateInit);
}

}  // namespace steps::rng
