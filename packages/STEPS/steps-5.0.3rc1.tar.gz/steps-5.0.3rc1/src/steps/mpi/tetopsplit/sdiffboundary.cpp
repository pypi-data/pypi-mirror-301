/*
 ___license_placeholder___
 */

// STEPS headers.
#include "sdiffboundary.hpp"
// logging
#include "util/error.hpp"

namespace steps::mpi::tetopsplit {

SDiffBoundary::SDiffBoundary(solver::SDiffBoundarydef* sdbdef)
    : pSDiffBoundarydef(sdbdef)
    , pSetPatches(false)
    , pPatchA(nullptr)
    , pPatchB(nullptr) {
    AssertLog(sdbdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundary::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundary::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundary::setPatches(Patch* patcha, Patch* patchb) {
    AssertLog(!pSetPatches);
    AssertLog(patcha != nullptr);
    AssertLog(patchb != nullptr);
    AssertLog(patcha != patchb);

    pPatchA = patcha;
    pPatchB = patchb;
    pSetPatches = true;
}

////////////////////////////////////////////////////////////////////////////////

Patch* SDiffBoundary::patchA() {
    AssertLog(pSetPatches);
    return pPatchA;
}

////////////////////////////////////////////////////////////////////////////////

Patch* SDiffBoundary::patchB() {
    AssertLog(pSetPatches);
    return pPatchB;
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundary::setTriDirection(triangle_global_id tri, uint direction) {
    AssertLog(direction < 3);

    pTris.push_back(tri);
    pTriDirection.push_back(direction);
}

}  // namespace steps::mpi::tetopsplit
