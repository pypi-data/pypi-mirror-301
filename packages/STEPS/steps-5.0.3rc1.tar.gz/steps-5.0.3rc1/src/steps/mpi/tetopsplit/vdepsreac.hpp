/*
 ___license_placeholder___
 */

#pragma once

////////////////////////////////////////////////////////////////////////////////

// Standard library & STL headers.
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/vdepsreacdef.hpp"
#include "tri.hpp"

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Tri;
class TetOpSplitP;

////////////////////////////////////////////////////////////////////////////////

class VDepSReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    VDepSReac(solver::VDepSReacdef* vdsrdef, Tri* tri);
    VDepSReac(const VDepSReac&) = delete;

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
    bool depSpecTet(solver::spec_global_id  gidx, WmVol * tet) override;
    bool depSpecTri(solver::spec_global_id  gidx, Tri * tri) override;
    */
    void reset() override;

    double rate(TetOpSplitP* solver = nullptr) override;
    double getScaledDcst(TetOpSplitP* /*solver*/ = nullptr) const override {
        return 0.0;
    }

    using KProc::apply;
    void apply(const rng::RNGptr& rng, double dt, double simtime, double period) override;

    std::vector<KProc*> const& getLocalUpdVec(int direction = -1) const override;
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(int direction = -1) const override;

    void resetOccupancies() override;

    inline bool getInHost() const noexcept override {
        return pTri->getInHost();
    }

    inline int getHost() const noexcept override {
        return pTri->getHost();
    }
    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::VDepSReacdef* pVDepSReacdef;
    Tri* pTri;

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;

    // The information about the size of the comaprtment or patch, and the
    // dimensions. Important for scaling the constant.
    // As volumes and areas currently don't change this can be stored as
    // a constant.
    double pScaleFactor;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetopsplit
