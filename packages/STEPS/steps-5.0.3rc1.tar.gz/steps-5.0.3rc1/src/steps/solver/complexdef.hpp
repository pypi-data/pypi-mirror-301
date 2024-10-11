/*
 ___license_placeholder___
 */

#pragma once

#include "model/complex.hpp"
#include "statedef.hpp"
#include "util/common.hpp"

namespace steps::solver {

/// Defined Complex
class Complexdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the complex.
    /// \param d Pointer to the associated Complex object.
    Complexdef(complex_global_id idx, steps::model::Complex& d);

    /// Destructor
    ~Complexdef();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: COMPLEX
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this complex.
    complex_global_id gidx() const noexcept {
        return pIdx;
    }

    uint nbSubStates() const noexcept {
        return pNbSubStates;
    }

    /// Return the name of the complex.
    const std::string& name() const {
        return pName;
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////
    /// Setup the object.
    ///
    /// This method is included for consistency with other def objects,
    /// but currently does nothing.
    void setup();

  private:
    const complex_global_id pIdx;
    const uint pNbSubStates;
    const std::string pName;
    bool pSetupdone{false};
};

}  // namespace steps::solver
