/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <fstream>
#include <vector>

// STEPS headers.
#include "solver/compdef.hpp"
#include "tet.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Comp;

// Auxiliary declarations.
typedef Comp* CompP;
typedef std::vector<CompP> CompPVec;
typedef CompPVec::iterator CompPVecI;
typedef CompPVec::const_iterator CompPVecCI;

////////////////////////////////////////////////////////////////////////////////

class Comp {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    explicit Comp(solver::Compdef* compdef);

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    /// Checks whether the Tet's compdef() corresponds to this object's
    /// CompDef. There is no check whether the Tet object has already
    /// been added to this Comp object before (i.e. no duplicate checking).
    ///
    void addTet(WmVol* tet);

    ////////////////////////////////////////////////////////////////////////

    inline void reset() {
        def()->reset();
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::Compdef* def() const noexcept {
        return pCompdef;
    }

    inline double vol() const noexcept {
        return pVol;
    }

    inline auto pools() const noexcept {
        return def()->pools();
    }

    void modCount(solver::spec_local_id slidx, double count) const;

    inline uint countTets() const noexcept {
        return pTets.size();
    }

    WmVol* pickTetByVol(double rand01) const;

    inline const WmVolPVec& tets() const noexcept {
        return pTets;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Compdef* pCompdef;
    double pVol{0.0};

    WmVolPVec pTets;

    ////////////////////////////////////////////////////////////////////////
};

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::mpi::tetopsplit
