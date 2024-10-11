/*
 ___license_placeholder___
 */

#pragma once

#include <string>

#include "complexevents.hpp"
#include "fwd.hpp"

namespace steps::model {

/// GHK current base class.
/// Current through a channel based on the GHK flux equation.
/// The GHK flux equation contains a term for the channel permeability, not
/// conductance (since this is not constant with changes in concentrations),
/// however it is assumed that single-channel SLOPE conductance will be
/// supplied, in which case we need to know a lot of information about the
/// conductance measurement in order to calculate the permeability constant. We
/// need to know at time of measurement: 1) the valence of the ion (which will
/// come from the species object and checked not to be zero), 2) the membrane
/// potential, 3) the intra and extra-cellular concentrations of the ion and 4)
/// the temperature.
/// 2,3 and 4 are conveniently all doubles, and can be supplied in a dict (map
/// in c++), e.g.   Ca_curr.setGMeasInfo({'temp':6.3, 'iconc': 5e-6}) If this
/// information is not supplied, these will be taken from the initial conditions
/// in the simulation itself. This information will then be used to find the
/// single-channel permeability to be used during the simulation.

/// \warning Methods start with an underscore are not exposed to Python.

class GHKcurrBase {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the GHK current reaction.
    /// \param surfsys Reference to the parent surface system.
    /// \param ion The ion species which carries the current.
    /// \param computeflux Whether the current should lead to species fluxes.
    /// \param virtual_oconc Virtual outside concentration of the ion.
    /// \param vshift Shift in membrane potential for the computation of GHK current.
    ///
    GHKcurrBase(std::string const& id,
                Surfsys& surfsys,
                Spec& ion,
                bool computeflux = true,
                double virtual_oconc = -1.0,
                double vshift = 0.0);

    GHKcurrBase(const GHKcurrBase&) = delete;
    GHKcurrBase& operator=(const GHKcurrBase&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // GHK CURRENT PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    /// Return the GHK current ID.
    ///
    /// \return ID of the GHK current.
    const std::string& getID() const noexcept {
        return pID;
    }

    /// Set or change the GHK current ID.
    ///
    /// \param id ID of the GHK current.
    void setID(std::string const& id);

    /// Return a reference to the parent surface system.
    ///
    /// \return Reference to the surface system.
    Surfsys& getSurfsys() const noexcept {
        return pSurfsys;
    }

    /// Return a reference to the parent model.
    ///
    /// \return Reference to the parent model.
    Model& getModel() const noexcept {
        return pModel;
    }

    /// Return a reference to the ion.
    ///
    /// \return Reference to the ion.
    Spec& getIon() const noexcept {
        return *pIon;
    }

    /// Change the ion.
    ///
    /// \param ion Ion species.
    void setIon(Spec& ion);

    /// Set or change the permeability measurement information.
    ///
    /// \param ginfo Permeability meaurement information.
    void setPInfo(double g, double V, double T, double oconc, double iconc);

    /// Directly set or change the single-channel permeability.
    ///
    /// \param ginfo Permeability.
    void setP(double p);

    /// Return the single-channel permeability.
    ///
    /// \return single channel permeability.
    double getP() {
        return _P();
    }

    ////////////////////////////////////////////////////////////////////////
    // INTERNAL (NON-EXPOSED) OPERATIONS: CONDUCTANCE INFORMATION
    ////////////////////////////////////////////////////////////////////////
    /// Return whether user has supplied conductance information or not.
    ///
    /// \Return Conductance information supplied bool
    bool _infosupplied() const noexcept {
        return pInfoSupplied;
    }

    int _valence() const;

    double _P() const;

    ////////////////////////////////////////////////////////////////////////
    // INTERNAL (NON-EXPOSED) OPERATIONS
    ////////////////////////////////////////////////////////////////////////
    // Real flux flag
    bool _realflux() const noexcept {
        return pRealFlux;
    }

    double _voconc() const noexcept {
        return pVirtual_conc;
    }

    double _vshift() const noexcept {
        return pVshift;
    }

    ////////////////////////////////////////////////////////////////////////

  protected:
    ////////////////////////////////////////////////////////////////////////

    std::string pID;
    Model& pModel;
    Surfsys& pSurfsys;
    Spec* pIon;
    bool pRealFlux;

    ////////////////////////////////////////////////////////////////////////
    // CONDUCTANCE MEASUREMENT INFORMATION
    ////////////////////////////////////////////////////////////////////////
    // The measured conductance
    double pG;
    // The ion valence. This comes from Spec object
    int pValence;
    // The potential
    double pV;
    // The temperature IN KELVIN
    double pTemp;
    // The inner concentration in Molar units
    double pInnerConc;
    // The outer concentration in Molar units
    double pOuterConc;

    // The single-channel permeability, if we have it
    double pP;

    // True if we have all conductance measurement information.
    // An exception should be thrown at def level if this info is missing.
    bool pInfoSupplied;

    // The 'virtual outer-concentration'. If this is set to a positive number
    // then the outer concentration will be taken from this number,
    // allowing GHK currents on surface of mesh with no outer compartment
    double pVirtual_conc;

    // Allowing a 'voltage shift' for the calcuation as this is used in
    // some models
    double pVshift;
};

////////////////////////////////////////////////////////////////////////
/// GHK current with a species-like channel state
class GHKcurr: public GHKcurrBase {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the GHK current reaction.
    /// \param surfsys Reference to the parent surface system.
    /// \param chanstate The channel state in which current is conducted.
    /// \param ion The ion species which carries the current.
    /// \param computeflux Whether the current should lead to species fluxes.
    /// \param virtual_oconc Virtual outside concentration of the ion.
    /// \param vshift Shift in membrane potential for the computation of GHK current.
    ///
    GHKcurr(std::string const& id,
            Surfsys& surfsys,
            ChanState& chanstate,
            Spec& ion,
            bool computeflux = true,
            double virtual_oconc = -1.0,
            double vshift = 0.0);

