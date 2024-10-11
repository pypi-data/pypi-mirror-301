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

namespace steps::tetexact {

// Forward declarations.
class Tri;
class Tetexact;

class GHKcurr: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    GHKcurr(solver::GHKcurrdef* ghkdef, steps::tetexact::Tri* tri);
    GHKcurr(const GHKcurr&) = delete;
    ~GHKcurr() override;

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
    bool depSpecTet(solver::spec_global_id gidx, steps::tetexact::WmVol* tet) override;
    bool depSpecTri(solver::spec_global_id gidx, steps::tetexact::Tri* tri) override;
    void reset() override;


    double rate(steps::tetexact::Tetexact* solver) override;

    // double rate(double v, double T);
    std::vector<KProc*> const& apply(const rng::RNGptr& rng, double dt, double simtime) override;

    inline bool efflux() const noexcept {
        return pEffFlux;
    }

    inline void setEffFlux(bool efx) noexcept {
        pEffFlux = efx;
    }

    uint updVecSize() const noexcept override {
        return static_cast<uint>(pUpdVec.size());
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::GHKcurrdef* pGHKcurrdef;
    steps::tetexact::Tri* pTri;
    std::vector<KProc*> pUpdVec;

    // Flag if flux is outward, positive flux (true) or inward, negative flux (false)
    bool pEffFlux;

    ////////////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetexact
