/*
 ___license_placeholder___
 */

#pragma once

////////////////////////////////////////////////////////////////////////////////

// Standard library & STL headers.
#include <fstream>
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/sreacdef.hpp"
#include "tri.hpp"

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Tri;
class TetOpSplitP;

////////////////////////////////////////////////////////////////////////////////

class SReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    SReac(solver::SReacdef* srdef, mpi::tetopsplit::Tri* tri);
    SReac(const SReac&) = delete;

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
    void resetCcst() override;

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
    /*
    bool depSpecTet(solver::spec_global_id  gidx, mpi::tetopsplit::WmVol *
    tet) override; bool depSpecTri(solver::spec_global_id  gidx,
    mpi::tetopsplit::Tri * tri) override;
    */
    void reset() override;
    double rate(mpi::tetopsplit::TetOpSplitP* solver = nullptr) override;
    inline double getScaledDcst(mpi::tetopsplit::TetOpSplitP* /*solver*/ = nullptr) const override {
        return 0.0;
    }

    // We need the works here: dt and simtime needed for Ohmic Currents
    using KProc::apply;
    void apply(const rng::RNGptr& rng, double dt, double simtime, double period) override;

    std::vector<KProc*> const& getLocalUpdVec(int direction = -1) const override;
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(int direction = -1) const override;

    void resetOccupancies() override;

    ////////////////////////////////////////////////////////////////////////

    // inline solver::Reacdef * defr() const
    //{ return pReacdef; }

    ////////////////////////////////////////////////////////////////////////
    // mpi
    inline bool getInHost() const noexcept override {
        return pTri->getInHost();
    }

    inline int getHost() const noexcept override {
        return pTri->getHost();
    }

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::SReacdef* pSReacdef;
    mpi::tetopsplit::Tri* pTri;

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;

    /// Properly scaled reaction constant.
    double pCcst{0.0};
    // Store the kcst for convenience
    double pKcst{0.0};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetopsplit
