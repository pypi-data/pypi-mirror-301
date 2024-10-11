/*
 ___license_placeholder___
 */

#pragma once

#include <map>
#include <string>
#include <vector>

#include "fwd.hpp"

namespace steps::model {

/// Exocytosis.
///
/// A specific type of interaction that models Exocytosis of a vesicle
///
/// \warning Methods start with an underscore are not exposed to Python.
class Exocytosis {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the exocytotic reaction.
    /// \param vessurfsys Reference to the parent vesicle surface system.
    /// \param spec_deps Species dependency for exocytosis on the vesicle surface
    /// \param raft Optional creation of raft on surface upon exocytosis event.
    /// \param kcst Rate constant of the exocytosis 'reaction'.
    ///
    Exocytosis(std::string const& id,
               VesSurfsys& vessurfsys,
               std::vector<Spec*> const& spec_deps = {},
               Raft* raft = nullptr,
               double kcst = 0.0,
               bool kiss_and_run = false,
               std::map<Spec*, Spec*> const& kiss_and_run_spec_changes = {},
               double kiss_and_run_partial_release = 1.0);

    Exocytosis(const Exocytosis&) = delete;
    Exocytosis& operator=(const Exocytosis&) = delete;

    /// Destructor
    ~Exocytosis();

    ////////////////////////////////////////////////////////////////////////
    // EXOCYTOSIS PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    /// Return the surface reaction rule ID.
    ///
    /// \return ID of the surface reaction.
    inline const std::string& getID() const noexcept {
        return pID;
    }

    /// Set or change the surface reaction rule ID.
    ///
    /// \param id ID of the surface reaction.
    void setID(std::string const& id);

    /// Return a reference to the parent vesicle surface system.
    ///
    /// \return Reference to the vesicle surface system.
    inline VesSurfsys& getVesSurfsys() const noexcept {
        return pVesSurfsys;
    }

    /// Return a reference to the parent model.
    ///
    /// \return Reference to the parent model.
    inline Model& getModel() const noexcept {
        return pModel;
    }

    /// Return a pointer to the created Raft.
    ///
    /// \return Pointer to the raft.
    inline Raft* getRaft() const noexcept {
        return pRaft;
    }

    /// Return if this is a kiss-and-run or not.
    ///
    /// \return Bool.
    inline bool getKissAndRun() const noexcept {
        return pKissAndRun;
    }

    /// Return species that will be transfered from vesicle to membrane upon kiss-n-run.
    ///
    /// \return Vector of species.
    inline const std::map<Spec*, Spec*>& getKissAndRunSpecChanges() const noexcept {
        return pKissAndRunSpecChanges;
    }

    /// Return kiss-and-run partial release factor.
    ///
    /// \return Double.
    inline double getKissAndRunPartRelease() const noexcept {
        return pKissAndRunPartRelease;
    }

    /// Return a list of surface species dependencies.
    ///
    /// \return List of pointers of surface species.
    inline const std::vector<Spec*>& getSpecDeps() const noexcept {
        return pDepSurface;
    }

    /// Get the rate constant of the exocytotic reaction.
    ///
    /// \return Rate constant of the exocytotic reaction.
    inline double getKcst() const noexcept {
        return pKcst;
    }

    /// Set the rate constant of the exocytotic reaction.
    ///
    /// \param Rate constant of the exocytotic reaction.
    void setKcst(double kcst);

    ////////////////////////////////////////////////////////////////////////
    // INTERNAL (NON-EXPOSED) OPERATIONS: DELETION
    ////////////////////////////////////////////////////////////////////////
    /// Self delete.
    ///
    /// Called if Python object deleted, or from del method in parent object.
    /// Will only be called once
    void _handleSelfDelete();

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    std::string pID;
    Model& pModel;
    VesSurfsys& pVesSurfsys;

    std::vector<Spec*> pDepSurface;

    Raft* pRaft;
    bool pKissAndRun;
    std::map<Spec*, Spec*> pKissAndRunSpecChanges;
    double pKissAndRunPartRelease;
    double pKcst;
};

inline bool operator<(const Exocytosis& lhs, const Exocytosis& rhs) {
    return lhs.getID() < rhs.getID();
}

}  // namespace steps::model
