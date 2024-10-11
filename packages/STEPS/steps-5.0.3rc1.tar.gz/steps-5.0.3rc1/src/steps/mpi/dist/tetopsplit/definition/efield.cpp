#include "efield.hpp"

#include "../mol_state.hpp"
#include "geom/dist/distmemb.hpp"
#include "geom/dist/distmesh.hpp"
#include "geom/patch.hpp"
#include "math/constants.hpp"
#include "model/chan.hpp"
#include "model/chanstate.hpp"
#include "model/ghkcurr.hpp"
#include "model/ohmiccurr.hpp"
#include "model/surfsys.hpp"
#include "mpi/dist/tetopsplit/definition/complexeventsdef.hpp"
#include "patchdef.hpp"
#include "statedef.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {

osh::Real OhmicCurrentBase::getReversalPotential(mesh::triangle_id_t triangle) const {
    auto it = reversal_potentials.find(triangle);
    if (it != reversal_potentials.end()) {
        return it->second;
    }
    return reversal_potential;
}

void OhmicCurrentBase::setReversalPotential(mesh::triangle_id_t triangle, osh::Real value) {
    reversal_potentials.emplace(triangle, value);
}

void OhmicCurrentBase::reset() {
    reversal_potentials.clear();
}

#ifdef USE_PETSC

PetscReal OhmicCurrentBase::getTriCurrentOnVertex(const osh::Real potential_on_vertex,
                                                  const mesh::triangle_id_t& b_id,
                                                  const MolState& mol_state,
                                                  const DistMesh& mesh,
                                                  const osh::Real sim_time) const {
    // A tri split among the vertexes
    const double Avert = mesh.getTri(b_id).area / 3.0;
    const PetscReal tri_oc_bc = getTriBConVertex(b_id, mol_state, Avert, sim_time);

    return tri_oc_bc * (potential_on_vertex - getReversalPotential(b_id));
}

PetscReal OhmicCurrent::getTriBConVertex(const mesh::triangle_id_t& b_id,
                                         const MolState& mol_state,
                                         const double Avert,
                                         const osh::Real sim_time) const {
    const auto avg_open_channels =
        channel_state ? mol_state.get_occupancy_ef(b_id, *channel_state, sim_time) / 3.0 : Avert;

    return avg_open_channels * conductance;
}

PetscReal ComplexOhmicCurrent::getTriBConVertex(const mesh::triangle_id_t& b_id,
                                                const MolState& mol_state,
                                                const double /*Avert*/,
                                                const osh::Real sim_time) const {
    const auto avg_open_channels = mol_state.get_occupancy_ef(b_id, occupancy_id, sim_time) / 3.0;

    return avg_open_channels * conductance;
}

#endif  // USE_PETSC

