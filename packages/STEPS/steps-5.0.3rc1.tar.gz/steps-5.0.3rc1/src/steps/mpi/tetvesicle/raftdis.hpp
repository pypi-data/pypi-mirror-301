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
#include "mpi/tetvesicle/raft.hpp"
#include "solver/raftdisdef.hpp"

namespace steps::mpi::tetvesicle {

////////////////////////////////////////////////////////////////////////////////

class RaftDis {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    RaftDis(solver::RaftDisdef* rddef, Raft* raft);
    RaftDis(solver::RaftDisdef* rddef, Raft* raft, std::fstream& cp_file);
    ~RaftDis();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    inline double kcst() const noexcept {
        return pKcst;
    }
    void setKcst(double k);

    inline unsigned long getExtent() const noexcept {
        return rExtent;
    }
    inline void resetExtent() noexcept {
        rExtent = 0;
    }

    inline bool active() const noexcept {
        return pActive;
    }
    inline bool inactive() const noexcept {
        return !pActive;
    }
    void setActive(bool active) noexcept {
        pActive = active;
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() {
        return;
    };

    void reset();

    double rate();

    void apply();

    ////////////////////////////////////////////////////////////////////////

    inline solver::RaftDisdef* def() const noexcept {
        return pRaftDisdef;
    }

    inline Raft* raft() const noexcept {
        return pRaft;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::RaftDisdef* pRaftDisdef;
    Raft* pRaft;

    // Store the kcst for convenience
    double pKcst;

    unsigned long rExtent;

    bool pActive;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
