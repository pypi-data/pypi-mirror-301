/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <fstream>
#include <map>
#include <vector>

// STEPS headers.
#include "solver/patchdef.hpp"
#include "tri.hpp"

namespace steps::tetode {


// Forward declarations.
class Patch;

// Auxiliary declarations.
typedef Patch* PatchP;
typedef std::vector<PatchP> PatchPVec;
typedef PatchPVec::iterator PatchPVecI;
typedef PatchPVec::const_iterator PatchPVecCI;

////////////////////////////////////////////////////////////////////////////////

class Patch {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Patch(solver::Patchdef* patchdef);
    ~Patch();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    /// Checks whether Tri::patchdef() corresponds to this object's
    /// PatchDef. There is no check whether the Tri object has already
    /// been added to this Patch object before (i.e. no duplicate
    /// checking).
    ///
    void addTri(Tri* tri);

    ////////////////////////////////////////////////////////////////////////

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline double area() const noexcept {
        return pArea;
    }

    // Return the local index of a tri given by global index
    triangle_local_id getTri_GtoL(triangle_global_id gidx);

    // Return the tri of a given local index
    Tri* getTri(triangle_local_id lidx);

    inline solver::Patchdef& def() const noexcept {
        return *pPatchdef;
    }

    inline uint countTris() const noexcept {
        return pTris.size();
    }

    inline TriPVecCI bgnTri() const noexcept {
        return pTris.begin();
    }
    inline TriPVecCI endTri() const noexcept {
        return pTris.end();
    }
    inline const TriPVec& tris() const noexcept {
        return pTris;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Patchdef* pPatchdef;

    TriPVec pTris;

    double pArea;

    // A map storing global index to local
    std::map<triangle_global_id, triangle_local_id> pTris_GtoL;
};

}  // namespace steps::tetode
