#include "statedef.hpp"

#include <algorithm>
#include <sstream>

#include "compdef.hpp"
#include "complexdef.hpp"
#include "diffdef.hpp"
#include "efield.hpp"
#include "fwd.hpp"
#include "patchdef.hpp"
#include "reacdef.hpp"

#include "geom/dist/distcomp.hpp"
#include "geom/dist/distmemb.hpp"
#include "geom/dist/distmesh.hpp"
#include "geom/dist/distpatch.hpp"
#include "math/constants.hpp"
#include "model/chan.hpp"
#include "model/chanstate.hpp"
#include "model/complex.hpp"
#include "model/diff.hpp"
#include "model/ghkcurr.hpp"
#include "model/model.hpp"
#include "model/ohmiccurr.hpp"
#include "model/reac.hpp"
#include "model/spec.hpp"
#include "model/sreac.hpp"
#include "model/surfsys.hpp"
#include "model/vdepsreac.hpp"
#include "util/collections.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {

/**
 * \brief Helper function that augment std::map::at with an error message
 * if \key cannot be found.
 *
 * TMap can be a std::map or a std::unordered_map
 *
 */
template <typename AssociativeContainer>
const typename AssociativeContainer::mapped_type& map_at(
    const AssociativeContainer& container,
    const typename AssociativeContainer::key_type& key,
    const char* name) {
    try {
        return container.at(key);
    } catch (const std::out_of_range&) {
        std::stringstream ss;
        ss << "No " << name << " with id " << key << ". Possible values are:\n[";
        for (const auto& i: container) {
            ss << i.first << ", ";
        }
        ss << "].\n";
        throw std::invalid_argument(ss.str());
    }
}

template <typename AssociativeContainer>
typename AssociativeContainer::mapped_type& map_at(
    AssociativeContainer& container,
    const typename AssociativeContainer::key_type& key,
    const char* name) {
    try {
        return container.at(key);
    } catch (const std::out_of_range&) {
        std::stringstream ss;
        ss << "No " << name << " with id " << key << ". Possible values are:\n[";
        for (const auto& i: container) {
            ss << i.first << ", ";
        }
        ss << "].\n";
        throw std::invalid_argument(ss.str());
    }
}


Statedef::Statedef(const steps::model::Model& _model, const steps::dist::DistMesh& mesh)
    : pModel(_model)
    , pMesh(mesh) {
    // Species
    for (auto* spec: model().getAllSpecs()) {
        addSpec(*spec);
    }

    // Complexes
    for (auto* complex: model().getAllComplexes()) {
        addComplex(*complex);
    }

    // Compartments
    for (auto* comp: mesh.getAllComps()) {
        addComp(*comp);
    }

    for (auto* patch: mesh.getAllPatches()) {
        addPatch(*patch);
    }

    for (auto& memb: mesh.membranes()) {
        addMembrane(*memb.second);
    }
}

model::species_id Statedef::addSpec(const steps::model::Spec& spec) {
    model::species_name name(spec.getID());
    auto result = specModelIdxs.find(name);
    if (result != specModelIdxs.end()) {
        return result->second;
    }
    model::species_id model_idx(static_cast<int>(specModelIdxs.size()));
    specModelIdxs.emplace(name, model_idx);
    specIDs.container().push_back(name);
    return model_idx;
}

model::complex_id Statedef::addComplex(const steps::model::Complex& cmplx) {
    model::complex_name name(cmplx.getID());
    auto result = complexModelIdxs.find(name);
    if (result != complexModelIdxs.end()) {
        return result->second;
    }
    model::complex_id model_idx(static_cast<int>(complexModelIdxs.size()));
    complexModelIdxs.emplace(name, model_idx);
    complexIDs.container().push_back(name);
    complexdefPtrs.container().emplace_back(new Complexdef(*this, model_idx, cmplx));
    return complexModelIdxs[name];
}

model::species_id Statedef::getSpecModelIdx(const model::species_name& name) const {
    auto result = specModelIdxs.find(name);
    if (result == specModelIdxs.end()) {
        return {};
    }
    return result->second;
}

