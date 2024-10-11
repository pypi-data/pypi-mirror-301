/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <fstream>
#include <string>

// STEPS headers.
#include "fwd.hpp"
#include "model/complex.hpp"
#include "util/common.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::dist {

/// Defined Complex
class Complexdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the complex.
    /// \param d Reference to the associated Complex object.
    Complexdef(const Statedef& sd, model::complex_id idx, const steps::model::Complex& d);

    /// Destructor
    ~Complexdef();

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: COMPLEX
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this complex.
    inline model::complex_id idx() const noexcept {
        return pIdx;
    }

    inline uint nbSubStates() const noexcept {
        return pNbSubStates;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    model::complex_id pIdx;
    uint pNbSubStates;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::dist
