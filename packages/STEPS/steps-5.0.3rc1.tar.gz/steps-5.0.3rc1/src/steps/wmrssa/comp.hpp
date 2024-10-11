/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <fstream>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "patch.hpp"
#include "solver/compdef.hpp"

namespace steps::wmrssa {

// Forward declarations.
class Comp;
class Wmrssa;

// Auxiliary declarations.
typedef Comp* CompP;
typedef std::vector<CompP> CompPVec;
typedef CompPVec::iterator CompPVecI;
typedef CompPVec::const_iterator CompPVecCI;

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

    ////////////////////////////////////////////////////////////////////////

    void setupKProcs(Wmrssa* wmd);
    void setupDeps();

    void reset();

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::Compdef* def() const {
        return pCompdef;
    }

    ////////////////////////////////////////////////////////////////////////

    inline std::vector<wmrssa::KProc*>::const_iterator begin() const noexcept {
        return pKProcs.begin();
    }
    inline std::vector<wmrssa::KProc*>::const_iterator end() const noexcept {
        return pKProcs.end();
    }
    inline uint countKProcs() const noexcept {
        return pKProcs.size();
    }
    inline const std::vector<wmrssa::KProc*> kprocs() const noexcept {
        return pKProcs;
    }

    wmrssa::KProc* reac(solver::reac_local_id lridx) const;

    ////////////////////////////////////////////////////////////////////////

    void addIPatch(Patch* p);

    inline uint countIPatches() const noexcept {
        return pIPatches.size();
    }

    inline std::vector<wmrssa::Patch*>::const_iterator beginIPatches() const noexcept {
        return pIPatches.begin();
    }
    inline std::vector<wmrssa::Patch*>::const_iterator endIPatches() const noexcept {
        return pIPatches.end();
    }
    inline const std::vector<wmrssa::Patch*>& ipatches() const noexcept {
        return pIPatches;
    }

    void addOPatch(Patch* p);

    inline uint countOPatches() const noexcept {
        return pOPatches.size();
    }

    inline std::vector<wmrssa::Patch*>::const_iterator beginOPatches() const noexcept {
        return pOPatches.begin();
    }
    inline std::vector<wmrssa::Patch*>::const_iterator endOPatches() const noexcept {
        return pOPatches.end();
    }
    inline const std::vector<wmrssa::Patch*>& opatches() const noexcept {
        return pOPatches;
    }

    ////////////////////////////////////////////////////////////////////////

    void setBounds(solver::spec_local_id i, int nc);
    bool isOutOfBound(solver::spec_local_id i, int nc);
    const util::strongid_vector<solver::spec_local_id, double>& pools(
        wmrssa::PropensityRSSA prssa) const;
    void setupSpecDeps();
    std::vector<wmrssa::KProc*> const& getSpecUpdKProcs(solver::spec_local_id slidx);

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Compdef* pCompdef;

    /// The kinetic processes.
    std::vector<wmrssa::KProc*> pKProcs;

    std::vector<wmrssa::Patch*> pIPatches;
    std::vector<wmrssa::Patch*> pOPatches;
    // Table of the lower bounds on populations of the species in this
    // compartment.
    util::strongid_vector<solver::spec_local_id, double> pPoolLB;
    // Table of the upper bounds on populations of the species in this
    // compartment.
    util::strongid_vector<solver::spec_local_id, double> pPoolUB;
    util::strongid_vector<solver::spec_local_id, std::vector<wmrssa::KProc*>> localSpecUpdKProcs;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmrssa
