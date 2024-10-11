/*
 ___license_placeholder___
 */

#pragma once

#include "model.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////
/// Multi-state complex reactant.
/// Component that represents a complex that can be referred to from
/// volume and surface systems.
class Complex {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Complex(std::string const& id, Model& model, const uint& nbSub, const uint& nbSt);
    virtual ~Complex();

    ////////////////////////////////////////////////////////////////////////
    // COMPLEX PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    const std::string& getID() const noexcept {
        return pID;
    }

    Model& getModel() const noexcept {
        return pModel;
    }

    unsigned int getNbSubStates() const noexcept {
        return pnbSubStates;
    }

    unsigned int getNbSubUnits() const noexcept {
        return pnbSubunits;
    }

  private:
    const std::string pID;
    Model& pModel;
    const unsigned int pnbSubunits;
    const unsigned int pnbSubStates;
};

}  // namespace steps::model