model::species_id Statedef::getSpecModelIdx(const steps::model::Spec& spec) const {
    return getSpecModelIdx(model::species_name(spec.getID()));
}

model::complex_id Statedef::getComplexModelIdx(const model::complex_name& name) const {
    auto result = complexModelIdxs.find(name);
    if (result == complexModelIdxs.end()) {
        return {};
    }
    return result->second;
}

container::compartment_id Statedef::addComp(const DistComp& compartment) {
    container::compartment_id container_id(compdefPtrs.size());
    compdefPtrs.container().emplace_back(
        std::make_unique<Compdef>(*this, compartment, container_id));
    compModelIdxs.emplace(compartment.getID(), container_id);
    return container_id;
}

container::patch_id Statedef::addPatch(const DistPatch& patch) {
    container::patch_id container_id(patchdefPtrs.size());
    patchdefPtrs.container().emplace_back(std::make_unique<Patchdef>(*this, patch, container_id));
    patchModelIdxs.emplace(patch.getID(), container_id);
    return container_id;
}

container::membrane_id Statedef::addMembrane(const DistMemb& membrane) {
    container::membrane_id container_id(membranePtrs.size());
    membranePtrs.container().emplace_back(std::make_unique<Membrane>(*this, membrane));
    membraneModelIdxs.emplace(membrane.getID(), container_id);
    return container_id;
}

container::compartment_id Statedef::getCompModelIdx(
    const model::compartment_id& compartment) const noexcept {
    const auto id = compModelIdxs.find(compartment);
    if (id == compModelIdxs.end()) {
        return {};
    }
    return id->second;
}

Compdef& Statedef::getCompdef(container::compartment_id compartment) const noexcept {
    return *compdefPtrs[compartment];
}

Compdef& Statedef::getCompdef(const model::compartment_id& compartment) const noexcept {
    return *compdefPtrs[getCompModelIdx(compartment)];
}

Patchdef& Statedef::getPatchdef(const container::patch_id& patchId) const noexcept {
    return *patchdefPtrs[patchId];
}

Patchdef& Statedef::getPatchdef(const model::patch_id& patchId) const {
    return *patchdefPtrs[map_at(patchModelIdxs, patchId, "patches")];
}

Membrane& Statedef::getMembrane(const model::membrane_id& membraneId) const {
    return *membranePtrs[map_at(membraneModelIdxs, membraneId, "membranes")];
}

container::species_id Statedef::getCompSpecContainerIdx(const model::compartment_id& compartment,
                                                        const model::species_name& specie) const {
    const auto comp_model_idx = getCompModelIdx(compartment);
    if (comp_model_idx.unknown()) {
        std::ostringstream msg;
        msg << "Unknown compartment: " << compartment;
        throw std::invalid_argument(msg.str());
    }
    const auto spec_model_idx = getSpecModelIdx(specie);
    if (spec_model_idx.unknown()) {
        std::ostringstream msg;
        msg << "Unknown species: " << specie;
        throw std::invalid_argument(msg.str());
    }

    return compdefPtrs[comp_model_idx]->getSpecContainerIdx(spec_model_idx);
}

container::surface_reaction_id Statedef::getSReacIdx(const model::patch_id& patchId,
                                                     const model::surface_reaction_id& reac) const {
    return getPatchdef(patchId).getReacIdx(reac);
}

std::string Statedef::createReport() const {
    std::stringstream report_stream;
    report_stream << "Biochemical Model Report\n";
    report_stream << "Number of Species: " << specModelIdxs.size() << std::endl;
    report_stream << "[ID, ModelIdx]\n";
    for (auto&& spec: specModelIdxs) {
        report_stream << "[" << spec.first << ", " << spec.second << "]" << '\n';
    }
    report_stream << '\n';

    report_stream << "Number of Compartments: " << compModelIdxs.size() << '\n';
    report_stream << "[ID, Model Idx]\n";
    for (auto&& comp: compModelIdxs) {
        report_stream << "[" << comp.first << ", " << comp.second << "]" << '\n';
    }
    report_stream << '\n';

    report_stream << "Number of Patches: " << patchModelIdxs.size() << '\n';
    report_stream << "[ID, Model Idx]\n";
    for (auto&& patch: patchModelIdxs) {
        report_stream << "[" << patch.first << ", " << patch.second << "]" << '\n';
    }
    report_stream << '\n';

    report_stream << "Detail Compartment Report\n";
    for (auto&& compdef: compdefPtrs) {
        compdef->report(report_stream);
    }
    report_stream << '\n';

    return report_stream.str();
}