    /// Destructor
    ~GHKcurr();

    ////////////////////////////////////////////////////////////////////////
    // GHK CURRENT PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    /// Return a reference to the associated channel state.
    ///
    /// \return Reference to the channel state.
    ChanState& getChanState() const noexcept {
        return *pChanState;
    }

    /// Change the channel state.
    ///
    /// \param chanstate Channel state of the open state.
    void setChanState(ChanState& chanstate);

    ////////////////////////////////////////////////////////////////////////
    // INTERNAL (NON-EXPOSED) OPERATIONS: DELETION
    ////////////////////////////////////////////////////////////////////////
    /// Self delete.
    ///
    /// Called if Python object deleted, or from del method in parent object.
    /// Will only be called once
    void _handleSelfDelete();

  private:
    ChanState* pChanState;
};


////////////////////////////////////////////////////////////////////////
/// GHK current with a multi-state complex channel state
class ComplexGHKcurr: public GHKcurrBase {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the ohmic current reaction.
    /// \param surfsys Reference to the parent surface system.
    /// \param cplx The name of the complex type involved in the current
    /// \param filt The complex filter that determines the conducting states
    /// \param ion The ion species which carries the current.
    /// \param computeflux Whether the current should lead to species fluxes.
    /// \param virtual_oconc Virtual outside concentration of the ion.
    /// \param vshift Shift in membrane potential for the computation of GHK current.
    ///
    ComplexGHKcurr(std::string const& id,
                   Surfsys& surfsys,
                   std::string const& cplx,
                   const std::vector<std::vector<SubunitStateFilter>>& filt,
                   Spec& ion,
                   bool computeflux = true,
                   double virtual_oconc = -1.0,
                   double vshift = 0.0);

    /// Return a reference to the associated channel state.
    ///
    /// \return Reference to the channel state.
    inline const ComplexFilterDescr& getChanState() const noexcept {
        return pChanState;
    }

    ComplexUpdateEvent getUpdEvent() const noexcept;

  private:
    const ComplexFilterDescr pChanState;
};

}  // namespace steps::model
