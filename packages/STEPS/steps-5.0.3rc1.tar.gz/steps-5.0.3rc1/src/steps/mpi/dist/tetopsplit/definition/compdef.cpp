#include "compdef.hpp"

#include <cassert>
#include <memory>

#include "diffdef.hpp"
#include "geom/dist/distcomp.hpp"
#include "model/diff.hpp"
#include "model/reac.hpp"
#include "model/spec.hpp"
#include "mpi/dist/tetopsplit/definition/fwd.hpp"
#include "reacdef.hpp"
#include "statedef.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {

Compdef::Compdef(const Statedef& statedef,
                 const DistComp& comp,
                 container::compartment_id t_container_compartment)
    : pStatedef(statedef)
    , model_compartment(comp.getID())
    , container_compartment(t_container_compartment)
    , conductivity(comp.getConductivity()) {
    for (auto& spec: comp.getAllSpecs(statedef.model())) {
        addSpec(*spec);
    }

    // Reactions
    for (auto* reac: comp.getAllReacs(statedef.model())) {
        addReac(*reac);
    }

    // Complex Reactions
    for (auto* reac: comp.getAllComplexReacs(statedef.model())) {
        addReac(*reac);
    }

    // Diffusions
    for (const auto* diff: comp.getAllDiffs(statedef.model())) {
        const model::species_name lig_name(diff->getLig().getID());
        addDiff(statedef.getSpecModelIdx(lig_name), diff->getDcst());
    }
}

container::species_id Compdef::addSpec(const steps::model::Spec& spec) {
    model::species_id species(pStatedef.getSpecModelIdx(model::species_name(spec.getID())));
    auto speciesIt = specM2C.find(species);
    if (speciesIt != specM2C.end()) {
        return speciesIt->second;
    }
    const container::species_id spec_container_idx(
        static_cast<container::species_id::value_type>(specC2M.size()));
    specM2C[species] = spec_container_idx;
    specC2M.push_back(species);
    return spec_container_idx;
}

container::species_id Compdef::getSpecContainerIdx(model::species_id species) const {
    auto result = specM2C.find(species);
    if (result != specM2C.end()) {
        return result->second;
    }
    return {};
}

container::species_id Compdef::getSpecContainerIdx(const steps::model::Spec& spec) const {
    return getSpecContainerIdx(pStatedef.getSpecModelIdx(spec));
}

model::species_id Compdef::getSpecModelIdx(container::species_id species) const {
    assert(species < static_cast<container::species_id::value_type>(specC2M.size()));
    return specC2M[static_cast<size_t>(species.get())];
}

template <typename ReacT>
container::reaction_id Compdef::addReac(const ReacT& reac) {
    using rdefT = typename Model2Def<ReacT>::def_type;
    container::kproc_id kproc_id(nKProcs);
    auto& rdefPtrs = reacdefs<rdefT>();
    container::reaction_id reac_container_idx(static_cast<osh::I64>(rdefPtrs.size()));
    rdefPtrs.emplace_back(std::make_unique<rdefT>(*this, kproc_id, reac_container_idx, reac));
    nKProcs++;
    return reac_container_idx;
}

container::diffusion_id Compdef::addDiff(model::species_id species, osh::Real dcst) {
    const container::kproc_id kproc_id(nKProcs);
    const container::diffusion_id diffusion_id(static_cast<osh::I64>(diffdefPtrs.size()));
    const container::species_id spec(getSpecContainerIdx(species));
    assert(spec.valid());
    diffdefPtrs.emplace_back(std::make_unique<Diffdef>(*this, kproc_id, diffusion_id, spec, dcst));
    nKProcs++;
    species_diffused_.insert(spec);
    return diffusion_id;
}

void Compdef::report(std::ostream& ostr) const {
    ostr << "Compartment ID: " << model_compartment << " Model Idx: " << container_compartment
         << std::endl;
    ostr << "Number of Species: " << specM2C.size() << std::endl;
    ostr << "SpecM2C: [Model Idx, Container Idx]\n";
    for (const auto& spec: specM2C) {
        ostr << "[" << spec.first << ", " << spec.second << "]" << std::endl;
    }
    ostr << "SpecC2M: [Container Idx, Model Idx]\n";
    auto spec_container_idx = 0;
    for (const auto& spec: specC2M) {
        ostr << "[" << spec_container_idx << ", " << spec << "]" << std::endl;
        spec_container_idx++;
    }

    ostr << std::endl;
    ostr << "Number of Kinetic Processes: " << nKProcs << " (Reactions: " << reacdefPtrs.size()
         << ","
         << " Diffusions: " << diffdefPtrs.size() << ")\n";

    ostr << std::endl;
    for (const auto& reacdef: reacdefPtrs) {
        reacdef->report(ostr, std::nullopt);
    }

    ostr << std::endl;
    for (const auto& diffdef: diffdefPtrs) {
        diffdef->report(ostr);
    }
    ostr << std::endl;
}

}  // namespace steps::dist
