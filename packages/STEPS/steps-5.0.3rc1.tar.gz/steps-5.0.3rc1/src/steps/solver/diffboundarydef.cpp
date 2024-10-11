/*
 ___license_placeholder___
 */

#include "diffboundarydef.hpp"

#include "geom/diffboundary.hpp"
#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

////////////////////////////////////////////////////////////////////////////////

DiffBoundarydef::DiffBoundarydef(Statedef&, diffboundary_global_id idx, tetmesh::DiffBoundary& db)
    : pIdx(idx)
    , pName(db.getID())
    , pTris(db._getAllTriIndices()) {
    const auto& comps = db.getComps();
    pCompA_temp = comps[0];
    pCompB_temp = comps[1];
    AssertLog(pCompA_temp != nullptr);
    AssertLog(pCompB_temp != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundarydef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundarydef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundarydef::setup(Statedef& sd) {
    AssertLog(pSetupdone == false);

    pCompA = sd.getCompIdx(*pCompA_temp);
    pCompB = sd.getCompIdx(*pCompB_temp);
    pSetupdone = true;
}

}  // namespace steps::solver
