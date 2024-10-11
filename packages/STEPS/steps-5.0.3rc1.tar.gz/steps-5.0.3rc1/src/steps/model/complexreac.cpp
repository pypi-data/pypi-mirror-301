/*
 ___license_placeholder___
 */

#include "model/complexreac.hpp"

#include "model/model.hpp"
#include "model/spec.hpp"
#include "model/volsys.hpp"
#include "util/error.hpp"

namespace steps::model {

ComplexReac::ComplexReac(std::string const& id,
                         Volsys& volsys,
                         std::vector<Spec*> const& lhs,
                         std::vector<Spec*> const& rhs,
                         std::vector<ComplexEvent*> const& compEvs,
                         double kcst)
    : pID(id)
    , pModel(volsys.getModel())
    , pVolsys(volsys)
    , pLHS(lhs)
    , pRHS(rhs) {
    setKcst(kcst);

    for (auto const& l: pLHS) {
        AssertLog(&l->getModel() == &pModel);
    }
    for (auto const& r: pRHS) {
        AssertLog(&r->getModel() == &pModel);
    }

    pOrder = pLHS.size();

    for (auto* ev: compEvs) {
        if (auto* upd = dynamic_cast<ComplexUpdateEvent*>(ev)) {
            pCompUPD.push_back(upd);
            ++pOrder;
        } else if (auto* del = dynamic_cast<ComplexDeleteEvent*>(ev)) {
            pCompDEL.push_back(del);
            ++pOrder;
        } else if (auto* cre = dynamic_cast<ComplexCreateEvent*>(ev)) {
            pCompCRE.push_back(cre);
        }
    }

    pVolsys._handleComplexReacAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

void ComplexReac::setKcst(double kcst) {
    ArgErrLogIf(kcst < 0.0, "Reaction constant can't be negative");
    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

util::flat_set<Spec*> ComplexReac::getAllSpecs() const {
    util::flat_set<Spec*> specSet;
    specSet.insert(pLHS.begin(), pLHS.end());
    specSet.insert(pRHS.begin(), pRHS.end());
    return specSet;
}

}  // namespace steps::model
