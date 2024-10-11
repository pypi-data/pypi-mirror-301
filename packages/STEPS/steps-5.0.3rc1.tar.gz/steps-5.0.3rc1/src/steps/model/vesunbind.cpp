/*
 ___license_placeholder___
 */

#include "vesunbind.hpp"

#include "linkspec.hpp"
#include "spec.hpp"
#include "vesicle.hpp"
#include "volsys.hpp"

#include "util/error.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

VesUnbind::VesUnbind(std::string const& id,
                     Volsys& volsys,
                     LinkSpec& link1,
                     LinkSpec& link2,
                     Vesicle& vesicle1,
                     Spec& product1,
                     Vesicle& vesicle2,
                     Spec& product2,
                     double kcst,
                     Immobilization immobilization)
    : pID(id)
    , pModel(volsys.getModel())
    , pVolsys(volsys)
    , pKcst(kcst)
    , pImmobilization(immobilization) {
    if (pKcst < 0.0) {
        std::ostringstream os;
        os << "Vesicle binding constant can't be negative";
        ArgErrLog(os.str());
    }

    if (pImmobilization == IMMOBILIZING) {
        std::ostringstream os;
        os << "Unsupported immobilization flag. A VesUnBind event cannot immobilize vesicles.";
        ArgErrLog(os.str());
    }

    AssertLog(&product1.getModel() == &pModel);
    AssertLog(&product2.getModel() == &pModel);

    pProducts1 = std::make_pair(&vesicle1, &product1);
    pProducts2 = std::make_pair(&vesicle2, &product2);

    AssertLog(&link1.getModel() == &pModel);
    AssertLog(&link2.getModel() == &pModel);

    pLinks1 = std::make_pair(&vesicle1, &link1);
    pLinks2 = std::make_pair(&vesicle2, &link2);

    pVolsys._handleVesUnbindAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

VesUnbind::~VesUnbind() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void VesUnbind::_handleSelfDelete() {
    pVolsys._handleVesUnbindDel(*this);
    pKcst = 0.0;
}

////////////////////////////////////////////////////////////////////////////////

void VesUnbind::setID(std::string const& id) {
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pVolsys._handleVesUnbindIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

void VesUnbind::setKcst(double kcst) {
    if (kcst < 0.0) {
        std::ostringstream os;
        os << "Vesicle unbinding rate constant can't be negative";
        ArgErrLog(os.str());
    }
    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

std::vector<Spec*> VesUnbind::getAllSpecs() const {
    std::vector<Spec*> specs;

    specs.emplace_back(pProducts1.second);

    if (specs[0] != pProducts2.second) {
        specs.emplace_back(pProducts2.second);
    }
    return specs;
}

}  // namespace steps::model
