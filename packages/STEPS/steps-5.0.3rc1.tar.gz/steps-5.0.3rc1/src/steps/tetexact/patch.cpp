/*
 ___license_placeholder___
 */

// STEPS headers.
#include "patch.hpp"
#include "kproc.hpp"
#include "model/reac.hpp"
#include "solver/compdef.hpp"

// logging
#include "util/error.hpp"

namespace steps::tetexact {


////////////////////////////////////////////////////////////////////////////////

Patch::Patch(solver::Patchdef* patchdef)
    : pPatchdef(patchdef) {
    AssertLog(pPatchdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

Patch::~Patch() = default;

////////////////////////////////////////////////////////////////////////////////

void Patch::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Patch::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Patch::addTri(Tri* tri) {
    AssertLog(tri->patchdef() == def());
    pTris.push_back(tri);
    pArea += tri->area();
}

////////////////////////////////////////////////////////////////////////////////

Tri* Patch::pickTriByArea(double rand01) const {
    if (countTris() == 0) {
        return nullptr;
    }
    if (countTris() == 1) {
        return pTris[0];
    }

    double accum = 0.0;
    double selector = rand01 * area();
    for (auto const& t: tris()) {
        accum += t->area();
        if (selector <= accum) {
            return t;
        }
    }

    return *(endTri() - 1);
}

}  // namespace steps::tetexact
