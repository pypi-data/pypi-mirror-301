/*
 ___license_placeholder___
 */

#include "model/raftsreac.hpp"

#include "model/raftsys.hpp"
#include "model/spec.hpp"
#include "util/error.hpp"

////////////////////////////////////////////////////////////////////////////////

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////

RaftSReac::RaftSReac(std::string const& id,
                     Raftsys& raftsys,
                     std::vector<Spec*> const& ilhs,
                     std::vector<Spec*> const& olhs,
                     std::vector<Spec*> const& slhs,
                     std::vector<Spec*> const& rslhs,
                     std::vector<Spec*> const& rsrhs,
                     std::vector<Spec*> const& srhs,
                     std::vector<Spec*> const& orhs,
                     std::vector<Spec*> const& irhs,
                     std::vector<Spec*> const& rsdeps,
                     std::vector<Spec*> const& anti_rsdeps,
                     double kcst,
                     Immobilization immobilization)
    : pID(id)
    , pModel(raftsys.getModel())
    , pRaftsys(raftsys)
    , pImmobilization(immobilization)
    , pOuter(true)
    , pOrder(0)
    , pKcst(kcst) {
    if (pKcst < 0.0) {
        std::ostringstream os;
        os << "Raft surface reaction constant can't be negative";
        ArgErrLog(os.str());
    }

    // Can't have species on the lhs in the inner and outer compartment
    if (olhs.size() != 0 && ilhs.size() != 0) {
        std::ostringstream os;
        os << "Reactant species cannot consist of both ilhs and olhs species.";
        ArgErrLog(os.str());
    }

    if (!olhs.empty()) {
        setOLHS(olhs);
    }
    if (!ilhs.empty()) {
        setILHS(ilhs);
    }
    setSLHS(slhs);
    setRsLHS(rslhs);
    setRsRHS(rsrhs);
    setSRHS(srhs);
    setORHS(orhs);
    setIRHS(irhs);
    setRsDeps(rsdeps);
    setAntiRsDeps(anti_rsdeps);

    pRaftsys._handleRaftSReacAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

RaftSReac::~RaftSReac() {
    _handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::_handleSelfDelete() {
    pRaftsys._handleRaftSReacDel(*this);
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setID(std::string const& id) {
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pRaftsys._handleRaftSReacIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setILHS(std::vector<Spec*> const& ilhs) {
    if (pOLHS.size() != 0) {
        CLOG(WARNING, "general_log") << "Removing outer compartment species from "
                                        "lhs stoichiometry for RaftSReac "
                                     << getID() << ".\n";
        pOLHS.clear();
    }

    pILHS.clear();

    for (auto const& il: ilhs) {
        AssertLog(&il->getModel() == &pModel);
        pILHS.push_back(il);
    }
    pOuter = false;
    pOrder = pILHS.size() + pRsLHS.size() + pSLHS.size();
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setOLHS(std::vector<Spec*> const& olhs) {
    if (pILHS.size() != 0) {
        CLOG(WARNING, "general_log") << "Removing inner compartment species from "
                                        "lhs stoichiometry for RaftSReac "
                                     << getID() << ".\n";
        pILHS.clear();
    }

    for (auto const& ol: olhs) {
        AssertLog(&ol->getModel() == &pModel);
    }
    pOLHS = olhs;

    pOuter = true;
    pOrder = pOLHS.size() + pSLHS.size() + pRsLHS.size();
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setRsLHS(std::vector<Spec*> const& rslhs) {
    for (auto const& rsl: rslhs) {
        AssertLog(&rsl->getModel() == &pModel);
    }
    pRsLHS = rslhs;

    if (pOuter) {
        pOrder = pOLHS.size() + pSLHS.size() + pRsLHS.size();
    } else {
        pOrder = pILHS.size() + pRsLHS.size() + pSLHS.size();
    }
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setSLHS(std::vector<Spec*> const& slhs) {
    for (auto const& sl: slhs) {
        AssertLog(&sl->getModel() == &pModel);
    }
    pSLHS = slhs;


    if (pOuter) {
        pOrder = pOLHS.size() + pSLHS.size() + pRsLHS.size();
    } else {
        pOrder = pILHS.size() + pRsLHS.size() + pSLHS.size();
    }
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setRsRHS(std::vector<Spec*> const& rsrhs) {
    for (auto const& rsr: rsrhs) {
        AssertLog(&rsr->getModel() == &pModel);
    }
    pRsRHS = rsrhs;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setSRHS(std::vector<Spec*> const& srhs) {
    for (auto const& sr: srhs) {
        AssertLog(&sr->getModel() == &pModel);
    }
    pSRHS = srhs;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setORHS(std::vector<Spec*> const& orhs) {
    for (auto const& ors: orhs) {
        AssertLog(&ors->getModel() == &pModel);
    }
    pORHS = orhs;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setIRHS(std::vector<Spec*> const& irhs) {
    for (auto const& irs: irhs) {
        AssertLog(&irs->getModel() == &pModel);
    }
    pIRHS = irhs;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setRsDeps(std::vector<Spec*> const& rsdeps) {
    for (auto const& rsd: rsdeps) {
        AssertLog(&rsd->getModel() == &pModel);
    }
    pRsDeps = rsdeps;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setAntiRsDeps(std::vector<Spec*> const& anti_rsdeps) {
    for (auto const& arsd: anti_rsdeps) {
        AssertLog(&arsd->getModel() == &pModel);
    }
    pAntiRsDeps = anti_rsdeps;
}

////////////////////////////////////////////////////////////////////////////////

void RaftSReac::setKcst(double kcst) {
    if (kcst < 0.0) {
        std::ostringstream os;
        os << "Surface reaction constant can't be negative";
        ArgErrLog(os.str());
    }
    pKcst = kcst;
}

////////////////////////////////////////////////////////////////////////////////

util::flat_set<Spec*> RaftSReac::getAllSpecs() const {
    util::flat_set<Spec*> specs;
    specs.insert(getILHS().begin(), getILHS().end());
    specs.insert(getOLHS().begin(), getOLHS().end());
    specs.insert(getRsLHS().begin(), getRsLHS().end());
    specs.insert(getSLHS().begin(), getSLHS().end());
    specs.insert(getRsRHS().begin(), getRsRHS().end());
    specs.insert(getSRHS().begin(), getSRHS().end());
    specs.insert(getORHS().begin(), getORHS().end());
    specs.insert(getIRHS().begin(), getIRHS().end());
    return specs;
}

}  // namespace steps::model
