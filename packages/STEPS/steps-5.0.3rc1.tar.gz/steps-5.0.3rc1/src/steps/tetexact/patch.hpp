/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <fstream>
#include <vector>

// STEPS headers.
#include "solver/patchdef.hpp"
#include "tri.hpp"

namespace steps::tetexact {

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

    inline void reset() {
        def()->reset();
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::Patchdef* def() const noexcept {
        return pPatchdef;
    }

    inline double area() const noexcept {
        return pArea;
    }

    inline uint countTris() const noexcept {
        return static_cast<uint>(pTris.size());
    }

    Tri* pickTriByArea(double rand01) const;

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
    double pArea{0.0};

    TriPVec pTris;
};

}  // namespace steps::tetexact
