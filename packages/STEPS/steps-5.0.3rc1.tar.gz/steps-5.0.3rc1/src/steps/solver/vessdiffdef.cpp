/*
 ___license_placeholder___
 */

#include "vessdiffdef.hpp"

#include "model/spec.hpp"
#include "solver/fwd.hpp"
#include "solver/specdef.hpp"
#include "solver/statedef.hpp"
#include "util/checkpointing.hpp"
#include "util/error.hpp"

namespace steps::solver {

VesSDiffdef::VesSDiffdef(Statedef& sd, vessdiff_global_id idx, model::VesSDiff& vsd)
    : pIdx(idx)
    , pName(vsd.getID())
    , pDcst(vsd.getDcst())
    , pLig(sd.getSpecIdx(vsd.getLig().getID())) {}

////////////////////////////////////////////////////////////////////////////////

void VesSDiffdef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void VesSDiffdef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void VesSDiffdef::setup() {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::solver
