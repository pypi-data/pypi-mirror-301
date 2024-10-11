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
#include "math/point.hpp"
#include "solver/fwd.hpp"
#include "util/vocabulary.hpp"

namespace steps::mpi::tetvesicle {

class PointSpec {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    PointSpec(solver::spec_global_id gidx, double radius, solver::pointspec_individual_id idx);
    PointSpec(solver::spec_global_id gidx, double radius, std::fstream& cp_file);
    ~PointSpec();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);
    // Note: resoration is done by second constructor directly.

    ////////////////////////////////////////////////////////////////////////

    inline solver::pointspec_individual_id getUniqueIndex() const noexcept {
        return pIdx;
    }

    inline void setSpecIndex(solver::spec_global_id gidx) {
        pSpec_gidx = gidx;
    }

    void setPosSpherical(double theta, double phi);

    inline math::position_spherical const& getPosSpherical() const noexcept {
        return pPosSpherical;
    }

    void setPosCartesian(math::position_rel_to_ves const& pos) noexcept;

    inline math::position_rel_to_ves const& getPosCartesian() noexcept {
        return pPosCartesian;
    }

    void updatePos(double theta, double phi);

    inline void setOverlapTet_gidx(tetrahedron_global_id tet_idx) noexcept {
        pTetOverlap = tet_idx;
    }

    inline tetrahedron_global_id getOverlapTet_gidx() const noexcept {
        return pTetOverlap;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::pointspec_individual_id pIdx;

    solver::spec_global_id pSpec_gidx;

    // Positions are all held relative to centre of vesicle sphere
    math::position_spherical pPosSpherical;
    math::position_rel_to_ves pPosCartesian;

    tetrahedron_global_id pTetOverlap;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::mpi::tetvesicle
