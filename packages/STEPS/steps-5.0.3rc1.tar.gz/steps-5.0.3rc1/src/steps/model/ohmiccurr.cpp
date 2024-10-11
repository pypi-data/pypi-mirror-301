/*
 ___license_placeholder___
 */

#include "ohmiccurr.hpp"

#include "chanstate.hpp"
#include "surfsys.hpp"

#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

OhmicCurrBase::OhmicCurrBase(std::string const& id, Surfsys& surfsys, double erev, double g)
    : pID(id)
    , pModel(surfsys.getModel())
    , pSurfsys(surfsys)
    , pERev(erev)
    , pG(g) {
    ArgErrLogIf(pG < 0.0, "Channel conductance can't be negative");
}

////////////////////////////////////////////////////////////////////////////////

void OhmicCurrBase::setID(std::string const& id) {
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pSurfsys._handleOhmicCurrIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

void OhmicCurrBase::setERev(double erev) {
    pERev = erev;
}

////////////////////////////////////////////////////////////////////////////////

void OhmicCurrBase::setG(double g) {
    ArgErrLogIf(g < 0.0, "Conductance provided to OhmicCurrBase::setG function can't be negative");
    pG = g;
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

OhmicCurr::OhmicCurr(std::string const& id,
                     Surfsys& surfsys,
                     ChanState& chanstate,
                     double erev,
                     double g)
    : OhmicCurrBase(id, surfsys, erev, g)
    , pChanState(&chanstate) {
    pSurfsys._handleOhmicCurrAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

OhmicCurr::~OhmicCurr() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void OhmicCurr::_handleSelfDelete() {
    pSurfsys._handleOhmicCurrDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void OhmicCurr::setChanState(ChanState& chanstate) {
    pChanState = &chanstate;
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

ComplexOhmicCurr::ComplexOhmicCurr(std::string const& id,
                                   Surfsys& surfsys,
                                   std::string const& cplx,
                                   const std::vector<std::vector<SubunitStateFilter>>& filt,
                                   double erev,
                                   double g)
    : OhmicCurrBase(id, surfsys, erev, g)
    , pChanState(cplx, filt) {
    pSurfsys._handleComplexOhmicCurrAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::model
