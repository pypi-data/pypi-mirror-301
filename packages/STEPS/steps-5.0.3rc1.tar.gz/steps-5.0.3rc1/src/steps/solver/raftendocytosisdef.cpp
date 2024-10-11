/*
 ___license_placeholder___
 */

#include "solver/raftendocytosisdef.hpp"

#include "solver/patchdef.hpp"
#include "solver/statedef.hpp"
#include "util/checkpointing.hpp"
#include "util/error.hpp"

namespace steps::solver {

RaftEndocytosisdef::RaftEndocytosisdef(Statedef& sd,
                                       raftendocytosis_global_id idx,
                                       model::RaftEndocytosis& raftendo)
    : pStatedef(sd)
    , pIdx(idx)
    , pName(raftendo.getID())
    , pKcst(raftendo.getKcst())
    , pDefaultKcst(raftendo.getKcst())
    , pIrhs(raftendo.getRHS())
    , pCountSpecs(sd.countSpecs())
    , pSDeps(raftendo.getSpecDeps())
    , pExtent(0)
    , pInner(raftendo.getInner()) {
    pSpec_S_DEP.container().resize(pCountSpecs, DEP_NONE);
    pSpec_S_LHS.container().resize(pCountSpecs);
}

////////////////////////////////////////////////////////////////////////////////

void RaftEndocytosisdef::checkpoint(std::fstream& cp_file) const {
    util::checkpoint(cp_file, pKcst);
    util::checkpoint(cp_file, pExtent);
    util::checkpoint(cp_file, pEvents);
}

////////////////////////////////////////////////////////////////////////////////

void RaftEndocytosisdef::restore(std::fstream& cp_file) {
    util::restore(cp_file, pKcst);
    util::restore(cp_file, pExtent);
    util::restore(cp_file, pEvents);
}

////////////////////////////////////////////////////////////////////////////////

void RaftEndocytosisdef::setup(const Statedef& sd) {
    AssertLog(pSetupdone == false);

    pVes_I_RHS_uint = sd.getVesicleIdx(pIrhs);
    pVes_I_RHS = &sd.vesicledef(pVes_I_RHS_uint);

    for (auto const& sl: pSDeps) {
        spec_global_id sidx = sd.getSpecIdx(*sl);
        pSpec_S_LHS[sidx] += 1;
    }

    // Now set up the update vector
    // Deal with surface.
    for (auto s: spec_global_id::range(sd.countSpecs())) {
        int lhs = static_cast<int>(pSpec_S_LHS[s]);
        if (lhs != 0) {
            pSpec_S_DEP[s] |= DEP_STOICH;
        }
    }

    // That's it
    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

void RaftEndocytosisdef::reset() {
    pKcst = pDefaultKcst;
    pExtent = 0;
    pEvents.clear();
}

////////////////////////////////////////////////////////////////////////////////

void RaftEndocytosisdef::setKcst(double kcst) {
    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

Vesicledef& RaftEndocytosisdef::rhs_I_ves() const {
    AssertLog(pSetupdone == true);
    return *pVes_I_RHS;
}

////////////////////////////////////////////////////////////////////////////////

vesicle_global_id RaftEndocytosisdef::rhs_I_ves_uint() const {
    AssertLog(pSetupdone == true);
    return pVes_I_RHS_uint;
}

////////////////////////////////////////////////////////////////////////////////

int RaftEndocytosisdef::dep_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_S_DEP.at(gidx);
}

////////////////////////////////////////////////////////////////////////////////

bool RaftEndocytosisdef::reqspec_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    if (pSpec_S_DEP.at(gidx) != DEP_NONE) {
        return true;
    }
    return false;
}

////////////////////////////////////////////////////////////////////////////////

std::vector<RaftEndocytosisEvent> RaftEndocytosisdef::getEvents() {
    std::vector<RaftEndocytosisEvent> copy;
    copy.swap(pEvents);
    return copy;
}

}  // namespace steps::solver
