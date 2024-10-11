/*
 ___license_placeholder___
 */

#include "solver/raftgendef.hpp"

#include "solver/statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

RaftGendef::RaftGendef(Statedef& sd, raftgen_global_id idx, model::RaftGen& raftgen)
    : pIdx(idx)
    , pName(raftgen.getID())
    , pKcst(raftgen.getKcst())
    , pCountSpecs(sd.countSpecs())
    , pSDeps(raftgen.getSpecSignature())
    , pRaft(raftgen.getRaft()) {
    pSpec_S_DEP.container().resize(pCountSpecs, DEP_NONE);
    pSpec_S_LHS.container().resize(pCountSpecs);
}


////////////////////////////////////////////////////////////////////////////////

void RaftGendef::checkpoint(std::fstream& /*cp_file*/) const {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void RaftGendef::restore(std::fstream& /*cp_file*/) {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void RaftGendef::setup(const Statedef& sd) {
    AssertLog(pSetupdone == false);

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

    // Find the raftdef.
    raft_global_id raftidx = sd.getRaftIdx(pRaft);
    pRaftdef = sd.rafts()[raftidx].get();

    // That's it
    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

int RaftGendef::dep_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_S_DEP.at(gidx);
}

////////////////////////////////////////////////////////////////////////////////

bool RaftGendef::reqspec_S(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    if (pSpec_S_DEP.at(gidx) != DEP_NONE) {
        return true;
    }
    return false;
}

}  // namespace steps::solver
