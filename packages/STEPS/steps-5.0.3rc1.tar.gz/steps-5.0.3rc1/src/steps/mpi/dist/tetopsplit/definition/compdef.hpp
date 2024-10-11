#pragma once

#include <memory>
#include <set>
#include <unordered_map>
#include <vector>

#include "fwd.hpp"

#include "geom/dist/fwd.hpp"
#include "model/fwd.hpp"
#include "model/reac.hpp"
#include "mpi/dist/tetopsplit/kproc/fwd.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {

/**
 * \brief State definition of a compartment.
 *
 * The Compdef class defines the sub biochemical container of a compartment.
 * It provides the global and local indexing for species, reactions
 * and diffusions in the compartment.
 *
 * This class corresponds to the solver::Compdef class in STEPS.
 */
class Compdef {
  public:
    Compdef(const Statedef& statedef,
            const DistComp& comp,
            container::compartment_id t_container_compartment);

    inline const model::compartment_id& getID() const noexcept {
        return model_compartment;
    }

    inline container::compartment_id getIdx() const noexcept {
        return container_compartment;
    }

    inline osh::Real getConductivity() const noexcept {
        return conductivity;
    }

    container::species_id getSpecContainerIdx(model::species_id species) const;

    container::species_id getSpecContainerIdx(const steps::model::Spec& spec) const;

    model::species_id getSpecModelIdx(container::species_id species) const;

    /**
     * \return number of chemical species in the compartment
     */
    inline osh::I32 getNSpecs() const noexcept {
        return static_cast<osh::I32>(specC2M.size());
    }

    /**
     * \return number of kinetic processes defined in the compartment
     */
    inline osh::I64 getNKProcs() const noexcept {
        return nKProcs;
    }

    /**
     * \return number of reactions defined in the compartment
     */
    inline osh::I64 getNReacs() const noexcept {
        return static_cast<osh::I64>(reacdefPtrs.size());
    }

    /**
     * \return number of diffusions defined in the compartment
     */
    inline osh::I64 getNDiffs() const noexcept {
        return static_cast<osh::I64>(diffdefPtrs.size());
    }

    /**
     * \return the diffusion definitions
     */
    inline const std::vector<std::unique_ptr<Diffdef>>& diffdefs() const noexcept {
        return diffdefPtrs;
    }

    inline const std::set<container::species_id>& getAllSpeciesDiffused() const noexcept {
        return species_diffused_;
    }

    inline bool isDiffused(const container::species_id& species) const {
        return std::find(species_diffused_.begin(), species_diffused_.end(), species) !=
               species_diffused_.end();
    }

    /**
     * \return the reaction definitions
     */
    template <typename rdefT>
    inline std::vector<std::unique_ptr<rdefT>>& reacdefs() noexcept {
        if constexpr (std::is_same_v<rdefT, Reacdef>) {
            return reacdefPtrs;
        } else if constexpr (std::is_same_v<rdefT, ComplexReacdef>) {
            return complexReacdefPtrs;
        } else {
            static_assert(util::always_false_v<rdefT>, "Unmanaged reaction type");
        }
    }

    template <typename rdefT>
    inline const std::vector<std::unique_ptr<rdefT>>& reacdefs() const noexcept {
        return const_cast<Compdef*>(this)->reacdefs<rdefT>();
    }

    inline const Statedef& statedef() const noexcept {
        return pStatedef;
    }

    void report(std::ostream& ostr) const;

  private:
    /**
     * Add the STEPS objects to the compartment definition and return their local index.
     * If the object has been added before, return its lidx in record,
     * otherwise add the object to the record and return its new lidx.
     */
    container::species_id addSpec(const steps::model::Spec& spec);
    template <typename ReacT>
    container::reaction_id addReac(const ReacT& reac);
    container::diffusion_id addDiff(model::species_id species, osh::Real dcst);

    // compartment KProc order: Reac then Diff
    const Statedef& pStatedef;
    model::compartment_id model_compartment;
    container::compartment_id container_compartment;
    std::set<container::species_id> species_diffused_;
    std::unordered_map<model::species_id, container::species_id> specM2C;
    std::vector<model::species_id> specC2M;
    osh::Real conductivity;

    osh::I64 nKProcs{};
    std::vector<std::unique_ptr<Reacdef>> reacdefPtrs;
    std::vector<std::unique_ptr<ComplexReacdef>> complexReacdefPtrs;
    std::vector<std::unique_ptr<Diffdef>> diffdefPtrs;
};

}  // namespace steps::dist
