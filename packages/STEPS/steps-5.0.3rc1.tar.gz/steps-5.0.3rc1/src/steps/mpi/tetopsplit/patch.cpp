/*
 ___license_placeholder___
 */

#include "patch.hpp"

// Standard library & STL headers.
#include <vector>

// STEPS headers.
#include "model/reac.hpp"
#include "solver/compdef.hpp"
#include "util/checkpointing.hpp"
#include "util/error.hpp"


namespace steps::mpi::tetopsplit {

Patch::Patch(solver::Patchdef* patchdef)
    : pPatchdef(patchdef) {
    AssertLog(pPatchdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void Patch::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pArea);
}

////////////////////////////////////////////////////////////////////////////////

void Patch::restore(std::fstream& cp_file) {
    util::compare(cp_file, pArea);
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
    for (auto const& t: pTris) {
        accum += t->area();
        if (selector <= accum) {
            return t;
        }
    }

    return tris().back();
}

}  // namespace steps::mpi::tetopsplit
