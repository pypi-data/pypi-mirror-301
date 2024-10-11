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
#include "mpi/tetvesicle/vesproxy.hpp"
#include "solver/exocytosisdef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
class TriRDEF;
class TetVesicleRDEF;

////////////////////////////////////////////////////////////////////////////////

class Exocytosis: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    // EXO is now per tet. So rate should be divided by number of tets for
    // consistency and multiplied by number of vesicles ??
    // Exocytosis(solver::Exocytosisdef * exodef, Vesicle *
    // vesicle); pre
    Exocytosis(solver::Exocytosisdef* exodef, TetRDEF* tet);
    ~Exocytosis();

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
        return pExocytosisdef->kcst();
    }

    inline solver::Exocytosisdef* exodef() const noexcept {
        return pExocytosisdef;
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;

    void reset() override;

#if defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Woverloaded-virtual"
#endif

    double rate(TetVesicleRDEF* solver = nullptr) override;
    void apply(const rng::RNGptr& rng,
               double dt,
               double simtime,
               double period,
               TetVesicleRDEF* solver = nullptr) override;

#if defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic pop
#endif
    //////////////// ADDED FOR MPI STEPS ////////////////////

    std::vector<KProc*> const& getLocalUpdVec(int /*direction = -1*/) const override {
        return localUpdVec;
    }
    std::vector<solver::kproc_global_id> const& getRemoteUpdVec(
        int /*direction = -1*/) const override {
        return remoteUpdVec;
    }

    void resetOccupancies() override {
        pTet->resetPoolOccupancy();
    }

    inline bool getInHost() const noexcept override {
        return pTet->getInHost();
    }

    inline int getHost() const noexcept override {
        return pTet->getHost();
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Exocytosisdef* pExocytosisdef;

    TetRDEF* pTet;

    bool pRate_zero;

    std::map<solver::vesicle_individual_id, double> pRate_per_ves;
    double pTotal_rate{};

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
