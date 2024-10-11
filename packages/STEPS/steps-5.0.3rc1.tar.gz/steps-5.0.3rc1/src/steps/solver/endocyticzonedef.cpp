/*
 ___license_placeholder___
 */

#include "endocyticzonedef.hpp"

#include "geom/endocyticzone.hpp"

namespace steps::solver {

EndocyticZonedef::EndocyticZonedef(Statedef&, tetmesh::EndocyticZone& z)
    : pName(z.getID())
    , pTris(z.getAllTriIndices()) {}

////////////////////////////////////////////////////////////////////////////////

void EndocyticZonedef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void EndocyticZonedef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

}  // namespace steps::solver
