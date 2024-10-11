#pragma once

#include <cassert>
#include <memory>
#include <numeric>
#include <optional>
#include <set>
#include <unordered_map>
#include <vector>

#include "fwd.hpp"
#include "geom/dist/fwd.hpp"
#include "model/fwd.hpp"
#include "model/ghkcurr.hpp"
#include "model/spec.hpp"
#include "model/vdepsreac.hpp"
#include "mpi/dist/tetopsplit/kproc/fwd.hpp"
#include "solver/vdepsreacdef.hpp"
#include "sreacdef.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {


/**
 * \brief State definition of a patch.
 *
 * The Patchdef class defines the sub biochemical container of a patch.
 * It provides the global and local indexing for species, reactions
 * and diffusions in the compartment.
 *
 */
class Patchdef {
  public:
    Patchdef(const Statedef& statedef,
             const DistPatch& patch,
             container::patch_id container_patch_id);

    inline const model::patch_id& getID() const noexcept {
        return model_patch_;
    }

    inline container::patch_id getModelIdx() const noexcept {
        return container_patch_id_;
    }

    inline model::compartment_id getInnerCompId() const noexcept {
        return inner_compartment_id_;
    }

    container::surface_reaction_id getReacIdx(model::surface_reaction_id reaction_id) const;

    const Compdef& getInnerComp() const noexcept;

    inline const std::optional<model::compartment_id>& getOuterCompId() const noexcept {
        return outer_compartment_id_;
    }

    model::species_id getSpecModelIdx(container::species_id species) const;

    inline osh::LO getNSpecs() const noexcept {
        return static_cast<osh::LO>(specC2M_.size());
    }

    const SReacdef& getReac(container::surface_reaction_id reaction_id) const;

    /**
     * \return the reaction definitions
     */
    template <typename rdefT>
    inline std::vector<std::unique_ptr<rdefT>>& reacdefs() noexcept {
        if constexpr (std::is_same_v<rdefT, SReacdef>) {
            return reacdefPtrs_;
        } else if constexpr (std::is_same_v<rdefT, ComplexSReacdef>) {
            return complexReacdefPtrs_;
        } else if constexpr (std::is_same_v<rdefT, VDepComplexSReacdef>) {
            return vdepComplexReacdefPtrs_;
        } else if constexpr (std::is_same_v<rdefT, VDepSReacdef>) {
            return vdepSReacPtrs_;
        } else if constexpr (std::is_same_v<rdefT, GHKSReacdef>) {
            return ghkSReacPtrs_;
        } else if constexpr (std::is_same_v<rdefT, ComplexGHKSReacdef>) {
            return complexGhkSReacPtrs_;
        } else {
            static_assert(util::always_false_v<rdefT>, "Unmanaged reaction type");
        }
    }

    inline const Statedef& statedef() const noexcept {
        return pStatedef_;
    }

    inline const std::set<container::species_id>& getAllSpeciesDiffused() const noexcept {
        return species_diffused_;
    }

    inline bool isDiffused(const container::species_id& species) const {
        return species_diffused_.find(species) != species_diffused_.end();
    }

    inline osh::I64 getNReacs() const;

    inline osh::I64 getNKProcs() const;

    container::species_id getSpecContainerIdx(const steps::model::Spec& spec) const;
    container::species_id getSpecContainerIdx(model::species_name species) const;
    container::species_id getSpecContainerIdx(model::species_id species) const;

    //-------------------------------------------------------

    std::pair<container::surface_reaction_id, container::surface_reaction_id> addGHKReacs(
        const steps::model::GHKcurr& curr);
    std::pair<container::surface_reaction_id, container::surface_reaction_id> addGHKReacs(
        const steps::model::ComplexGHKcurr& curr);

  private:
    container::species_id addSpec(model::species_id species);

    template <typename SReacT, class... ArgsT>
    container::surface_reaction_id addReac(const SReacT& sreac, ArgsT... args);

    // compartment KProc order: Reac then Diff
    const Statedef& pStatedef_;
    model::patch_id model_patch_;
    model::compartment_id inner_compartment_id_;
    std::optional<model::compartment_id> outer_compartment_id_;
    container::patch_id container_patch_id_;
    std::unordered_map<model::species_id, container::species_id> specM2C_;
    std::map<model::surface_reaction_id, container::surface_reaction_id> reacM2C_;
    std::vector<model::species_id> specC2M_;
    osh::I64 nKProcs_;

    std::vector<std::unique_ptr<SReacdef>> reacdefPtrs_;
    std::vector<std::unique_ptr<ComplexSReacdef>> complexReacdefPtrs_;
    std::vector<std::unique_ptr<VDepComplexSReacdef>> vdepComplexReacdefPtrs_;
    std::vector<std::unique_ptr<VDepSReacdef>> vdepSReacPtrs_;
    std::vector<std::unique_ptr<GHKSReacdef>> ghkSReacPtrs_;
    std::vector<std::unique_ptr<ComplexGHKSReacdef>> complexGhkSReacPtrs_;
    // This is in preparation for SReac
    std::set<container::species_id> species_diffused_;
};

}  // namespace steps::dist
