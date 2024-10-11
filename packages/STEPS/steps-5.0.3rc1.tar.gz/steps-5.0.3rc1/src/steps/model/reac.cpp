/*
 ___license_placeholder___
 */

#include "reac.hpp"

#include "spec.hpp"
#include "volsys.hpp"

#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

Reac::Reac(std::string const& id,
           Volsys& volsys,
           std::vector<Spec*> const& lhs,
           std::vector<Spec*> const& rhs,
           double kcst)
    : pID(id)
    , pModel(volsys.getModel())
    , pVolsys(volsys)
    , pOrder(0)
    , pKcst(kcst) {
    ArgErrLogIf(pKcst < 0.0, "Reaction constant can't be negative");

    setLHS(lhs);
    setRHS(rhs);

    pVolsys._handleReacAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

Reac::~Reac() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void Reac::_handleSelfDelete() {
    pVolsys._handleReacDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void Reac::setID(std::string const& id) {
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pVolsys._handleReacIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

void Reac::setLHS(std::vector<Spec*> const& lhs) {
    pLHS.clear();
    pLHS.reserve(lhs.size());

    for (auto const& l: lhs) {
        AssertLog(&l->getModel() == &pModel);
        pLHS.push_back(l);
    }
    pOrder = pLHS.size();
}

////////////////////////////////////////////////////////////////////////////////

void Reac::setRHS(std::vector<Spec*> const& rhs) {
    pRHS.clear();
    pRHS.reserve(rhs.size());

    for (auto const& r: rhs) {
        AssertLog(&r->getModel() == &pModel);
        pRHS.push_back(r);
    }
}

////////////////////////////////////////////////////////////////////////////////

void Reac::setKcst(double kcst) {
    ArgErrLogIf(kcst < 0.0, "Reaction constant can't be negative");

    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

util::flat_set<Spec*> Reac::getAllSpecs() const {
    util::flat_set<Spec*> specs;
    specs.insert(getLHS().begin(), getLHS().end());
    specs.insert(getRHS().begin(), getRHS().end());
    return specs;
}

}  // namespace steps::model
