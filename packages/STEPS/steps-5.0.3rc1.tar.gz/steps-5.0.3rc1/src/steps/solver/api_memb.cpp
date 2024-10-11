/*
 ___license_placeholder___
 */

#include "api.hpp"

#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

void API::setMembPotential(std::string const& m, double v) {
    // the following may raise exceptions if string is unused
    membrane_global_id midx = pStatedef->getMembIdx(m);

    _setMembPotential(midx, v);
}

////////////////////////////////////////////////////////////////////////////////

void API::setMembCapac(std::string const& m, double cm) {
    // the following may raise exceptions if string is unused
    membrane_global_id midx = pStatedef->getMembIdx(m);

    _setMembCapac(midx, cm);
}

////////////////////////////////////////////////////////////////////////////////

void API::setMembVolRes(std::string const& m, double ro) {
    // the following may raise exceptions if string is unused
    membrane_global_id midx = pStatedef->getMembIdx(m);

    _setMembVolRes(midx, ro);
}

////////////////////////////////////////////////////////////////////////////////

void API::setMembRes(std::string const& m, double ro, double vrev) {
    // the following may raise exceptions if string is unused
    membrane_global_id midx = pStatedef->getMembIdx(m);

    _setMembRes(midx, ro, vrev);
}

std::pair<double, double> API::getMembRes(std::string const& m) {
    // the following may raise exceptions if string is unused
    membrane_global_id midx = pStatedef->getMembIdx(m);

    return _getMembRes(midx);
}

////////////////////////////////////////////////////////////////////////////////

void API::_setMembPotential(membrane_global_id /*midx*/, double /*v*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::_setMembCapac(membrane_global_id /*midx*/, double /*cm*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::_setMembVolRes(membrane_global_id /*midx*/, double /*ro*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::_setMembRes(membrane_global_id /*midx*/, double /*ro*/, double /*vrev*/) {
    NotImplErrLog("");
}

std::pair<double, double> API::_getMembRes(membrane_global_id /*midx*/) const {
    NotImplErrLog("");
}

}  // namespace steps::solver
