/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>

#include "model/vesunbind.hpp"
#include "solver/fwd.hpp"

namespace steps::solver {

/// Defined vesicle-vesicle unbinding reaction.
class VesUnbinddef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the vesicle binding reaction.
    /// \param vub Reference to the associated VesUnbind object.
    VesUnbinddef(Statedef& sd, vesunbind_global_id idx, model::VesUnbind& vub);

    VesUnbinddef(const VesUnbinddef&) = delete;
    VesUnbinddef& operator=(const VesUnbinddef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: VESUNBINDTION RULE
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this vesicle binding reaction rule.
    inline vesunbind_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the vesicle binding reaction.
    inline std::string const& name() const noexcept {
        return pName;
    }

    /// Return the MACROscopic vesicle binding reaction constant.
    inline double kcst() const noexcept {
        return pKcst;
    }

    inline int immobility() const noexcept {
        return pImmobility;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: STOICHIOMETRY
    ////////////////////////////////////////////////////////////////////////

    vesicle_global_id getVes1idx() const;
    vesicle_global_id getVes2idx() const;

    linkspec_global_id getLinkSpec1gidx() const;
    linkspec_global_id getLinkSpec2gidx() const;

    // The products
    spec_global_id getSpec1gidx() const;
    spec_global_id getSpec2gidx() const;

    // Placeholder. Might need to support other orders at some stage
    inline uint order() const noexcept {
        return 1;
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////
    /// Setup the object.
    void setup(const Statedef& sd);

  private:
    const vesunbind_global_id pIdx;
    const std::string pName;
    const double pKcst;
    const int pImmobility;

    // Need to copy this data for setup
    const std::pair<model::Vesicle*, model::LinkSpec*> pLinks1;
    const std::pair<model::Vesicle*, model::LinkSpec*> pLinks2;
    const std::pair<model::Vesicle*, model::Spec*> pProducts1;
    const std::pair<model::Vesicle*, model::Spec*> pProducts2;

    vesicle_global_id pVesicle_1_idx;
    vesicle_global_id pVesicle_2_idx;

    linkspec_global_id pLinkSpec_1_gidx;
    linkspec_global_id pLinkSpec_2_gidx;

    spec_global_id pSpec_1_gidx;
    spec_global_id pSpec_2_gidx;

    bool pSetupdone{false};
};

}  // namespace steps::solver
