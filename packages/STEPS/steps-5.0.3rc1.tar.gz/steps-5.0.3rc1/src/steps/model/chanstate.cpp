/*
 ___license_placeholder___
 */

#include "chanstate.hpp"

#include "chan.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

ChanState::ChanState(std::string const& id, Model& model, Chan& chan)
    : Spec(id, model)
    , pChan(chan) {
    pChan._handleChanStateAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

ChanState::~ChanState() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void ChanState::_handleSelfDelete() {
    // Base method
    Spec::_handleSelfDelete();

    pChan._handleChanStateDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void ChanState::setID(std::string const& id) {
    if (id == getID()) {
        return;
    }
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pChan._handleChanStateIDChange(getID(), id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    Spec::setID(id);
}

}  // namespace steps::model
