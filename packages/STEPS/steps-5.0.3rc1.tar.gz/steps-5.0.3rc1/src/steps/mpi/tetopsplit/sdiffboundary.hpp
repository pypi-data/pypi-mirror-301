/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <vector>

// STEPS headers.
#include "patch.hpp"
#include "solver/sdiffboundarydef.hpp"

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

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
    Patch* patchA();

    Patch* patchB();

    void setPatches(Patch* patcha, Patch* patchb);

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
    Patch* pPatchA;
    // Compartment arbitrarily labelled 'B'
    Patch* pPatchB;

    // A big vector of all the tris connected to this diffusion boundary
    std::vector<triangle_global_id> pTris;

    // Directions have to be stored here - a tri could be connected to 2
    // different diffusion boundaries for example
    // This will be the same length as the pTets vector
    std::vector<uint> pTriDirection;
};

}  // namespace steps::mpi::tetopsplit
