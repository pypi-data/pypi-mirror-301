/*
 ___license_placeholder___
 */

#include "model/vesicle.hpp"

#include "model/model.hpp"
#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

Vesicle::Vesicle(std::string const& id, Model& model, double diameter, double dcst)
    : pID(id)
    , pModel(model)
    , pDiameter(diameter)
    , pDcst(dcst) {
    if (pDcst < 0.0) {
        std::ostringstream os;
        os << "Vesicle diffusion constant can't be negative";
        ArgErrLog(os.str());
    }
    pModel._handleVesicleAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

Vesicle::~Vesicle() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void Vesicle::_handleSelfDelete() {
    pModel._handleVesicleDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void Vesicle::addVesSurfsys(std::string const& id) {
    // string identifier is only added to set if it is not already included
    pVesSurfsys.insert(id);
}

////////////////////////////////////////////////////////////////////////////////

void Vesicle::setDcst(double dcst) {
    if (dcst < 0.0) {
        std::ostringstream os;
        os << "Vesicle diffusion constant can't be negative";
        ArgErrLog(os.str());
    }
    pDcst = dcst;
}

////////////////////////////////////////////////////////////////////////////////

void Vesicle::setID(std::string const& id) {
    if (id == pID) {
        return;
    }
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pModel._handleVesicleIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

}  // namespace steps::model
