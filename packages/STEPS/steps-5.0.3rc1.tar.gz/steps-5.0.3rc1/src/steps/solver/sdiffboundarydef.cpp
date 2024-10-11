/*
 ___license_placeholder___
 */

#include "sdiffboundarydef.hpp"

#include "geom/sdiffboundary.hpp"
#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

SDiffBoundarydef::SDiffBoundarydef(Statedef& sd,
                                   sdiffboundary_global_id idx,
                                   tetmesh::SDiffBoundary& sdb)
    : pStatedef(sd)
    , pIdx(idx)
    , pName(sdb.getID())
    , pBars(sdb.getAllBarIndices())
    , pPatches(sdb.getPatches()) {
    AssertLog(pPatches.size() == 2);
    AssertLog(pPatches[0] != nullptr);
    AssertLog(pPatches[1] != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundarydef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundarydef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundarydef::setup() {
    AssertLog(pSetupdone == false);

    pPatchA = pStatedef.getPatchIdx(*pPatches[0]);
    pPatchB = pStatedef.getPatchIdx(*pPatches[1]);
    pSetupdone = true;
}

}  // namespace steps::solver
