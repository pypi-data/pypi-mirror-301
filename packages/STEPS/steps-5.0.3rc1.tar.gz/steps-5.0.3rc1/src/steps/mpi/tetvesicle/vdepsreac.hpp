/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "math/constants.hpp"
#include "mpi/tetvesicle/kproc.hpp"
#include "mpi/tetvesicle/tri_rdef.hpp"
#include "solver/vdepsreacdef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
class TriRDEF;
class TetVesicleRDEF;

////////////////////////////////////////////////////////////////////////////////

class VDepSReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    VDepSReac(solver::VDepSReacdef* vdsrdef, TriRDEF* tri);
    VDepSReac(const VDepSReac&) = delete;
    ~VDepSReac();

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

    //////////////// ADDED FOR MPI STEPS ////////////////////

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
    TriRDEF* pTri;

    std::vector<KProc*> localUpdVec;
    std::vector<solver::kproc_global_id> remoteUpdVec;

    // The information about the size of the comaprtment or patch, and the
    // dimensions. Important for scaling the constant.
    // Volumes and areas can now change (as opposed to other solvers) by vesicle
    // occupancy so this 'constant' will be recalculated on the fly by rate()
    double pScaleFactor;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
