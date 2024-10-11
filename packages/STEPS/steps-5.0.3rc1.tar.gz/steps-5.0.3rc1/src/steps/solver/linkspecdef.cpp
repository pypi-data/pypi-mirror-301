/*
 ___license_placeholder___
 */

#include "linkspecdef.hpp"

#include "model/linkspec.hpp"

namespace steps::solver {

LinkSpecdef::LinkSpecdef(Statedef&, linkspec_global_id idx, model::LinkSpec& l)
    : pIdx(idx)
    , pName(l.getID())
    , pDcst(l.getDcst()) {}

////////////////////////////////////////////////////////////////////////////////

void LinkSpecdef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void LinkSpecdef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void LinkSpecdef::setup(const Statedef&) {
    pSetupdone = true;
}

}  // namespace steps::solver
