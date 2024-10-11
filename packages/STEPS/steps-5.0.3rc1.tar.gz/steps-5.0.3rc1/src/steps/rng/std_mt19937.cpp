/*
 ___license_placeholder___
 */

#include "rng/std_mt19937.hpp"
#include "util/error.hpp"

// logging

namespace steps::rng {

STDMT19937::STDMT19937(unsigned int bufsize)
    : RNG(bufsize) {}

STDMT19937::~STDMT19937() = default;

void STDMT19937::concreteInitialize(unsigned long seed) {
    rng_.seed(seed);
}

void STDMT19937::concreteFillBuffer() {
    for (unsigned int i = 0; i < rSize; ++i) {
        rBuffer.get()[i] = rng_();
    }
}

////////////////////////////////////////////////////////////////////////////////

void STDMT19937::checkpoint(std::ostream& cp_file) const {
    RNG::checkpoint(cp_file);
    CLOG(INFO, "general_log") << "Warning - std_mt19937 checkpointing is not implemented, runs "
                                 "might not be reproducible "
                              << std::endl;
    // TODO Implement checkpoint for std_mt19937
}

////////////////////////////////////////////////////////////////////////////////

void STDMT19937::restore(std::istream& cp_file) {
    RNG::restore(cp_file);
    // TODO Implement checkpoint for std_mt19937
}

}  // namespace steps::rng
