/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/comp_rdef.hpp"

// STEPS headers.
#include "mpi/tetvesicle/reac.hpp"
#include "mpi/tetvesicle/tet_rdef.hpp"
#include "mpi/tetvesicle/tetvesicle_rdef.hpp"
#include "solver/compdef.hpp"
#include "solver/statedef.hpp"
#include "util/checkpointing.hpp"

namespace steps::mpi::tetvesicle {

CompRDEF::CompRDEF(solver::Compdef* compdef, tetmesh::Tetmesh* mesh, TetVesicleRDEF* rdef)
    : pCompdef(compdef)
    , pVol(0.0)
    , pMesh(mesh)
    , pRNG(rdef->rng())
    , pRDEF(rdef) {
    AssertLog(pCompdef != nullptr);
    AssertLog(pMesh != nullptr);
    AssertLog(pRDEF != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

CompRDEF::~CompRDEF() = default;

////////////////////////////////////////////////////////////////////////////////

void CompRDEF::checkpoint(std::fstream& cp_file) {
    // NOTES:
    //    pTets not owned by this object, owned by solver
    util::checkpoint(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void CompRDEF::restore(std::fstream& cp_file) {
    util::compare(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void CompRDEF::reset() const {
    def()->reset();
    // Tet objects now clear their own overlap
}

////////////////////////////////////////////////////////////////////////////////

void CompRDEF::addTet(TetRDEF* tet) {
    AssertLog(tet->compdef() == def());

    tet->setCompRDEF(this);

    index_t lidx_uint = pTets.size();
    tetrahedron_local_id lidx(lidx_uint);
    tetrahedron_global_id gidx = tet->idx();

    pTetidcs_L_to_G.emplace(lidx, gidx);
    pTetidcs_G_to_L.emplace(gidx, lidx);

    pTets.push_back(tet);

    pVol += tet->vol();
}

////////////////////////////////////////////////////////////////////////////////

steps::tetrahedron_global_id CompRDEF::tetidx_L_to_G(tetrahedron_local_id lidx) const {
    auto it = pTetidcs_L_to_G.find(lidx);
    AssertLog(it != pTetidcs_L_to_G.end());

    return it->second;
}

////////////////////////////////////////////////////////////////////////////////

steps::tetrahedron_local_id CompRDEF::tetidx_G_to_L(tetrahedron_global_id gidx) const {
    auto it = pTetidcs_G_to_L.find(gidx);
    AssertLog(it != pTetidcs_G_to_L.end());

    return it->second;
}

////////////////////////////////////////////////////////////////////////////////

TetRDEF* CompRDEF::pickTetByVol(double rand01) const {
    // This function picks by excluded volume, that is the volume of tetrahedrons
    // after subtracting their vesicle occupancy

    if (countTets() == 0) {
        return nullptr;
    }
    if (countTets() == 1) {
        return pTets[0];
    }

    double volume = 0.0;
    for (const auto& tet: pTets) {
        volume += tet->vol();  // tet volume may change with vesicle occupancy
    }

    double accum = 0.0;
    double selector = rand01 * volume;

    for (const auto& tet: pTets) {
        accum += tet->vol();
        if (selector < accum) {
            return tet;
        }
    }
    AssertLog(false);
    return nullptr;
}

}  // namespace steps::mpi::tetvesicle
