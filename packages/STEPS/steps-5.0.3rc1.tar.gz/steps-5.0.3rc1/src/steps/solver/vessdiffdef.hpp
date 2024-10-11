/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>

#include "model/vessdiff.hpp"
#include "solver/fwd.hpp"

namespace steps::solver {

/// Defined diffusion on vesicle surface object.

class VesSDiffdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the object.
    /// \param vsd Reference to the associated VesSDiff object.
    VesSDiffdef(Statedef& sd, vessdiff_global_id idx, model::VesSDiff& vsd);

    VesSDiffdef(const VesSDiffdef&) = delete;
    VesSDiffdef& operator=(const VesSDiffdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////

    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: VESICLE SURFACE DIFFUSION RULE
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this vesicle surface diffusion rule.
    inline vessdiff_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of this vesicle surface diffusion rule.
    inline std::string const& name() const noexcept {
        return pName;
    }

    /// Return the diffusion constant.
    inline double dcst() const noexcept {
        return pDcst;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: LIGAND
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of the ligand species.
    spec_global_id lig() const noexcept {
        return pLig;
    }

    int dep(spec_global_id gidx) const noexcept {
        if (gidx == lig()) {
            return 1;
        } else {
            return 0;
        }
    }
    bool reqspec(spec_global_id gidx) const noexcept {
        return gidx == lig();
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Setup the object.
    void setup();

    ////////////////////////////////////////////////////////////////////////

  private:
    /// The global index of this diffusion rule
    const vessdiff_global_id pIdx;

    /// The string identifier of this diffusion rule
    const std::string pName;

    /// The diffusion constant
    const double pDcst;

    /// The chemical species to which this diffusion rule applies,
    /// safer to store as a string, rather than model level spec object pointer
    const spec_global_id pLig;
};

}  // namespace steps::solver
