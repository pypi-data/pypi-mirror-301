/*
 ___license_placeholder___
 */

// STEPS headers.
#include "patch.hpp"
#include "solver/statedef.hpp"
#include "wmdirect.hpp"
// logging
#include "util/error.hpp"

namespace steps::wmdirect {

Patch::Patch(solver::Patchdef* patchdef, Comp* icomp, Comp* ocomp, Wmdirect* solver)
    : pSolver(solver)
    , pPatchdef(patchdef)
    , pIComp(icomp)
    , pOComp(ocomp) {
    AssertLog(pPatchdef != nullptr);
    if (iComp() != nullptr) {
        iComp()->addIPatch(this);
    }
    if (oComp() != nullptr) {
        oComp()->addOPatch(this);
    }
}

////////////////////////////////////////////////////////////////////////////////

Patch::~Patch() {
    for (auto const& k: pKProcs) {
        delete k;
    }
}

////////////////////////////////////////////////////////////////////////////////

void Patch::checkpoint(std::fstream& cp_file) {
    for (auto const& k: pKProcs) {
        k->checkpoint(cp_file);
    }
}

////////////////////////////////////////////////////////////////////////////////

void Patch::restore(std::fstream& cp_file) {
    for (auto const& k: pKProcs) {
        k->restore(cp_file);
    }
}

////////////////////////////////////////////////////////////////////////////////

void Patch::setupKProcs(Wmdirect* wmd) {
    // Create surface reaction kproc's.
    uint nsreacs = def()->countSReacs();
    uint ncsreacs = def()->countComplexSReacs();
    pKProcs.resize(nsreacs + ncsreacs);
    for (auto i: solver::sreac_local_id::range(nsreacs)) {
        auto& srdef = def()->sreacdef(i);
        auto* sr = new SReac(&srdef, this);
        pKProcs[i.get()] = sr;
        wmd->addKProc(sr);
    }

    for (auto i: solver::complexsreac_local_id::range(ncsreacs)) {
        solver::ComplexSReacdef& csrdef = def()->complexsreacdef(i);
        auto* r = new ComplexSReac(csrdef, *this);
        pKProcs[nsreacs + i.get()] = r;
        wmd->addKProc(r);
    }
}

////////////////////////////////////////////////////////////////////////////////

void Patch::setupDeps() {
    for (auto const& kproc: pKProcs) {
        kproc->setupDeps();
    }
}

////////////////////////////////////////////////////////////////////////////////

KProc* Patch::sreac(solver::sreac_local_id lsridx) const {
    AssertLog(lsridx.get() < pKProcs.size());
    return pKProcs[lsridx.get()];
}

////////////////////////////////////////////////////////////////////////////////

KProc* Patch::sreac(solver::complexsreac_local_id lridx) const {
    uint idx = def()->countSReacs() + lridx.get();
    AssertLog(idx < pKProcs.size());
    return pKProcs[idx];
}

////////////////////////////////////////////////////////////////////////////////

void Patch::reset() {
    for (auto const& kproc: pKProcs) {
        kproc->reset();
    }
}

}  // namespace steps::wmdirect
