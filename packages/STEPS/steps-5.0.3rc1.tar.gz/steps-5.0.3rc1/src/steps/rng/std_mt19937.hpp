/*
 ___license_placeholder___
 */

#pragma once

#include <random>

#include "rng/rng.hpp"

namespace steps::rng {

class STDMT19937: public RNG {
  public:
    STDMT19937(unsigned int bufsize);
    ~STDMT19937() override;

    void checkpoint(std::ostream& cp_file) const override;

    void restore(std::istream& cp_file) override;

  protected:
    void concreteInitialize(unsigned long seed) override;

    void concreteFillBuffer() override;

    std::mt19937 rng_;
};

}  // namespace steps::rng
