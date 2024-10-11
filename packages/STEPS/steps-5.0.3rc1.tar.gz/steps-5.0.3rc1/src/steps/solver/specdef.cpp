/*
 ___license_placeholder___
 */

#include "specdef.hpp"

#include "model/spec.hpp"

namespace steps::solver {

Specdef::Specdef(Statedef&, spec_global_id idx, model::Spec& s)
    : pIdx(idx)
    , pName(s.getID()) {}

////////////////////////////////////////////////////////////////////////////////

void Specdef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Specdef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Specdef::setup(const Statedef&) {
    pSetupdone = true;
}

}  // namespace steps::solver
