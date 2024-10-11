#pragma once
/**
 * \file reactions.hpp
 * Provide the \a Reactions class
 */

#include <cmath>
#include <functional>
#include <random>
#include <vector>

#include "../mol_state.hpp"

#include "fwd.hpp"
#include "geom/dist/fwd.hpp"
#include "mpi/dist/tetopsplit/definition/compdef.hpp"
#include "mpi/dist/tetopsplit/definition/diffdef.hpp"
#include "mpi/dist/tetopsplit/definition/fwd.hpp"
#include "mpi/dist/tetopsplit/definition/reacdef.hpp"
#include "mpi/dist/tetopsplit/definition/statedef.hpp"
#include "reactions_iterator.hpp"
#include "solver/fwd.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist::kproc {

static std::vector<MolStateComplexElementID> empty_complex_element_id{};

template <typename RDefT>
class ReactionsBase {
  public:
    using iterator_type = reactions_iterator<ReactionsBase>;
    using const_iterator_type = reactions_iterator<const ReactionsBase>;
    /**
     *
     * \param statedef model definition
     * \param mesh distributed mesh object
     */
    ReactionsBase(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : measureInfo(mesh.getMeasure()) {
        const auto& owned_elems_mask = mesh.owned_elems_mask();

        for (const auto& compartment: statedef.compdefs()) {
            const auto& elements = mesh.getEntities(compartment->getID());
            for (auto k: elements) {
                if (owned_elems_mask[k.get()] != 0) {
                    addReactions(*compartment, mol_state, k);
                }
            }
        }
    }

    virtual ~ReactionsBase() = default;

    size_t size() const noexcept {
        return ownerPoints_.size();
    }
    mesh::tetrahedron_id_t getOwnerPoint(size_t index) const noexcept {
        return ownerPoints_[index];
    }
    const RDefT& getReacDef(size_t index) const noexcept {
        return reacdefs_[index];
    }

    void report(std::ostream& report_stream, size_t index) const {
        getReacDef(index).report(report_stream, ownerPoints_[index]);
    }

    /**
     * \brief Compute the rate of the KProc.
     */
    virtual osh::Real computeRate(const MolState& mol_state, size_t index) const {
        const auto& lhs = reacdefs_[index].get().getPoolChangeLHS();

        osh::Real h_mu = 1.0;
        const container::species_id num_species(
            static_cast<container::species_id::value_type>(lhs.size()));

        for (auto species: lhs.range()) {
            osh::I64 lhs_s = -lhs[species];

            if (lhs_s == 0) {
                continue;
            }
            auto pool_s = mol_state(this->getOwnerPoint(index), species);

            if (lhs_s > pool_s) {
                h_mu = 0.0;
                break;
            }
            switch (lhs_s) {
            case 4: {
                h_mu *= static_cast<osh::Real>(pool_s - 3);
                OMEGA_H_FALLTHROUGH;
            }
            case 3: {
                h_mu *= static_cast<osh::Real>(pool_s - 2);
                OMEGA_H_FALLTHROUGH;
            }
            case 2: {
                h_mu *= static_cast<osh::Real>(pool_s - 1);
                OMEGA_H_FALLTHROUGH;
            }
            case 1: {
                h_mu *= static_cast<osh::Real>(pool_s);
                break;
            }
            default: {
                throw std::runtime_error("Reaction rate computation error");
            }
            }
        }

        return h_mu * ccsts_[index];
    }

    virtual const std::vector<MolStateElementID>& updateMolStateAndOccupancy(
        MolState& mol_state,
        rng::RNG& /*rng*/,
        size_t index,
        osh::Real event_time) const {
        const auto& upd = reactions_upd_[index];
        const auto& stoichoimetry = stoichiometry_change_[index];


        for (size_t k = 0; k < upd.size(); k++) {
            const auto& elmt = upd[k];
            const auto& s = stoichoimetry[k];

            // mol_state(elmt) +s is the new mols count. It cannot go negative
            assert(mol_state(elmt) >= -s);
            assert(mol_state(elmt) <= std::numeric_limits<molecules_t>::max() - std::max(s, {}));
            mol_state.add_and_update_occupancy(elmt, static_cast<osh::LO>(s), event_time);
        }
        return upd;
    }

    /**
     * \brief Returns a list of molecular state elements that effect the
     * propensity of the reaction index.
     */
    const std::vector<MolStateElementID>& getPropensityDependency(size_t index) const noexcept {
        return reactions_lhs_[index];
    }

    /**
     * \brief Returns a list of complex molecular state elements that effect the
     * propensity of the reaction index.
     */
    virtual const std::vector<MolStateComplexElementID>& getComplexPropensityDependency(
        size_t) const noexcept {
        return empty_complex_element_id;
    }

    /**
     * \brief Returns a list of molecular state elements updated in the
     * event of the reaction identified by the index occuring.
     */
    const std::vector<MolStateElementID>& getMolStateElementsUpdates(size_t index) const noexcept {
        return reactions_upd_[index];
    }

    /**
     * \brief Returns a list of complex molecular state elements updated in the
     * event of the reaction identified by the index occuring.
     */
    virtual const std::vector<MolStateComplexElementID>& getComplexElementsUpdates(
        size_t) const noexcept {
        return empty_complex_element_id;
    }

    /// \return an iterator to the beginning
    iterator_type begin() noexcept {
        return {*this, size_t{0}};
    }


    /// \return an iterator to the end
    iterator_type end() noexcept {
        return {*this, this->size()};
    }

    /// \return an iterator to the beginning
    const_iterator_type begin() const noexcept {
        return {*this};
    }

    /// \return an iterator to the end
    const_iterator_type end() const noexcept {
        return {*this, this->size()};
    }

  protected:
    void addReactions(const Compdef& comp, MolState& mol_state, const mesh::tetrahedron_id_t& tet) {
        for (const auto& reacdef: comp.reacdefs<RDefT>()) {
            reacdefs_.emplace_back(*reacdef);
            ownerPoints_.push_back(tet);
            ccsts_.push_back(compute_ccst(*reacdef, tet));
            std::vector<osh::I64> stoichiometry_change;
            std::vector<MolStateElementID> reaction_upd;
            std::vector<MolStateElementID> reaction_lhs;
            const auto& upd_array = reacdef->getPoolChangeUPD();
            for (auto spec: upd_array.range()) {
                if (upd_array[spec] != 0) {
                    reaction_upd.emplace_back(tet, spec);
                    stoichiometry_change.push_back(upd_array[spec]);

                    // track occupancy if the molecule can diffuse (here we have only
                    // molecules, not channel states)
                    if (comp.isDiffused(spec)) {
                        mol_state.track_occupancy_rd(tet, spec);
                    }
                }
            }
            const auto& lhs_array = reacdef->getPoolChangeLHS();
            for (auto spec: lhs_array.range()) {
                if (lhs_array[spec] != 0) {
                    reaction_lhs.emplace_back(tet, spec);
                }
            }
            reactions_upd_.push_back(reaction_upd);
            reactions_lhs_.push_back(reaction_lhs);
            stoichiometry_change_.push_back(stoichiometry_change);
        }
    }

    /**
     * \brief Reaction rate constant in the particular mesh element.
     * Multiplier of the propensity of the reaction in the mesh element.
     *
     * \param reacdef definition of the reaction
     * \param element index of a mesh element
     * \return the reaction rate constant.
     */
    osh::Real compute_ccst(const RDefT& reacdef, mesh::tetrahedron_id_t element) const {
        const auto measure = measureInfo.element_measure(element);
        osh::Real scale = 1.0e3 * measure * math::AVOGADRO;
        osh::I64 o1 = reacdef.getOrder() - 1;
        osh::Real ccst = reacdef.getKcst() * std::pow(scale, static_cast<osh::Real>(-o1));
        return ccst;
    }

    std::vector<std::reference_wrapper<RDefT>> reacdefs_;
    std::vector<mesh::tetrahedron_id_t> ownerPoints_;
    std::vector<osh::Real> ccsts_;
    std::vector<std::vector<MolStateElementID>> reactions_upd_;
    /// species-element id of each reactant in the ith surface reaction
    std::vector<std::vector<MolStateElementID>> reactions_lhs_;
    std::vector<std::vector<osh::I64>> stoichiometry_change_;

    const Measure& measureInfo;
};


class Reactions: public ReactionsBase<Reacdef> {
  public:
    Reactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : ReactionsBase<Reacdef>::ReactionsBase(statedef, mesh, mol_state) {}

