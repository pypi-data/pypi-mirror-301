/*
 ___license_placeholder___
 */

#include "solver/endocytosisdef.hpp"

#include "solver/statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

Endocytosisdef::Endocytosisdef(Statedef& sd, endocytosis_global_id idx, model::Endocytosis& endo)
    : pStatedef(sd)
    , pIdx(idx)
    , pKcst(endo.getKcst())
    , pIrhs(endo.getIRHS())
    , pSDeps(endo.getSpecDeps())
    , pInner(endo.getInner()) {
    uint nspecs = sd.countSpecs();
    pSpec_S_DEP.container().resize(nspecs, DEP_NONE);
    pSpec_S_LHS.container().resize(nspecs);
}

////////////////////////////////////////////////////////////////////////////////

void Endocytosisdef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Endocytosisdef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Endocytosisdef::setup(const Statedef& sd) {
    AssertLog(pSetupdone == false);

    pVes_I_RHS_id = sd.getVesicleIdx(pIrhs);
    pVes_I_RHS = &sd.vesicledef(pVes_I_RHS_id);

    for (auto const& sl: pSDeps) {
        spec_global_id sidx = sd.getSpecIdx(*sl);
        pSpec_S_LHS[sidx] += 1;
    }

    // Now set up the update vector
    uint ngspecs = sd.countSpecs();
    // Deal with surface.
    for (auto s: spec_global_id::range(ngspecs)) {
        int lhs = static_cast<int>(pSpec_S_LHS[s]);
        if (lhs != 0) {
            pSpec_S_DEP[s] |= DEP_STOICH;
        }
    }

    // That's it
    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

Vesicledef& Endocytosisdef::rhs_I_ves() const {
    AssertLog(pSetupdone == true);
    return *pVes_I_RHS;
}

////////////////////////////////////////////////////////////////////////////////

vesicle_global_id Endocytosisdef::rhs_I_ves_uint() const {
    AssertLog(pSetupdone == true);
    return pVes_I_RHS_id;
}

////////////////////////////////////////////////////////////////////////////////

depT Endocytosisdef::dep_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_S_DEP.at(gidx);
}

////////////////////////////////////////////////////////////////////////////////

bool Endocytosisdef::reqspec_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    if (pSpec_S_DEP.at(gidx) != DEP_NONE) {
        return true;
    }
    return false;
}

}  // namespace steps::solver
