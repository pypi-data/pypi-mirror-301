/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/ghkcurrdef.hpp"
#include "tri.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Tri;
class TetOpSplitP;

////////////////////////////////////////////////////////////////////////////////

class GHKcurr: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    GHKcurr(solver::GHKcurrdef* ghkdef, Tri* tri);
    GHKcurr(const GHKcurr&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) override;

    /// restore data
    void restore(std::fstream& cp_file) override;

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;
    /*
    bool depSpecTet(solver::spec_global_id gidx, WmVol *
    tet) override; bool depSpecTri(solver::spec_global_id gidx,
    Tri * tri) override;
    */
    void reset() override;

    double rate(TetOpSplitP* solver) override;
    inline double getScaledDcst(TetOpSplitP* /*solver*/ = nullptr) const noexcept override {
        return 0.0;
    }

    using KProc::apply;
    void apply(const rng::RNGptr& rng, double dt, double simtime, double period) override;
    std::vector<KProc*> const& getLocalUpdVec(int direction = -1) const override;
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(int direction = -1) const override;

    void resetOccupancies() override;

    inline bool efflux() const noexcept {
        return pEffFlux;
    }

    void setEffFlux(bool efx) noexcept {
        pEffFlux = efx;
    }

    bool getInHost() const noexcept override {
        return pTri->getInHost();
    }

    int getHost() const noexcept override {
        return pTri->getHost();
    }
    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::GHKcurrdef* pGHKcurrdef;
    Tri* pTri;

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;
    // Flag if flux is outward, positive flux (true) or inward, negative flux
    // (false)
    bool pEffFlux;

    ////////////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetopsplit
