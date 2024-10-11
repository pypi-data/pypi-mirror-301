/*
 ___license_placeholder___
 */

#include "solver/complexreacdef.hpp"

#include "geom/comp.hpp"
#include "model/complexreac.hpp"
#include "model/spec.hpp"
#include "solver/compdef.hpp"
#include "solver/statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

ComplexReacdef::ComplexReacdef(Statedef& sd,
                               complexreac_global_id idx,
                               steps::model::ComplexReac& r)
    : pStatedef(sd)
    , pIdx(idx)
    , pName(r.getID())
    , pOrder(r.getOrder())
    , pKcst(r.getKcst())
    , pLhs(r.getLHS())
    , pRhs(r.getRHS()) {
    // Copy complex events
    for (auto* ev: r.getUPDEvents()) {
        pComplexUPDEvs.push_back(std::make_unique<ComplexUpdateEventdef>(*ev, sd));
    }
    for (auto* ev: r.getDELEvents()) {
        pComplexDELEvs.push_back(std::make_unique<ComplexDeleteEventdef>(*ev, sd));
    }
    for (auto* ev: r.getCREEvents()) {
        pComplexCREEvs.push_back(std::make_unique<ComplexCreateEventdef>(*ev, sd));
    }

    uint nspecs = pStatedef.countSpecs();
    pSpec_DEP.container().resize(nspecs, DEP_NONE);
    pSpec_LHS.container().resize(nspecs);
    pSpec_RHS.container().resize(nspecs);
    pSpec_UPD.container().resize(nspecs);
}

////////////////////////////////////////////////////////////////////////////////

void ComplexReacdef::checkpoint(std::fstream& /*cp_file*/) const {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void ComplexReacdef::restore(std::fstream& /*cp_file*/) {
    // Reserve
}

////////////////////////////////////////////////////////////////////////////////

void ComplexReacdef::setup() {
    AssertLog(pSetupdone == false);

    // first copy the information about the reaction stoichiometry from ComplexReac object
    for (auto const& l: pLhs) {
        spec_global_id sidx = pStatedef.getSpecIdx(*l);
        pSpec_LHS[sidx] += 1;
    }
    for (auto const& r: pRhs) {
        spec_global_id sidx = pStatedef.getSpecIdx(*r);
        pSpec_RHS[sidx] += 1;
    }

    // Now set up the update vector
    for (auto i: pSpec_LHS.range()) {
        const auto lhs = static_cast<int>(pSpec_LHS[i]);
        const auto rhs = static_cast<int>(pSpec_RHS[i]);
        const int aux = pSpec_UPD[i] = (rhs - lhs);
        if (lhs != 0) {
            pSpec_DEP[i] |= DEP_STOICH;
        }
        if (aux != 0) {
            pSpec_UPD_Coll.emplace_back(i);
        }
    }

    // set up deps for complexes
    for (const auto& upd: pComplexUPDEvs) {
        pComplex_DEPMAP[upd->complexIdx()].merge(upd->getDepSet());
        pComplex_UPDMAP[upd->complexIdx()].merge(upd->getUpdSet());
    }
    for (const auto& del: pComplexDELEvs) {
        pComplex_DEPMAP[del->complexIdx()].merge(del->getDepSet());
        pComplex_UPDMAP[del->complexIdx()].merge(del->getUpdSet());
    }
    for (const auto& cre: pComplexCREEvs) {
        pComplex_UPDMAP[cre->complexIdx()].merge(cre->getUpdSet());
    }
    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

uint ComplexReacdef::lhs(spec_global_id gidx) const {
    AssertLog(gidx < pStatedef.countSpecs());
    return pSpec_LHS[gidx];
}

////////////////////////////////////////////////////////////////////////////////

int ComplexReacdef::dep(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    AssertLog(gidx < pStatedef.countSpecs());
    return pSpec_DEP[gidx];
}

////////////////////////////////////////////////////////////////////////////////

bool ComplexReacdef::complexdep(complex_global_id gidx, complex_substate_id sus) const {
    AssertLog(pSetupdone == true);
    AssertLog(gidx < pStatedef.countComplexes());
    const auto it = pComplex_DEPMAP.find(gidx);
    if (it == pComplex_DEPMAP.end()) {
        return false;
    } else {
        return it->second.find(sus) != it->second.end();
    }
}

////////////////////////////////////////////////////////////////////////////////

uint ComplexReacdef::rhs(spec_global_id gidx) const {
    AssertLog(gidx < pStatedef.countSpecs());
    return pSpec_RHS[gidx];
}

////////////////////////////////////////////////////////////////////////////////

int ComplexReacdef::upd(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    AssertLog(gidx < pStatedef.countSpecs());
    return pSpec_UPD[gidx];
}

////////////////////////////////////////////////////////////////////////////////

bool ComplexReacdef::reqspec(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    AssertLog(gidx < pStatedef.countSpecs());
    if (pSpec_DEP[gidx] != DEP_NONE) {
        return true;
    }
    if (pSpec_RHS[gidx] != 0) {
        return true;
    }
    return false;
}

}  // namespace steps::solver
