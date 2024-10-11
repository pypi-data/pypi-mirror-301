/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/diffboundary.hpp"

// STEPS headers.
#include "mpi/tetvesicle/comp_rdef.hpp"
#include "solver/diffboundarydef.hpp"

namespace steps::mpi::tetvesicle {

DiffBoundary::DiffBoundary(solver::DiffBoundarydef* dbdef)
    : pDiffBoundarydef(dbdef)
    , pSetComps(false)
    , pCompA(nullptr)
    , pCompB(nullptr) {
    AssertLog(dbdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

DiffBoundary::~DiffBoundary() = default;

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::setComps(CompRDEF* compa, CompRDEF* compb) {
    AssertLog(pSetComps == false);
    AssertLog(compa != nullptr);
    AssertLog(compb != nullptr);
    AssertLog(compa != compb);

    pCompA = compa;
    pCompB = compb;
    pSetComps = true;
}

////////////////////////////////////////////////////////////////////////////////

CompRDEF* DiffBoundary::compA() {
    AssertLog(pSetComps == true);
    return pCompA;
}

////////////////////////////////////////////////////////////////////////////////

CompRDEF* DiffBoundary::compB() {
    AssertLog(pSetComps == true);
    return pCompB;
}

////////////////////////////////////////////////////////////////////////////////

void DiffBoundary::setTetDirection(tetrahedron_global_id tet, uint direction) {
    AssertLog(direction < 4);

    pTets.push_back(tet);
    pTetDirection.push_back(direction);
}

}  // namespace steps::mpi::tetvesicle
