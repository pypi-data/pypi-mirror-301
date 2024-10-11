/*
 ___license_placeholder___
 */

#include "model/raft.hpp"

#include "model/model.hpp"
#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

Raft::Raft(std::string const& id, Model& model, double diameter, double dcst)
    : pID(id)
    , pModel(model)
    , pDiameter(diameter)
    , pDcst(dcst) {
    if (pDcst < 0.0) {
        std::ostringstream os;
        os << "Raft diffusion constant can't be negative";
        ArgErrLog(os.str());
    }

    pModel._handleRaftAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

Raft::~Raft() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void Raft::_handleSelfDelete() {
    pModel._handleRaftDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void Raft::addRaftsys(std::string const& id) {
    // string identifier is only added to set if it is not already included
    pRaftsys.insert(id);
}

////////////////////////////////////////////////////////////////////////////////

void Raft::setDcst(double dcst) {
    if (dcst < 0.0) {
        std::ostringstream os;
        os << "Raft Diffusion constant can't be negative";
        ArgErrLog(os.str());
    }
    pDcst = dcst;
}

////////////////////////////////////////////////////////////////////////////////

void Raft::setID(std::string const& id) {
    if (id == pID) {
        return;
    }
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pModel._handleRaftIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

}  // namespace steps::model
