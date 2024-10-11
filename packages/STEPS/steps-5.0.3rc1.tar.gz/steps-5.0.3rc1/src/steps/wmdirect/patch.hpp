/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <cassert>
#include <fstream>
#include <vector>

// STEPS headers.
#include "comp.hpp"
#include "complexsreac.hpp"
#include "kproc.hpp"
#include "solver/patchdef.hpp"
#include "sreac.hpp"

namespace steps::wmdirect {

// Forward declarations.
class Patch;
class Wmdirect;

// Auxiliary declarations.
typedef Patch* PatchP;
typedef std::vector<PatchP> PatchPVec;
typedef PatchPVec::iterator PatchPVecI;
typedef PatchPVec::const_iterator PatchPVecCI;

class Patch {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Patch(solver::Patchdef* patchdef, Comp* icomp, Comp* ocomp, Wmdirect* solver);
    ~Patch();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////

    void setupKProcs(Wmdirect* wmd);
    void setupDeps();

    void reset();

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline solver::Patchdef* def() const noexcept {
        return pPatchdef;
    }

    inline Wmdirect* solver() const noexcept {
        return pSolver;
    }

    ////////////////////////////////////////////////////////////////////////

    inline std::vector<steps::wmdirect::KProc*>::const_iterator begin() const noexcept {
        return pKProcs.begin();
    }
    inline std::vector<steps::wmdirect::KProc*>::const_iterator end() const noexcept {
        return pKProcs.end();
    }
    inline uint countKProcs() const noexcept {
        return static_cast<uint>(pKProcs.size());
    }
    inline const std::vector<steps::wmdirect::KProc*>& kprocs() const noexcept {
        return pKProcs;
    }
    inline std::vector<steps::wmdirect::KProc*>& kprocs() noexcept {
        return pKProcs;
    }

    steps::wmdirect::KProc* sreac(solver::sreac_local_id lsridx) const;
    steps::wmdirect::KProc* sreac(solver::complexsreac_local_id lridx) const;

    ////////////////////////////////////////////////////////////////////////

    inline Comp* iComp() const noexcept {
        return pIComp;
    }

    inline Comp* oComp() const noexcept {
        return pOComp;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    Wmdirect* pSolver;

    solver::Patchdef* pPatchdef;

    /// The kinetic processes.
    std::vector<steps::wmdirect::KProc*> pKProcs;

    Comp* pIComp;
    Comp* pOComp;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmdirect
