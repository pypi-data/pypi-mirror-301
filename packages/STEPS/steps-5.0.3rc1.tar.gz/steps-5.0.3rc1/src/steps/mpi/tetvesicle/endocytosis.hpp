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
#include "mpi/tetvesicle/tri_vesraft.hpp"
#include "solver/endocytosisdef.hpp"

namespace steps::mpi::tetvesicle {

// Forward declarations.
class TetVesicleVesRaft;

////////////////////////////////////////////////////////////////////////////////

class Endocytosis {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Endocytosis(solver::Endocytosisdef* endodef, std::vector<TriVesRaft*>& tri);
    ~Endocytosis();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    void resetCcst();

    inline double kcst() const noexcept {
        return pKcst;
    }

    void setKcst(double k);

    inline double c() const noexcept {
        return pCcst;
    }

    inline double h() const noexcept {
        return rate() / pCcst;
    }

    inline unsigned long getExtent() const noexcept {
        return rExtent;
    }
    inline void resetExtent() noexcept {
        rExtent = 0;
        pEvents.clear();
    }

    std::vector<solver::EndocytosisEvent> getEvents();

    inline void addEvent(double time,
                         triangle_global_id tidx,
                         solver::vesicle_individual_id vidx) noexcept {
        rExtent++;
        pEvents.emplace_back(time, tidx, vidx);
    }

    inline bool active() const noexcept {
        return pActive;
    }
    inline bool inactive() const noexcept {
        return !pActive;
    }
    void setActive(bool active);

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void reset();
    double rate() const;

    void apply(TetVesicleVesRaft* solver);

    ////////////////////////////////////////////////////////////////////////

    inline solver::Endocytosisdef* endodef() const noexcept {
        return pEndocytosisdef;
    }

    inline bool inner() const noexcept {
        return endodef()->inner();
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Endocytosisdef* pEndocytosisdef;
    std::vector<TriVesRaft*> pTris;

    /// Properly scaled reaction constant.
    double pCcst;
    // Store the kcst for convenience
    double pKcst;

    unsigned long rExtent;

    std::vector<solver::EndocytosisEvent> pEvents;

    bool pActive;

    std::vector<math::point3d> pPos;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
