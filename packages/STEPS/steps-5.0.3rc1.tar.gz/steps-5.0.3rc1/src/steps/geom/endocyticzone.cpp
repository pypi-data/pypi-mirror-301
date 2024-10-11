/*
 ___license_placeholder___
 */

#include "geom/endocyticzone.hpp"

#include <algorithm>
#include <string>
#include <vector>

#include "geom/tmpatch.hpp"
#include "util/error.hpp"

namespace steps::tetmesh {

EndocyticZone::EndocyticZone(std::string const& id,
                             TmPatch& patch,
                             std::vector<index_t> const& tris)
    : pID(id)
    , pPatch(patch) {
    ArgErrLogIf(tris.empty(), "The triangle list is empty.");

    const auto& trisInside = pPatch.isTriInside(tris);
    bool allTrisInPatch =
        std::all_of(trisInside.begin(), trisInside.end(), [](bool b) { return b; });

    ArgErrLogIf(not allTrisInPatch, "Some triangles are not part of the provided patch.");

    for (auto tri: tris) {
        pTri_indices.emplace_back(tri);
    }

    pPatch._addEndocyticZone(this);
}

////////////////////////////////////////////////////////////////////////////////

EndocyticZone::~EndocyticZone() = default;

}  // namespace steps::tetmesh
