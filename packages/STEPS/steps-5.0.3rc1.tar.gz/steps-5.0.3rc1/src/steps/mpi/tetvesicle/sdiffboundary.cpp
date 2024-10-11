/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/sdiffboundary.hpp"

// logging

// STEPS headers.
#include "solver/sdiffboundarydef.hpp"

namespace steps::mpi::tetvesicle {

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

void SDiffBoundary::setPatches(PatchRDEF* patcha, PatchRDEF* patchb) {
    AssertLog(!pSetPatches);
    AssertLog(patcha != nullptr);
    AssertLog(patchb != nullptr);
    AssertLog(patcha != patchb);

    pPatchA = patcha;
    pPatchB = patchb;
    pSetPatches = true;
}

////////////////////////////////////////////////////////////////////////////////

PatchRDEF* SDiffBoundary::patchA() {
    AssertLog(pSetPatches);
    return pPatchA;
}

////////////////////////////////////////////////////////////////////////////////

PatchRDEF* SDiffBoundary::patchB() {
    AssertLog(pSetPatches);
    return pPatchB;
}

////////////////////////////////////////////////////////////////////////////////

void SDiffBoundary::setTriDirection(triangle_global_id tri, uint direction) {
    AssertLog(direction < 3);

    pTris.push_back(tri);
    pTriDirection.push_back(direction);
}

}  // namespace steps::mpi::tetvesicle