Membrane::Membrane(Statedef& statedef_, const DistMemb& membrane)
    : statedef(statedef_)
    , patches_(membrane.patches().begin(), membrane.patches().end())
    , capacitance_(membrane.getCapacitance())
    , current_([](auto) { return 0.0; }) {
    for (const auto& patchId: patches_) {
        const auto& patch = statedef.mesh().getPatch(patchId);
        auto& patchdef = statedef.getPatchdef(patchId);
        for (auto& ssysName: patch.getSurfsys()) {
            auto& ssys = statedef.model().getSurfsys(ssysName);
            // Ohmic currents
            for (auto& [currId, curr]: ssys._getAllOhmicCurrs()) {
                auto& chanstate = curr->getChanState();
                auto& chan = addChannel(chanstate.getChan().getID());

                auto stateContId = patchdef.getSpecContainerIdx(chanstate);
                auto& currdef = statedef_.addOhmicCurrent(model::ohmic_current_id(currId),
                                                          stateContId,
                                                          curr->getG(),
                                                          curr->getERev());
                chan.addOhmicCurrent(currdef);
            }
            for (auto& [currId, curr]: ssys._getAllComplexOhmicCurrs()) {
                auto& filt = curr->getChanState();
                auto& chan = addChannel(filt.complexId);

                ComplexFilterDescr filtDescr(filt, statedef);
                auto& currdef = statedef_.addComplexOhmicCurrent(model::ohmic_current_id(currId),
                                                                 filtDescr,
                                                                 curr->getG(),
                                                                 curr->getERev());
                chan.addOhmicCurrent(currdef);
            }
            // GHK currents
            auto checkCurr = [](const auto& curr) {
                if (not curr->_infosupplied()) {
                    std::ostringstream msg;
                    msg << "GHK current " << curr->getID() << ": Undefined permeability.";
                    throw std::invalid_argument(msg.str());
                }
                if (not curr->_realflux()) {
                    throw std::invalid_argument(
                        "GHK currents in distributed STEPS do not support "
                        "the computeflux=False argument.");
                }
                if (curr->_vshift() != 0.0) {
                    throw std::invalid_argument(
                        "GHK currents in distributed STEPS do not support "
                        "the vshift argument.");
                }
            };
            for (auto& [currId, curr]: ssys._getAllGHKcurrs()) {
                checkCurr(curr);

                auto& chanstate = curr->getChanState();
                auto& chan = addChannel(chanstate.getChan().getID());

                auto& currdef = statedef_.addGHKCurrent(model::ghk_current_id(currId),
                                                        model::species_name(chanstate.getID()),
                                                        model::species_name(curr->getIon().getID()),
                                                        curr->_valence());
                chan.addGHKCurrent(currdef);
                patchdef.addGHKReacs(*curr);
            }
            for (auto& [currId, curr]: ssys._getAllComplexGHKcurrs()) {
                checkCurr(curr);

                auto& filt = curr->getChanState();
                auto& chan = addChannel(filt.complexId);
                ComplexFilterDescr filtDescr(filt, statedef);
                auto& currdef =
                    statedef_.addComplexGHKCurrent(model::ghk_current_id(currId),
                                                   filtDescr,
                                                   model::species_name(curr->getIon().getID()),
                                                   curr->_valence());
                chan.addComplexGHKCurrent(currdef);
                patchdef.addGHKReacs(*curr);
            }
        }
    }
}

Channel& Membrane::addChannel(const std::string& name) {
    model::channel_id chanId(name);
    auto it = channels_.find(chanId);
    if (it == channels_.end()) {
        it = channels_.emplace(chanId, Channel{}).first;
    }
    return it->second;
}

std::ostream& operator<<(std::ostream& os, OhmicCurrent const& m) {
    return os << "OhmicCurrent.conductance: " << m.conductance
              << "\nOhmicCurrent.reversal_potential: " << m.reversal_potential
              << "\nOhmicCurrent.channel_state: "
              << (m.channel_state ? std::to_string(*m.channel_state) : "not assigned") << '\n';
}

std::ostream& operator<<(std::ostream& os, GHKCurrent const& m) {
    return os << "GHKCurrent.ion_channel_state: " << m.ion_channel_state
              << "\nGHKCurrent.ion_id: " << m.ion_id << "\nGHKCurrent.valence: " << m.valence
              << '\n';
}

std::ostream& operator<<(std::ostream& os, Channel const& m) {
    os << "\nChannel.ohmic_currents.size(): " << m.ohmic_currents.size() << '\n';
    for (const auto& i: m.ohmic_currents) {
        os << i;
    }
    os << "Channel.ghk_currents.size(): " << m.ghk_currents.size() << '\n';
    for (const auto& i: m.ghk_currents) {
        os << i;
    }
    return os;
}

#ifdef USE_PETSC

std::ostream& operator<<(std::ostream& os, const TriMatAndVecs& obj) {
    os << "vert_idxs:\n";
    for (const auto i: obj.face_bf2vertsPETSc) {
        os << i << ' ';
    }
    os << '\n';
    os << "triStiffnessMat:\n";
    for (size_t i = 0; i < 3; ++i) {
        for (size_t j = 0; j < 3; ++j) {
            os << obj.triStiffnessPETSc[3 * j + i] << ' ';
        }
        os << '\n';
    }
    os << "triBC:\n";
    for (const auto i: obj.triBC) {
        os << i << ' ';
    }
    os << '\n';
    os << "triI:\n";
    for (const auto i: obj.triI) {
        os << i << ' ';
    }
    os << '\n';

    return os;
}

#endif  // USE_PETSC

}  // namespace steps::dist