    constexpr KProcType getKProcType() const noexcept {
        return KProcType::Reac;
    }
};


class ComplexReactions: public ReactionsBase<ComplexReacdef> {
  public:
    ComplexReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : ReactionsBase<ComplexReacdef>::ReactionsBase(statedef, mesh, mol_state) {
        const auto& owned_elems_mask = mesh.owned_elems_mask();

        for (const auto& compartment: statedef.compdefs()) {
            const auto& elements = mesh.getEntities(compartment->getID());
            for (auto k: elements) {
                if (owned_elems_mask[k.get()] != 0) {
                    addComplexReactions(*compartment, mol_state, k);
                }
            }
        }
    }

    constexpr KProcType getKProcType() const noexcept {
        return KProcType::ComplexReac;
    }

    osh::Real computeRate(const MolState& mol_state, size_t index) const override;

    const std::vector<MolStateElementID>& updateMolStateAndOccupancy(
        MolState& mol_state,
        rng::RNG& rng,
        size_t index,
        osh::Real event_time) const override;

    /**
     * \brief Returns a list of complex molecular state elements that effect the
     * propensity of the reaction index.
     */
    const std::vector<MolStateComplexElementID>& getComplexPropensityDependency(
        size_t index) const noexcept override {
        return complex_reactions_deps[index];
    }

    /**
     * \brief Returns a list of complex molecular state elements updated in the
     * event of the reaction identified by the index occuring.
     */
    const std::vector<MolStateComplexElementID>& getComplexElementsUpdates(
        size_t index) const noexcept override {
        return complex_reactions_upds[index];
    }

  private:
    void addComplexReactions(const Compdef& comp,
                             MolState& mol_state,
                             const mesh::tetrahedron_id_t& tet);

    std::vector<std::vector<ComplexLHSCandidates<mesh::tetrahedron_id_t>>> candidates;
    std::vector<std::vector<MolStateComplexElementID>> complex_reactions_deps;
    std::vector<std::vector<MolStateComplexElementID>> complex_reactions_upds;
};

}  // namespace steps::dist::kproc
