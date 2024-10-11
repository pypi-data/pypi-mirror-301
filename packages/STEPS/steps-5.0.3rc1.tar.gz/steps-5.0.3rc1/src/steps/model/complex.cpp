/*
 ___license_placeholder___
 */

#include "complex.hpp"

#include "model.hpp"

namespace steps::model {

Complex::Complex(std::string const& id, Model& model, const uint& nbSub, const uint& nbSt)
    : pID(id)
    , pModel(model)
    , pnbSubunits(nbSub)
    , pnbSubStates(nbSt) {
    pModel._handleComplexAdd(*this);
}

////////////////////////////////////////////////////////////////////////////////

Complex::~Complex() {
    pModel._handleComplexDel(*this);
}

}  // namespace steps::model
