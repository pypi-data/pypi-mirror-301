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
#include "math/constants.hpp"
#include "mpi/tetvesicle/kproc.hpp"
#include "mpi/tetvesicle/tri_rdef.hpp"
#include "solver/raftgendef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
class TriRDEF;
class TetVesicleRDEF;

////////////////////////////////////////////////////////////////////////////////

class RaftGen: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    RaftGen(solver::RaftGendef* rgdef, TriRDEF* tri);
    RaftGen(const RaftGen&) = delete;
    ~RaftGen();

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

    inline double kcst() const {
        return pKcst;
    }
    void setKcst(double k);

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

#if defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Woverloaded-virtual"
#endif

    void setupDeps() override;

    void reset() override;

    double rate(TetVesicleRDEF* solver = nullptr) override;

    void apply(const rng::RNGptr& rng,
               double dt,
               double simtime,
               double period,
               TetVesicleRDEF* solver = nullptr) override;

#if defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic pop
#endif

    ////////////////////////////////////////////////////////////////////////

    inline solver::RaftGendef* def() const noexcept {
        return pRaftGendef;
    }

    inline TriRDEF* tri() const noexcept {
        return pTri;
    }

    //////////////// ADDED FOR MPI STEPS ////////////////////

    std::vector<KProc*> const& getLocalUpdVec(int /*direction = -1*/) const override {
        return localUpdVec;
    }
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(
        int /*direction = -1*/) const override {
        return remoteUpdVec;
    }

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

    solver::RaftGendef* pRaftGendef;
    TriRDEF* pTri;

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;

    // Store the kcst for convenience
    double pKcst;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
