/*
 ___license_placeholder___
 */

#include "solver/exocytosisdef.hpp"

#include "model/exocytosis.hpp"
#include "solver/statedef.hpp"
#include "util/checkpointing.hpp"
#include "util/error.hpp"

namespace steps::solver {

Exocytosisdef::Exocytosisdef(Statedef& sd, exocytosis_global_id idx, model::Exocytosis& exo)
    : pIdx(idx)
    , pName(exo.getID())
    , pKcst(exo.getKcst())
    , pDefaultKcst(exo.getKcst())
    , pVDeps(exo.getSpecDeps())
    , pRaft(exo.getRaft())
    , pKissAndRun(exo.getKissAndRun())
    , pKissAndRunPartRelease(exo.getKissAndRunPartRelease()) {
    for (auto const& [src, dst]: exo.getKissAndRunSpecChanges()) {
        spec_global_id sidx_src = sd.getSpecIdx(*src);
        spec_global_id sidx_dst = sd.getSpecIdx(*dst);
        AssertLog(sidx_src != sidx_dst);
        pKissAndRunSpecChanges.emplace(sidx_src, sidx_dst);
    }

    if (pRaft != nullptr) {
        AssertLog(pKissAndRun == false);
    }

    uint nspecs = sd.countSpecs();
    pSpec_V_LHS.container().resize(nspecs);
    pSpec_V_DEP.container().resize(nspecs, DEP_NONE);
}

////////////////////////////////////////////////////////////////////////////////

void Exocytosisdef::checkpoint(std::fstream& cp_file) const {
    util::checkpoint(cp_file, pKcst);
    util::checkpoint(cp_file, pExtent);
    util::checkpoint(cp_file, pEvents);
}

////////////////////////////////////////////////////////////////////////////////

void Exocytosisdef::restore(std::fstream& cp_file) {
    util::restore(cp_file, pKcst);
    util::restore(cp_file, pExtent);
    util::restore(cp_file, pEvents);
}

////////////////////////////////////////////////////////////////////////////////

void Exocytosisdef::setKcst(double k) {
    AssertLog(k >= 0.0);
    pKcst = k;
}

////////////////////////////////////////////////////////////////////////////////

void Exocytosisdef::setup(const Statedef& sd) {
    AssertLog(pSetupdone == false);

    for (auto const& sl: pVDeps) {
        spec_global_id sidx = sd.getSpecIdx(*sl);
        pSpec_V_LHS[sidx] += 1;
    }

    // Now set up the update vector
    uint nspecs = sd.countSpecs();
    // Deal with surface.
    // most convenient just to work with uints here (not strong ids)
    for (auto i: spec_global_id::range(nspecs)) {
        int lhs = static_cast<int>(pSpec_V_LHS[i]);
        if (lhs != 0) {
            pSpec_V_DEP[i] |= DEP_STOICH;
        }
    }

    // Find the raftdef. Might be NULL
    if (pRaft != nullptr) {
        raft_global_id raftidx = sd.getRaftIdx(*pRaft);
        pRaftdef = sd.rafts()[raftidx].get();
    }

    // That's it
    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

int Exocytosisdef::dep_V(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_V_DEP.at(gidx);
}

////////////////////////////////////////////////////////////////////////////////

uint Exocytosisdef::lhs_V(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_V_LHS.at(gidx);
}

////////////////////////////////////////////////////////////////////////////////

std::vector<ExocytosisEvent> Exocytosisdef::getEvents() {
    std::vector<ExocytosisEvent> copy;
    std::swap(copy, pEvents);
    return copy;
}

////////////////////////////////////////////////////////////////////////////////

void Exocytosisdef::reset() {
    pKcst = pDefaultKcst;
    pExtent = 0;
    pEvents.clear();
}

}  // namespace steps::solver
