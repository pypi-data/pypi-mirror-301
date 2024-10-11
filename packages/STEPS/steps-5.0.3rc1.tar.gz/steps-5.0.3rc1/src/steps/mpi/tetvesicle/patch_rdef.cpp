/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/patch_rdef.hpp"

// STEPS headers.
#include "math/point.hpp"
#include "mpi/tetvesicle/kproc.hpp"
#include "mpi/tetvesicle/tri_rdef.hpp"
#include "solver/compdef.hpp"
#include "solver/statedef.hpp"
#include "util/checkpointing.hpp"
#include "util/distribute.hpp"

namespace steps::mpi::tetvesicle {

////////////////////////////////////////////////////////////////////////////////

PatchRDEF::PatchRDEF(solver::Patchdef* patchdef, tetmesh::Tetmesh* mesh, TetVesicleRDEF* rdef)
    : pPatchdef(patchdef)
    , pArea(0.0)
    , pMesh(mesh)
    , pRDEF(rdef) {
    AssertLog(pPatchdef != nullptr);
    pRNG = pPatchdef->statedef().rng();
}

////////////////////////////////////////////////////////////////////////////////

PatchRDEF::~PatchRDEF() = default;

////////////////////////////////////////////////////////////////////////////////

void PatchRDEF::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pArea);
}

////////////////////////////////////////////////////////////////////////////////

void PatchRDEF::restore(std::fstream& cp_file) {
    util::compare(cp_file, pArea);
}

////////////////////////////////////////////////////////////////////////////////

void PatchRDEF::reset() const {
    def()->reset();
}

////////////////////////////////////////////////////////////////////////////////

void PatchRDEF::addTri(TriRDEF* tri) {
    AssertLog(tri->patchdef() == def());

    index_t lidx_uint = pTris.size();
    triangle_local_id lidx(lidx_uint);
    triangle_global_id gidx(tri->idx());

    pTriidcs_L_to_G.emplace(lidx, gidx);
    pTriidcs_G_to_L.emplace(gidx, lidx);

    pTris.push_back(tri);
    pArea += tri->area();

    tri->setPatchRDEF(this);
}

}  // namespace steps::mpi::tetvesicle
