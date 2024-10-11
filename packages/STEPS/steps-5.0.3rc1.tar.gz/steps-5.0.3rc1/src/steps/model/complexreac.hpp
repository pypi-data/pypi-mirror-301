/*
 ___license_placeholder___
 */

#pragma once

#include <string>
#include <vector>

#include "fwd.hpp"
#include "model/complexevents.hpp"
#include "util/collections.hpp"
#include "util/common.hpp"

namespace steps::model {

////////////////////////////////////////////////////////////////////////////////
/// Complex Reaction in a volume system.
///
/// A complex kinetic reaction is specified by:
///     - Species appearing on the left hand side of the reaction (lhs).
///     - Species appearing on the right hand side of the reaction (rhs).
///     - Complex events happening during the reaction.
///     - Rate constant for the reaction (kcst).

class ComplexReac {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the reaction.
    /// \param volsys Pointer to the parent volume system.
    /// \param lhs Vector of pointers to the species on the left hand side of the reaction.
    /// \param rhs Vector of pointers to the species on the right hand side of the reaction.
    /// \param kcst Rate constant for the reaction.
    ComplexReac(std::string const& id,
                Volsys& volsys,
                std::vector<Spec*> const& lhs = {},
                std::vector<Spec*> const& rhs = {},
                std::vector<ComplexEvent*> const& compEvs = {},
                double kcst = 0.0);

    ~ComplexReac() = default;

    ////////////////////////////////////////////////////////////////////////
    // REACTION RULE PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    std::string getID() const noexcept {
        return pID;
    }

    Volsys& getVolsys() const noexcept {
        return pVolsys;
    }

    Model& getModel() const noexcept {
        return pModel;
    }

    const std::vector<ComplexUpdateEvent*>& getUPDEvents() const noexcept {
        return pCompUPD;
    }

    const std::vector<ComplexDeleteEvent*>& getDELEvents() const noexcept {
        return pCompDEL;
    }

    const std::vector<ComplexCreateEvent*>& getCREEvents() const noexcept {
        return pCompCRE;
    }

    ////////////////////////////////////////////////////////////////////////
    // OPERATIONS (EXPOSED TO PYTHON)
    ////////////////////////////////////////////////////////////////////////

    const std::vector<Spec*>& getLHS() const noexcept {
        return pLHS;
    }

    const std::vector<Spec*>& getRHS() const noexcept {
        return pRHS;
    }

    /// Return all species involved in the reaction.
    util::flat_set<Spec*> getAllSpecs() const;

    /// Return the order of the reaction.
    uint getOrder() const noexcept {
        return pOrder;
    }

    /// Return the rate constant of the reaction.
    double getKcst() const noexcept {
        return pKcst;
    }

    /// Set or reset the rate constant of the reaction.
    void setKcst(double kcst);

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    const std::string pID;
    Model& pModel;
    Volsys& pVolsys;

    const std::vector<Spec*> pLHS;
    const std::vector<Spec*> pRHS;
    std::vector<ComplexUpdateEvent*> pCompUPD;
    std::vector<ComplexDeleteEvent*> pCompDEL;
    std::vector<ComplexCreateEvent*> pCompCRE;
    uint pOrder{};
    double pKcst{};
};

inline bool operator<(const ComplexReac& lhs, const ComplexReac& rhs) {
    return lhs.getID() < rhs.getID();
}

}  // namespace steps::model
