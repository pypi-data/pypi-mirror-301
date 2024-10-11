/*
 ___license_placeholder___
 */

#pragma once

#include <string>
#include <vector>

#include "fwd.hpp"
#include "geom/fwd.hpp"
#include "solver/fwd.hpp"
#include "util/vocabulary.hpp"

namespace steps::solver {

/// Defined Raft
class EndocyticZonedef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param z Reference to the associated EndocyticZone object.
    EndocyticZonedef(Statedef& sd, tetmesh::EndocyticZone& z);

    EndocyticZonedef(const EndocyticZonedef&) = delete;
    EndocyticZonedef& operator=(const EndocyticZonedef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    /// Return the name of the raft.
    inline std::string const& name() const noexcept {
        return pName;
    }

    inline const std::vector<triangle_global_id>& tris() const noexcept {
        return pTris;
    }

  private:
    const std::string pName;
    /// Triangles
    const std::vector<triangle_global_id>& pTris;
};

}  // namespace steps::solver
