/*
 ___license_placeholder___
 */

#include "chandef.hpp"

#include "model/chan.hpp"
#include "model/chanstate.hpp"
#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

Chandef::Chandef(Statedef& /*sd*/, chan_global_id idx, model::Chan& c)
    : pIdx(idx)
    , pName(c.getID())
    , pChanStatesVec(c.getAllChanStates()) {
    pChanStates.resize(pChanStatesVec.size());
}

////////////////////////////////////////////////////////////////////////////////

void Chandef::checkpoint(std::fstream& /*cp_file*/) const {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void Chandef::restore(std::fstream& /*cp_file*/) {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void Chandef::setup(const Statedef& sd) {
    AssertLog(pSetupdone == false);
    const auto& chan_states = pChanStatesVec;
    AssertLog(chan_states.size() == nchanstates());
    for (uint i = 0; i < nchanstates(); ++i) {
        spec_global_id gidx = sd.getSpecIdx(*chan_states[i]);
        pChanStates[i] = gidx;
    }

    pSetupdone = true;
}

}  // namespace steps::solver
