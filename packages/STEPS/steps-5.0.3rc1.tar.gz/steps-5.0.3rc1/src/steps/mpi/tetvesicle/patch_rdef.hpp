/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <fstream>
#include <list>
#include <vector>

// STEPS headers.
#include "mpi/tetvesicle/tri_rdef.hpp"
#include "solver/patchdef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
// class PatchRDEF;
class Endocytosis;

////////////////////////////////////////////////////////////////////////////////

class PatchRDEF {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    PatchRDEF(solver::Patchdef* patchdef, tetmesh::Tetmesh* mesh, TetVesicleRDEF* rdef);
    ~PatchRDEF();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // Additions and setup
    ////////////////////////////////////////////////////////////////////////

    void reset() const;

    // void setupRafts();

    ////////////////////////////////////////////////////////////////////////
    // DATA, MEMBER ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::Patchdef* def() const noexcept {
        return pPatchdef;
    }

    inline tetmesh::Tetmesh* mesh() const noexcept {
        return pMesh;
    }

    inline double area() const noexcept {
        return pArea;
    }

    /// Return the random number generator object.
    inline const rng::RNGptr& rng() const noexcept {
        return pRNG;
    }

    ////////////////////////////////////////////////////////////////////////
    // TRIANGLES
    ////////////////////////////////////////////////////////////////////////

    /// Checks whether Tri::patchdef() corresponds to this object's
    /// PatchDef. There is no check whether the Tri object has already
    /// been added to this Patch object before (i.e. no duplicate
    /// checking).
    ///
    void addTri(TriRDEF* tri);

    inline uint countTris() const {
        return pTris.size();
    }

    inline const TriRDEFPVec& tris() const noexcept {
        return pTris;
    }

    TriRDEF* tri(triangle_local_id tri_lidx) const noexcept {
        return pTris[tri_lidx.get()];
    }

    inline triangle_global_id triidx_L_to_G(triangle_local_id lidx) noexcept {
        return pTriidcs_L_to_G[lidx];
    }
    inline triangle_local_id triidx_G_to_L(triangle_global_id gidx) noexcept {
        return pTriidcs_G_to_L[gidx];
    }

    inline TetVesicleRDEF* solverRDEF() {
        return pRDEF;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Patchdef* pPatchdef;
    double pArea;

    tetmesh::Tetmesh* pMesh;

    // Just easier to store the solver for all the raft KProc stuff
    TetVesicleRDEF* pRDEF{nullptr};

    // Store a pointer to the RNG for convenience
    rng::RNGptr pRNG;

    TriRDEFPVec pTris;

    std::map<triangle_global_id, triangle_local_id> pTriidcs_G_to_L;
    std::map<triangle_local_id, triangle_global_id> pTriidcs_L_to_G;
};

}  // namespace steps::mpi::tetvesicle
