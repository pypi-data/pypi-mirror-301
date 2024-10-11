/*
 ___license_placeholder___
 */

// Standard library & STL headers.
#include <vector>

// STEPS headers.
#include "mpi/tetopsplit/comp.hpp"
#include "mpi/tetopsplit/diffboundary.hpp"
#include "solver/diffboundarydef.hpp"
#include "util/error.hpp"

// logging

namespace steps::mpi::tetopsplit {

////////////////////////////////////////////////////////////////////////////////

DiffBoundary::DiffBoundary(solver::DiffBoundarydef* dbdef)
    : pDiffBoundarydef(dbdef) {
    AssertLog(dbdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
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
    AssertLog(pSetComps);
    return pCompA;
}

////////////////////////////////////////////////////////////////////////////////

Comp* DiffBoundary::compB() {
    AssertLog(pSetComps);
    return pCompB;
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::setTetDirection(tetrahedron_global_id tet, uint direction) {
    AssertLog(direction < 4);

    pTets.push_back(tet);
    pTetDirection.push_back(direction);
}

}  // namespace steps::mpi::tetopsplit
