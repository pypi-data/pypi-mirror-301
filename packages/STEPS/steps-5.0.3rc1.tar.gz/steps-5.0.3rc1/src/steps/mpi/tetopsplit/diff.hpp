/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <array>
#include <fstream>
#include <map>
#include <random>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/diffdef.hpp"
#include "tetopsplit.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Tet;
class Tri;
class WmVol;

////////////////////////////////////////////////////////////////////////////////

class Diff: public mpi::tetopsplit::KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Diff(solver::Diffdef* ddef, mpi::tetopsplit::Tet* tet);
    Diff(const Diff&) = delete;

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

    inline solver::Diffdef* def() const noexcept {
        return pDiffdef;
    }

    double dcst(int direction = -1);
    void setDcst(double d);
    void setDirectionDcst(int direction, double dcst);

    void setupDeps() override;
    /*
    bool depSpecTet(solver::spec_global_id gidx, mpi::tetopsplit::WmVol *
    tet) override; bool depSpecTri(solver::spec_global_id gidx,
    mpi::tetopsplit::Tri * tri) override;
    */
    void reset() override;
    double rate(mpi::tetopsplit::TetOpSplitP* solver = nullptr) override;

    using KProc::apply;
    int apply(const rng::RNGptr& rng) override;
    int apply(const rng::RNGptr& rng, uint nmolcs) override;

    std::vector<KProc*> const& getLocalUpdVec(int direction = -1) const override;
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(int direction = -1) const override;

    ////////////////////////////////////////////////////////////////////////

    void setDiffBndActive(uint i, bool active);

    bool getDiffBndActive(uint i) const;

    //////////////// ADDED FOR OPSPLIT/MPI ////////////////////

    inline double getScaledDcst(
        mpi::tetopsplit::TetOpSplitP* /*solver */ = nullptr) const noexcept override {
        return pScaledDcst;
    }

    inline solver::spec_local_id getLigLidx() const noexcept {
        return lidxTet;
    }

    inline mpi::tetopsplit::Tet* getTet() noexcept {
        return pTet;
    }

    // MPI STUFF
    inline bool getInHost() const noexcept override {
        return pTet->getInHost();
    }

    inline int getHost() const noexcept override {
        return pTet->getHost();
    }

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Diffdef* pDiffdef;
    mpi::tetopsplit::Tet* pTet;

    // Local index (to tet) of the diffusing species
    solver::spec_local_id lidxTet;

    std::map<uint, double> directionalDcsts;


    /// Properly scaled diffusivity constant.
    double pScaledDcst{};
    // Compartmental dcst. Stored for convenience
    double pDcst{};

    // A flag to see if the species can move between compartments
    std::array<bool, 4> pDiffBndActive{false, false, false, false};

    // Flags to store if a direction is a diffusion boundary direction
    std::array<bool, 4> pDiffBndDirection{false, false, false, false};

    std::array<double, 4> pNonCDFSelector{0.0, 0.0, 0.0, 0.0};

    // Storing the species local index for each neighbouring tet: Needed
    // because neighbours may belong to different compartments
    // and therefore have different spec indices
    std::array<solver::spec_local_id, 4> pNeighbCompLidx{std::nullopt,
                                                         std::nullopt,
                                                         std::nullopt,
                                                         std::nullopt};

    std::vector<KProc*> localUpdVec[4];
    std::vector<KProc*> localAllUpdVec;

    std::vector<solver::kproc_global_id> remoteUpdVec[4];
    std::vector<solver::kproc_global_id> remoteAllUpdVec;

    // empty vec to return if no update occurs
    const std::vector<KProc*> pEmptyvec;
    const std::vector<solver::kproc_global_id> idxEmptyvec;

    std::vector<uint> pDirections;
    uint pNdirections{};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetopsplit
