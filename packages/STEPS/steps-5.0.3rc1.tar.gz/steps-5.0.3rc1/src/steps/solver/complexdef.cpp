/*
 ___license_placeholder___
 */

#include "complexdef.hpp"

#include "model/complex.hpp"
#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

Complexdef::Complexdef(complex_global_id idx, steps::model::Complex& s)
    : pIdx(idx)
    , pNbSubStates(s.getNbSubStates())
    , pName(s.getID()) {}

////////////////////////////////////////////////////////////////////////////////

Complexdef::~Complexdef() = default;

////////////////////////////////////////////////////////////////////////////////

void Complexdef::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Complexdef::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Complexdef::setup() {
    pSetupdone = true;
}

}  // namespace steps::solver
