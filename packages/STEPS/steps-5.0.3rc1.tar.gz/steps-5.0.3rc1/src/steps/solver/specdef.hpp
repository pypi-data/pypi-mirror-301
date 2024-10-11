/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>

#include "fwd.hpp"
#include "model/fwd.hpp"

namespace steps::solver {

/// Defined Species
class Specdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the species.
    /// \param d Reference to the associated Spec object.
    Specdef(Statedef& sd, spec_global_id idx, model::Spec& d);

    Specdef(const Specdef&) = delete;
    Specdef& operator=(const Specdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: SPECIES
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this species.
    inline spec_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the species.
    inline std::string const& name() const noexcept {
        return pName;
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////
    /// Setup the object.
    ///
    /// This method is included for consistency with other def objects,
    /// but currently does nothing.
    void setup(const Statedef&);

  private:
    const spec_global_id pIdx;
    const std::string pName;
    bool pSetupdone{false};
};

}  // namespace steps::solver
