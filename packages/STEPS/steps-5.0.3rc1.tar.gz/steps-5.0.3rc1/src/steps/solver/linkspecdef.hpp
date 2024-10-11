/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>

#include "fwd.hpp"
#include "model/linkspec.hpp"

namespace steps::solver {

/// Defined LinkSpecies
class LinkSpecdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the linkspecies.
    /// \param l Reference to the associated LinkSpec object.
    LinkSpecdef(Statedef& sd, linkspec_global_id idx, model::LinkSpec& l);

    LinkSpecdef(const LinkSpecdef&) = delete;
    LinkSpecdef& operator=(const LinkSpecdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: LINKSPECIES
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this link species.
    inline linkspec_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the species.
    const std::string& name() const noexcept {
        return pName;
    }

    inline double dcst() const noexcept {
        return pDcst;
    }

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////
    /// Setup the object.
    ///
    /// This method is included for consistency with other def objects,
    /// but currently does very little.
    void setup(const Statedef&);

  private:
    const linkspec_global_id pIdx;
    const std::string pName;
    const double pDcst;
    bool pSetupdone{false};
};

}  // namespace steps::solver
