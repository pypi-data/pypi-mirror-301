/*
 ___license_placeholder___
 */

#pragma once
////////////////////////////////////////////////////////////////////////////////

// Standard library & STL headers.
#include <math.h>
#include <vector>

// STEPS headers.
#include "rng/rng.hpp"

namespace steps::mpi::tetvesicle {

class Qtable {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Qtable(unsigned int size, double tau, const rng::RNGptr& r);

    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    void setup() noexcept;

    // Intended to be used if tablesize or tau changes during simulation
    void reinit(unsigned int size, double tau) noexcept;

    double getPhi() const noexcept;

    inline double getTau() const noexcept {
        return pTau;
    }


    ////////////////////////////////////////////////////////////////////////

  private:
    double Q(double theta) const noexcept;
    unsigned int pTablesize;
    double pTau;

    // The interpolation table
    std::vector<double> pX_interp;
    std::vector<double> pQ_values;

    // RNG stuff
    const rng::RNGptr rng;
};

}  // namespace steps::mpi::tetvesicle
