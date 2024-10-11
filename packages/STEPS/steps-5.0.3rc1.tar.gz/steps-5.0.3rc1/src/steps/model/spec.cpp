/*
 ___license_placeholder___
 */

#include "spec.hpp"

#include "model.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

Spec::Spec(std::string const& id, Model& model, int valence)
    : pID(id)
    , pModel(model)
    , pValence(valence) {
    pModel._handleSpecAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

Spec::~Spec() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void Spec::_handleSelfDelete() {
    pModel._handleSpecDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void Spec::setID(std::string const& id) {
    if (id == pID) {
        return;
    }
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pModel._handleSpecIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

void Spec::setValence(int valence) {
    pValence = valence;
}

}  // namespace steps::model
