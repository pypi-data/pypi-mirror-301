/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <string>
#include <vector>

#include "fwd.hpp"
#include "model/fwd.hpp"

namespace steps::solver {

////////////////////////////////////////////////////////////////////////////////
/// Defined diffusion object.
template <typename GlobalId>
class MetaDiffdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the object.
    /// \param d Reference to the associated Diff object.

    // NOTE: Since one class is used for both volume and surface diffusion,
    // can't think of another way right now but to use unsigned ints and not
    // strong ids for the indices
    MetaDiffdef(Statedef& sd, GlobalId idx, model::Diff& d);

    MetaDiffdef(const MetaDiffdef&) = delete;
    MetaDiffdef& operator=(const MetaDiffdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: DIFFUSION RULE
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this diffusion rule.
    inline GlobalId gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of this diffusion rule.
    inline const std::string& name() const noexcept {
        return pName;
    }

    /// Return the diffusion constant.
    inline double dcst() const noexcept {
        return pDcst;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: LIGAND
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of the ligand species.
    spec_global_id lig() const;

    int dep(spec_global_id gidx) const;

    bool reqspec(spec_global_id gidx) const;

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Setup the object.
    void setup(const Statedef& sd);

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    // The global index of this diffusion rule
    const GlobalId pIdx;

    // The string identifier of this diffusion rule
    const std::string pName;

    // The diffusion constant
    const double pDcst;

    // The global index of the spec
    const spec_global_id ligGIdx;

    bool pSetupdone{false};

    ////////////////////////////////////////////////////////////////////////
    // DATA: LIGAND
    ////////////////////////////////////////////////////////////////////////

    std::vector<int> pSpec_DEP;
};

// explicit template instantiation declarations
extern template class MetaDiffdef<diff_global_id>;
extern template class MetaDiffdef<surfdiff_global_id>;

}  // namespace steps::solver
