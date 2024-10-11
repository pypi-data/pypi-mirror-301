/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <vector>

// STEPS headers.
#include "comp.hpp"
#include "solver/diffboundarydef.hpp"

namespace steps::tetexact {

// Forward declarations.
class DiffBoundary;

// Auxiliary declarations.
typedef DiffBoundary* DiffBoundaryP;
typedef std::vector<DiffBoundaryP> DiffBoundaryPVec;
typedef DiffBoundaryPVec::iterator DiffBoundaryPVecI;
typedef DiffBoundaryPVec::const_iterator DiffBoundaryPVecCI;


////////////////////////////////////////////////////////////////////////////////

class DiffBoundary {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    explicit DiffBoundary(solver::DiffBoundarydef* dbdef);
    ~DiffBoundary();

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

    inline solver::DiffBoundarydef* def() const noexcept {
        return pDiffBoundarydef;
    }

    // We need access to the compartments so as to check if species are defined
    Comp* compA();

    Comp* compB();

    void setComps(Comp* compa, Comp* compb);

    // Other data we need is the TETRAHEDRONS (not triangles) affected by
    // this diff boundary- if a solver method like setDiffBoundarySpec is called
    // then this object provides a list of tetrahedrons and importantly
    // THE DIRECTION OF DIFFUSION (the direction that is to the next compartment)
    // the solver can then simply loop over the tets and activate diffusion
    // in that direction (or we could do it here)


    // This information is the tetrahedron connected to this diffusion boundary
    // and the direction of the diffusion boundary for that tetrahedron (0 to 3)
    void setTetDirection(tetrahedron_global_id tet, uint direction);


    inline const std::vector<tetrahedron_global_id>& getTets() const noexcept {
        return pTets;
    }

    inline const std::vector<uint>& getTetDirection() const noexcept {
        return pTetDirection;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::DiffBoundarydef* pDiffBoundarydef;

    // Bool to check if compartments have been specified
    bool pSetComps{false};

    // Compartment arbitrarily labelled 'A'
    Comp* pCompA{nullptr};
    // Compartment arbitrarily labelled 'B'
    Comp* pCompB{nullptr};

    // A big vector of all the tetrahedrons connected to this diffusion boundary
    // If the diff boundary allows passage of an ion these tets will tell
    // their diffs for that ion to allow diffusion
    // The direction information I'm thinking will come from WHERE??
    std::vector<tetrahedron_global_id> pTets;

    // Directions have to be stored here - a tet could be connected to 2
    // different diffusion boundaries for example
    // This will be the same length as the pTets vector
    std::vector<uint> pTetDirection;
};

}  // namespace steps::tetexact
