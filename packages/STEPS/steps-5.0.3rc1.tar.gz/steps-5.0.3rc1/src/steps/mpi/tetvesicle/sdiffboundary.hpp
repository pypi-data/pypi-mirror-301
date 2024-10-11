/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <vector>

// STEPS headers.
#include "mpi/tetvesicle/patch_rdef.hpp"

#include "solver/sdiffboundarydef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
class SDiffBoundary;

// Auxiliary declarations.
typedef SDiffBoundary* SDiffBoundaryP;
typedef std::vector<SDiffBoundaryP> SDiffBoundaryPVec;
typedef SDiffBoundaryPVec::iterator SDiffBoundaryPVecI;
typedef SDiffBoundaryPVec::const_iterator SDiffBoundaryPVecCI;

////////////////////////////////////////////////////////////////////////////////

class SDiffBoundary {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    explicit SDiffBoundary(solver::SDiffBoundarydef* sdbdef);

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::SDiffBoundarydef* def() const noexcept {
        return pSDiffBoundarydef;
    }

    // We need access to the compartments so as to check if species are defined
    PatchRDEF* patchA();

    PatchRDEF* patchB();

    void setPatches(PatchRDEF* patcha, PatchRDEF* patchb);

    void setTriDirection(triangle_global_id tri, uint direction);

    const std::vector<triangle_global_id>& getTris() const noexcept {
        return pTris;
    }

    const std::vector<uint>& getTriDirection() const noexcept {
        return pTriDirection;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::SDiffBoundarydef* pSDiffBoundarydef;

    // Bool to check if patches have been specified
    bool pSetPatches;

    // Patch arbitrarily labelled 'A'
    PatchRDEF* pPatchA;
    // Compartment arbitrarily labelled 'B'
    PatchRDEF* pPatchB;

    // A big vector of all the tris connected to this diffusion boundary
    std::vector<triangle_global_id> pTris;

    // Directions have to be stored here - a tri could be connected to 2
    // different diffusion boundaries for example
    // This will be the same length as the pTets vector
    std::vector<uint> pTriDirection;
};

}  // namespace steps::mpi::tetvesicle
