/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>

#include "fwd.hpp"
#include "model/ohmiccurr.hpp"

namespace steps::solver {

class OhmicCurrdef {
  public:
    /// Constructor
    ///
    /// \param sd Defined state of the solver.
    /// \param gidx Global index of the ohmic current.
    /// \param oc Reference to the OhmicCurr object.
    OhmicCurrdef(Statedef& sd, ohmiccurr_global_id gidx, model::OhmicCurr& oc);

    OhmicCurrdef(const OhmicCurrdef&) = delete;
    OhmicCurrdef& operator=(const OhmicCurrdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Setup the object.
    void setup(const Statedef& sd);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: OHMIC CURRENT
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this ohmic current.
    inline ohmiccurr_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the ohmic current.
    inline const std::string& name() const noexcept {
        return pName;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: PARAMETERS
    ////////////////////////////////////////////////////////////////////////

    inline double getG() const noexcept {
        return pG;
    }
    inline double getERev() const noexcept {
        return pERev;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: CHANNEL STATE
    ////////////////////////////////////////////////////////////////////////

    // Return the global index of the channel state
    spec_global_id chanstate() const;

    int dep(spec_global_id gidx) const;
    bool req(spec_global_id gidx) const;

    ////////////////////////////////////////////////////////////////////////

  private:
    /// The global index of this ohmic current.
    const ohmiccurr_global_id pIdx;

    /// The string identifier of this ohmic current.
    const std::string pName;

    /// True if setup() has been called.
    bool pSetupdone{false};

    ////////////////////////////////////////////////////////////////////////
    // DATA: PARAMETERS
    ////////////////////////////////////////////////////////////////////////

    /// The channel state store as a string, rather than ChanState pointer
    const std::string pChanState;

    /// Single-channel conductance
    const double pG;

    /// Reversal potential
    const double pERev;

    util::strongid_vector<spec_global_id, int> pSpec_DEP;

    // Global index of the channel state
    spec_global_id pSpec_CHANSTATE;
};

}  // namespace steps::solver
