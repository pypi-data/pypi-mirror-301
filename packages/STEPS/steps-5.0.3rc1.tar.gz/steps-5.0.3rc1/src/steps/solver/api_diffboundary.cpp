/*
 ___license_placeholder___
 */

#include "api.hpp"

#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

////////////////////////////////////////////////////////////////////////////////

void API::setDiffBoundarySpecDiffusionActive(std::string const& db,
                                             std::string const& s,
                                             bool act) {
    diffboundary_global_id dbidx = pStatedef->getDiffBoundaryIdx(db);
    spec_global_id sidx = pStatedef->getSpecIdx(s);

    return _setDiffBoundarySpecDiffusionActive(dbidx, sidx, act);
}

////////////////////////////////////////////////////////////////////////////////

bool API::getDiffBoundarySpecDiffusionActive(std::string const& db, std::string const& s) const {
    diffboundary_global_id dbidx = pStatedef->getDiffBoundaryIdx(db);
    spec_global_id sidx = pStatedef->getSpecIdx(s);

    return _getDiffBoundarySpecDiffusionActive(dbidx, sidx);
}

////////////////////////////////////////////////////////////////////////////////

void API::setDiffBoundarySpecDcst(std::string const& db,
                                  std::string const& s,
                                  double dcst,
                                  std::string const& direction_comp) {
    diffboundary_global_id dbidx = pStatedef->getDiffBoundaryIdx(db);
    spec_global_id sidx = pStatedef->getSpecIdx(s);
    if (direction_comp.empty()) {
        _setDiffBoundarySpecDcst(dbidx, sidx, dcst);
    } else {
        comp_global_id cidx = pStatedef->getCompIdx(direction_comp);
        _setDiffBoundarySpecDcst(dbidx, sidx, dcst, cidx);
    }
}

////////////////////////////////////////////////////////////////////////////////

void API::_setDiffBoundarySpecDiffusionActive(diffboundary_global_id /*dbidx*/,
                                              spec_global_id /*sidx*/,
                                              bool /*act*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

bool API::_getDiffBoundarySpecDiffusionActive(diffboundary_global_id /*dbidx*/,
                                              spec_global_id /*sidx*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::_setDiffBoundarySpecDcst(diffboundary_global_id /*dbidx*/,
                                   spec_global_id /*sidx*/,
                                   double /*dcst*/,
                                   comp_global_id /*direction_comp*/) {
    NotImplErrLog("");
}

}  // namespace steps::solver
