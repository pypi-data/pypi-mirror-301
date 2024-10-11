/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <fstream>
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/sreacdef.hpp"

namespace steps::tetexact {

// Forward declarations.
class Tri;
class Tetexact;

class SReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    SReac(solver::SReacdef* srdef, Tri* tri);
    SReac(const SReac&) = delete;
    ~SReac() override;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) override;

    /// restore data
    void restore(std::fstream& cp_file) override;

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline double c() const noexcept override {
        return pCcst;
    }

    void _resetCcst();

    inline double kcst() const noexcept {
        return pKcst;
    }

    void setKcst(double k);

    inline double h() override {
        return rate() / pCcst;
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;
    bool depSpecTet(solver::spec_global_id gidx, WmVol* tet) override;
    bool depSpecTri(solver::spec_global_id gidx, Tri* tri) override;
    void reset() override;
    double rate(Tetexact* solver = nullptr) override;
    std::vector<KProc*> const& apply(const rng::RNGptr& rng, double dt, double simtime) override;

    inline uint updVecSize() const noexcept override {
        return pUpdVec.size();
    }

    ////////////////////////////////////////////////////////////////////////

    // inline solver::Reacdef * defr() const
    //{ return pReacdef; }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::SReacdef* pSReacdef;
    Tri* pTri;
    std::vector<KProc*> pUpdVec;
    /// Properly scaled reaction constant.
    double pCcst;
    // Store the kcst for convenience
    double pKcst;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetexact
