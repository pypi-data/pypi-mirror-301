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
#include "solver/reacdef.hpp"

namespace steps::tetexact {

// Forward declarations.
class WmVol;
class Tri;
class Tetexact;

class Reac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Reac(solver::Reacdef* rdef, WmVol* tet);
    Reac(const Reac&) = delete;
    ~Reac() override;

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

    double c() const override {
        return pCcst;
    }
    void _resetCcst();

    inline double kcst() const {
        return pKcst;
    }
    void setKcst(double k);

    double h() override {
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

    uint updVecSize() const override {
        return static_cast<uint>(pUpdVec.size());
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Reacdef* pReacdef;
    WmVol* pTet;
    std::vector<KProc*> pUpdVec;
    /// Properly scaled reaction constant.
    double pCcst;
    // Also store the K constant for convenience
    double pKcst;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetexact
