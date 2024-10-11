/*
 ___license_placeholder___
 */

#pragma once

// Standard headers.
#include <cassert>
#include <fstream>
#include <vector>

// STEPS headers.
#include "solver/compdef.hpp"
#include "wmvol.hpp"

namespace steps::tetexact {

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

    Comp(solver::Compdef* compdef);
    ~Comp();

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

    inline uint countTets() const noexcept {
        return pTets.size();
    }

    WmVol* pickTetByVol(double rand01) const;

    inline WmVolPVecCI bgnTet() const noexcept {
        return pTets.begin();
    }
    inline WmVolPVecCI endTet() const noexcept {
        return pTets.end();
    }
    inline const WmVolPVec& tets() const noexcept {
        return pTets;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    solver::Compdef* pCompdef;
    double pVol;

    WmVolPVec pTets;
};

}  // namespace steps::tetexact
