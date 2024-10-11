/*
 ___license_placeholder___
 */

#include "model/linkspec.hpp"

#include "model.hpp"
#include "util/error.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

LinkSpec::LinkSpec(std::string const& id, Model& model, double dcst)
    : pID(id)
    , pModel(model) {
    if (dcst < 0.0) {
        std::ostringstream os;
        os << "Diffusion coefficient must not be negative!";
        ArgErrLog(os.str());
    }

    pDcst = dcst;

    pModel._handleLinkSpecAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

LinkSpec::~LinkSpec() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void LinkSpec::_handleSelfDelete() {
    pModel._handleLinkSpecDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void LinkSpec::setID(std::string const& id) {
    if (id == pID) {
        return;
    }
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pModel._handleLinkSpecIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

}  // namespace steps::model
