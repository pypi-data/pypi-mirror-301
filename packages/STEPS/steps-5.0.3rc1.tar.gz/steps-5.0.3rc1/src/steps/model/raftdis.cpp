/*
 ___license_placeholder___
 */

#include "model/raftdis.hpp"

#include "model/raftsys.hpp"
#include "model/spec.hpp"
#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

RaftDis::RaftDis(std::string const& id,
                 Raftsys& raftsys,
                 std::vector<Spec*> const& spec_signature,
                 double kcst)
    : pID(id)
    , pModel(raftsys.getModel())
    , pRaftsys(raftsys)
    , pKcst(kcst) {
    if (spec_signature.empty()) {
        std::ostringstream os;
        os << "No species signature provided to RaftDis initializer function";
        ArgErrLog(os.str());
    }

    if (pKcst < 0.0) {
        std::ostringstream os;
        os << "RaftDis rate can't be negative";
        ArgErrLog(os.str());
    }

    pSpecSignature.reserve(spec_signature.size());
    for (auto const& sig: spec_signature) {
        AssertLog(&sig->getModel() == &pModel);
        pSpecSignature.push_back(sig);
    }

    pRaftsys._handleRaftDisAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

RaftDis::~RaftDis() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void RaftDis::_handleSelfDelete() {
    pRaftsys._handleRaftDisDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void RaftDis::setKcst(double kcst) {
    if (kcst < 0.0) {
        std::ostringstream os;
        os << "RaftDis rate can't be negative";
        ArgErrLog(os.str());
    }

    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

void RaftDis::setID(std::string const& id) {
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pRaftsys._handleRaftDisIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

util::flat_set<Spec*> RaftDis::getAllSpecs() const {
    util::flat_set<Spec*> specs;
    specs.insert(getSpecSignature().begin(), getSpecSignature().end());
    return specs;
}

}  // namespace steps::model
