/*
 ___license_placeholder___
 */

#pragma once

#include "model/complex.hpp"
#include "model/complexreac.hpp"
#include "model/spec.hpp"
#include "solver/api.hpp"
#include "solver/complexeventsdef.hpp"
#include "solver/statedef.hpp"
#include "util/common.hpp"

namespace steps::solver {

/// Defined Reaction.
class ComplexReacdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the reaction.
    /// \param r Pointer to the associated ComplexReac object.
    ComplexReacdef(Statedef& sd, complexreac_global_id idx, steps::model::ComplexReac& r);

    /// Destructor
    ~ComplexReacdef() = default;

    const Statedef& statedef() const noexcept {
        return pStatedef;
    }

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: REACTION RULE
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this reaction rule.
    complexreac_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the reaction.
    const std::string& name() const {
        return pName;
    }

    /// Return the order of this reaction.
    uint order() const {
        return pOrder;
    }

    /// Return the MACROscopic reaction constant.
    double kcst() const {
        return pKcst;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: STOICHIOMETRY
    ////////////////////////////////////////////////////////////////////////
    /// \todo imcompleted.
    uint lhs(spec_global_id gidx) const;
    int dep(spec_global_id gidx) const;
    bool complexdep(complex_global_id gidx, complex_substate_id sus) const;
    uint rhs(spec_global_id gidx) const;
    int upd(spec_global_id gidx) const;
    bool reqspec(spec_global_id gidx) const;

    const spec_global_id_vec& updColl() const noexcept {
        return pSpec_UPD_Coll;
    }
    spec_global_id_vec& updColl() noexcept {
        return pSpec_UPD_Coll;
    }
    const std::map<complex_global_id, std::set<complex_substate_id>>& complexUPDMAP()
        const noexcept {
        return pComplex_UPDMAP;
    }

    const solver::spec_global_id_vec& UPD_Coll() const noexcept {
        return pSpec_UPD_Coll;
    }

    const std::vector<std::shared_ptr<ComplexUpdateEventdef>>& updEvents() const noexcept {
        return pComplexUPDEvs;
    }
    const std::vector<std::shared_ptr<ComplexDeleteEventdef>>& delEvents() const noexcept {
        return pComplexDELEvs;
    }
    const std::vector<std::shared_ptr<ComplexCreateEventdef>>& creEvents() const noexcept {
        return pComplexCREEvs;
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////
    /// Setup the object.
    void setup();

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    Statedef& pStatedef;
    const complexreac_global_id pIdx;
    const std::string pName;
    const uint pOrder;
    const double pKcst;

    // The stoichiometry stored as model level Spec objects.
    // To be used during setup ONLY
    const std::vector<model::Spec*> pLhs;
    const std::vector<model::Spec*> pRhs;

    bool pSetupdone{false};

    ////////////////////////////////////////////////////////////////////////
    // DATA: STOICHIOMETRY
    ////////////////////////////////////////////////////////////////////////

    util::strongid_vector<spec_global_id, depT> pSpec_DEP;
    util::strongid_vector<spec_global_id, uint> pSpec_LHS;
    util::strongid_vector<spec_global_id, uint> pSpec_RHS;
    util::strongid_vector<spec_global_id, int> pSpec_UPD;
    spec_global_id_vec pSpec_UPD_Coll;

    std::vector<std::shared_ptr<ComplexUpdateEventdef>> pComplexUPDEvs;
    std::vector<std::shared_ptr<ComplexDeleteEventdef>> pComplexDELEvs;
    std::vector<std::shared_ptr<ComplexCreateEventdef>> pComplexCREEvs;

    // cmplxIdx -> {sub unit states ind}
    std::map<complex_global_id, std::set<complex_substate_id>> pComplex_DEPMAP;
    std::map<complex_global_id, std::set<complex_substate_id>> pComplex_UPDMAP;
};

}  // namespace steps::solver
