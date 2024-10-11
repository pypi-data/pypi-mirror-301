
#include "patchdef.hpp"

#include "geom/dist/distpatch.hpp"
#include "model/ghkcurr.hpp"
#include "model/spec.hpp"
#include "model/sreac.hpp"
#include "model/vdepsreac.hpp"
#include "sreacdef.hpp"
#include "statedef.hpp"
#include "util/vocabulary.hpp"
#include <optional>

namespace steps::dist {

//-------------------------------------------------------

container::species_id Patchdef::getSpecContainerIdx(model::species_id species) const {
    const auto& it = specM2C_.find(species);
    if (it != specM2C_.end()) {
        return it->second;
    }
    throw std::logic_error("Unregistered species id " + pStatedef_.getSpecID(species) +
                           " in patch " + model_patch_);
}

//-------------------------------------------------------

container::species_id Patchdef::getSpecContainerIdx(const steps::model::Spec& spec) const {
    return getSpecContainerIdx(pStatedef_.getSpecModelIdx(spec));
}

//-------------------------------------------------------

container::species_id Patchdef::getSpecContainerIdx(model::species_name species) const {
    return getSpecContainerIdx(pStatedef_.getSpecModelIdx(species));
}

//-------------------------------------------------------

template <typename SReacT, class... ArgsT>
container::surface_reaction_id Patchdef::addReac(const SReacT& sreac, ArgsT... args) {
    using rdefT = typename Model2Def<SReacT>::def_type;
    container::kproc_id kproc_id(nKProcs_);
    auto& rdefPtrs = reacdefs<rdefT>();
    container::surface_reaction_id reac_container_idx(static_cast<osh::I64>(rdefPtrs.size()));
    rdefPtrs.emplace_back(
        std::make_unique<rdefT>(*this, kproc_id, reac_container_idx, sreac, args...));
    if constexpr (not std::is_base_of_v<steps::model::GHKcurrBase, SReacT>) {
        reacM2C_.emplace(model::surface_reaction_id(sreac.getID()), reac_container_idx);
    }
    nKProcs_++;
    return reac_container_idx;
}

//-------------------------------------------------------

std::pair<container::surface_reaction_id, container::surface_reaction_id> Patchdef::addGHKReacs(
    const steps::model::GHKcurr& curr) {
    return {addReac(curr, true), addReac(curr, false)};
}

//-------------------------------------------------------

std::pair<container::surface_reaction_id, container::surface_reaction_id> Patchdef::addGHKReacs(
    const steps::model::ComplexGHKcurr& curr) {
    return {addReac(curr, true), addReac(curr, false)};
}

//-------------------------------------------------------

Patchdef::Patchdef(const Statedef& statedef,
                   const DistPatch& patch,
                   container::patch_id container_patch_id)
    : pStatedef_(statedef)
    , model_patch_(patch.getID())
    , inner_compartment_id_(patch.getIComp().getID())
    , container_patch_id_(container_patch_id)
    , nKProcs_(0) {
    if (patch.getOComp() != nullptr) {
        outer_compartment_id_.emplace(patch.getOComp()->getID());
    }
    // Species
    for (auto* spec: patch.getAllSpecs(pStatedef_.model())) {
        addSpec(pStatedef_.getSpecModelIdx(model::species_name(spec->getID())));
    }
    // Surface diffusions
    auto diffs = patch.getAllDiffs(pStatedef_.model());
    if (not diffs.empty()) {
        throw std::logic_error("Model contains surface diffusion rules.");
    }
    // Surface reactions
    for (auto* sreac: patch.getAllSReacs(pStatedef_.model())) {
        addReac(*sreac);
    }
    // Voltage dependent surface reactions
    for (auto* vdepsreac: patch.getAllVDepSReacs(pStatedef_.model())) {
        addReac(*vdepsreac);
    }
    // Complex surface reactions
    for (auto* sreac: patch.getAllComplexSReacs(pStatedef_.model())) {
        addReac(*sreac);
    }
    // Complex surface reactions
    for (auto* sreac: patch.getAllVDepComplexSReacs(pStatedef_.model())) {
        addReac(*sreac);
    }
}

//-------------------------------------------------------

model::species_id Patchdef::getSpecModelIdx(container::species_id species) const {
    if (!(species < static_cast<container::species_id::value_type>(specC2M_.size()))) {
        throw std::invalid_argument(std::string("Unregistered needed species in patch ") +
                                    model_patch_);
    }
    return specC2M_[static_cast<size_t>(species.get())];
}

//-------------------------------------------------------

container::surface_reaction_id Patchdef::getReacIdx(model::surface_reaction_id reaction_id) const {
    return reacM2C_.at(reaction_id);
}

//-------------------------------------------------------

const Compdef& Patchdef::getInnerComp() const noexcept {
    return pStatedef_.getCompdef(inner_compartment_id_);
}

//-------------------------------------------------------

const SReacdef& Patchdef::getReac(container::surface_reaction_id reaction_id) const {
    return *reacdefPtrs_[static_cast<size_t>(reaction_id.get())];
}

//-------------------------------------------------------

container::species_id Patchdef::addSpec(model::species_id species) {
    auto speciesIt = specM2C_.find(species);
    if (speciesIt != specM2C_.end()) {
        return speciesIt->second;
    }
    const container::species_id spec_container_idx(
        static_cast<container::species_id::value_type>(specC2M_.size()));
    specM2C_[species] = spec_container_idx;
    specC2M_.push_back(species);
    return spec_container_idx;
}

//-------------------------------------------------------

inline osh::I64 Patchdef::getNReacs() const {
    return static_cast<osh::I64>(reacdefPtrs_.size());
}

//-------------------------------------------------------

inline osh::I64 Patchdef::getNKProcs() const {
    return nKProcs_;
}

}  // namespace steps::dist
