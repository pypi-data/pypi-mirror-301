/*
 ___license_placeholder___
 */

// STEPS headers.
#include "diffboundary.hpp"
#include "comp.hpp"

// logging
#include "util/error.hpp"

namespace steps::tetexact {

DiffBoundary::DiffBoundary(solver::DiffBoundarydef* dbdef)
    : pDiffBoundarydef(dbdef) {
    AssertLog(dbdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

DiffBoundary::~DiffBoundary() = default;

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
    // NOTE setTetDirection() is called during Tetexact::setup()
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::setComps(Comp* compa, Comp* compb) {
    AssertLog(pSetComps == false);
    AssertLog(compa != nullptr);
    AssertLog(compb != nullptr);
    AssertLog(compa != compb);

    pCompA = compa;
    pCompB = compb;
    pSetComps = true;
}

////////////////////////////////////////////////////////////////////////////////

Comp* DiffBoundary::compA() {
    AssertLog(pSetComps == true);
    return pCompA;
}

////////////////////////////////////////////////////////////////////////////////

Comp* DiffBoundary::compB() {
    AssertLog(pSetComps == true);
    return pCompB;
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::setTetDirection(tetrahedron_global_id tet, uint direction) {
    AssertLog(direction < 4);

    pTets.push_back(tet);
    pTetDirection.push_back(direction);
}

}  // namespace steps::tetexact
