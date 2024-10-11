/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <vector>

// logging
#include "util/error.hpp"
#include "util/vocabulary.hpp"

// STEPS headers.
#include "solver/patchdef.hpp"

namespace steps::tetode {

// Forward declarations

class Tet;
class Tri;
class TetODE;

////////////////////////////////////////////////////////////////////////////////

// Auxiliary declarations.
typedef Tri* TriP;
typedef std::vector<TriP> TriPVec;
typedef TriPVec::iterator TriPVecI;
typedef TriPVec::const_iterator TriPVecCI;

////////////////////////////////////////////////////////////////////////////////

class Tri {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Tri(triangle_global_id idx,
        solver::Patchdef* patchdef,
        double area,
        double l0,
        double l1,
        double l2,
        double d0,
        double d1,
        double d2,
        tetrahedron_global_id tetinner,
        tetrahedron_global_id tetouter,
        triangle_global_id tri0,
        triangle_global_id tri1,
        triangle_global_id tri2);
    ~Tri();

    ////////////////////////////////////////////////////////////////////////
    // SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Set pointer to the 'inside' neighbouring tetrahedron.
    ///
    void setInnerTet(Tet* t);

    /// Set pointer to the 'outside' neighbouring tetrahedron.
    ///
    void setOuterTet(Tet* t);

    /// Set pointer to the next neighbouring triangle.
    void setNextTri(uint i, Tri* t);

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: GENERAL
    ////////////////////////////////////////////////////////////////////////

    inline solver::Patchdef* patchdef() const noexcept {
        return pPatchdef;
    }

    inline triangle_global_id idx() const noexcept {
        return pIdx;
    }

    inline double area() const noexcept {
        return pArea;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: SHAPE & CONNECTIVITY
    ////////////////////////////////////////////////////////////////////////

    inline Tet* iTet() const noexcept {
        return pInnerTet;
    }

    inline Tet* oTet() const noexcept {
        return pOuterTet;
    }

    inline Tri* nextTri(uint i) const {
        AssertLog(i < 3);
        return pNextTri[i];
    }

    inline triangle_global_id tri(uint t) noexcept {
        return pTris[t];
    }

    /// Get the length of a boundary bar.
    ///
    inline double length(uint i) const noexcept {
        return pLengths[i];
    }

    /// Get the distance to the centroid of the next neighbouring
    /// triangle.
    ///
    inline double dist(uint i) const noexcept {
        return pDist[i];
    }

    inline tetrahedron_global_id tet(uint t) const noexcept {
        return pTets[t];
    }

    ////////////////////////////////////////////////////////////////////////
    // MAIN FUNCTIONALITY
    ////////////////////////////////////////////////////////////////////////

    double getOhmicI(double v, TetODE* solver) const;

    double getGHKI(double v, double dt, steps::tetode::TetODE* solver) const;

    // Set/get the reversal potential of an ohmic current
    void setOCerev(solver::ohmiccurr_local_id oclidx, double erev);
    double getOCerev(solver::ohmiccurr_local_id oclidx) const;

  private:
    ////////////////////////////////////////////////////////////////////////

    triangle_global_id pIdx;

    solver::Patchdef* pPatchdef;

    /// Pointers to neighbouring tetrahedra.
    Tet* pInnerTet{nullptr};
    Tet* pOuterTet{nullptr};

    // Indices of two neighbouring tets; -1 if surface triangle (if
    // triangle's patch is on the surface of the mesh, quite often the case)
    std::array<tetrahedron_global_id, 2> pTets;

    // Indices of neighbouring triangles.
    std::array<triangle_global_id, 3> pTris;

    /// POinters to neighbouring triangles
    std::array<Tri*, 3> pNextTri;

    double pArea;

    // Neighbour information- needed for surface diffusion
    std::array<double, 3> pLengths;
    std::array<double, 3> pDist;

    // Store reversal potential here to enable modification within API
    std::map<solver::ohmiccurr_local_id, double> pERev;
};

}  // namespace steps::tetode