const OhmicCurrent& Statedef::addOhmicCurrent(const model::ohmic_current_id& curr_id,
                                              const container::species_id& chanState,
                                              double conductance,
                                              double reversal_potential) {
    auto curr_it = ohmicCurrPtrs.find(curr_id);
    if (curr_it == ohmicCurrPtrs.end()) {
        curr_it =
            ohmicCurrPtrs
                .emplace(curr_id,
                         std::make_unique<OhmicCurrent>(conductance, reversal_potential, chanState))
                .first;
    }
    return *curr_it->second;
}

const ComplexOhmicCurrent& Statedef::addComplexOhmicCurrent(const model::ohmic_current_id& curr_id,
                                                            const ComplexFilterDescr& chanState,
                                                            double conductance,
                                                            double reversal_potential) {
    auto curr_it = complexOhmicCurrPtrs.find(curr_id);
    if (curr_it == complexOhmicCurrPtrs.end()) {
        curr_it = complexOhmicCurrPtrs
                      .emplace(curr_id,
                               std::make_unique<ComplexOhmicCurrent>(conductance,
                                                                     reversal_potential,
                                                                     chanState))
                      .first;
    }
    return *curr_it->second;
}

const GHKCurrent& Statedef::addGHKCurrent(const model::ghk_current_id& curr_id,
                                          model::species_name ion_channel_state,
                                          model::species_name ion_id,
                                          osh::I64 valence) {
    auto curr_it = ghkCurrPtrs.find(curr_id);
    if (curr_it == ghkCurrPtrs.end()) {
        curr_it = ghkCurrPtrs
                      .emplace(curr_id,
                               std::make_unique<GHKCurrent>(ion_channel_state, ion_id, valence))
                      .first;
    }
    return *curr_it->second;
}

const ComplexGHKCurrent& Statedef::addComplexGHKCurrent(const model::ghk_current_id& curr_id,
                                                        const ComplexFilterDescr& ion_channel_state,
                                                        model::species_name ion_id,
                                                        osh::I64 valence) {
    auto curr_it = complexGhkCurrPtrs.find(curr_id);
    if (curr_it == complexGhkCurrPtrs.end()) {
        curr_it =
            complexGhkCurrPtrs
                .emplace(curr_id,
                         std::make_unique<ComplexGHKCurrent>(ion_channel_state, ion_id, valence))
                .first;
    }
    return *curr_it->second;
}

void Statedef::setStimulus(const model::membrane_id& membrane, osh::Real current) {
    auto& memb = getMembrane(membrane);
    memb.setStimulus([current](auto) { return current; });
}

void Statedef::setResistivity(const model::membrane_id& membrane, osh::Real resistivity) {
    if (resistivity <= 0) {
        throw std::invalid_argument("Resistivity must be strictly positive");
    }
    auto& memb = getMembrane(membrane);
    memb.setConductivity(1.0 / resistivity);
}

osh::Real Statedef::getResistivity(const model::membrane_id& membrane) const {
    auto& memb = getMembrane(membrane);
    return 1.0 / memb.conductivity();
}

void Statedef::setReversalPotential(const model::membrane_id& membrane,
                                    osh::Real reversal_potential) {
    auto& memb = getMembrane(membrane);
    memb.setReversalPotential(reversal_potential);
}

osh::Real Statedef::getReversalPotential(const model::membrane_id& membrane) const {
    auto& memb = getMembrane(membrane);
    return memb.reversal_potential();
}

}  // namespace steps::dist
