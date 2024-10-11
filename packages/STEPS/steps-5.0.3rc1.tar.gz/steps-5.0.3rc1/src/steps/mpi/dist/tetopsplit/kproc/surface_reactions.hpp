#pragma once
/**
 * \file surface_reactions.hpp
 * Provide the \a SurfaceReactions class
 */

#include <cmath>
#include <random>
#include <vector>

#include <Omega_h_adj.hpp>

#include "../mol_state.hpp"
#include "geom/dist/distmesh.hpp"
#include "mpi/dist/tetopsplit/definition/compdef.hpp"
#include "mpi/dist/tetopsplit/definition/diffdef.hpp"
#include "mpi/dist/tetopsplit/definition/fwd.hpp"
#include "mpi/dist/tetopsplit/definition/patchdef.hpp"
#include "mpi/dist/tetopsplit/definition/reacdef.hpp"
#include "mpi/dist/tetopsplit/definition/sreacdef.hpp"
#include "mpi/dist/tetopsplit/definition/statedef.hpp"
#include "mpi/dist/tetopsplit/kproc/surface_reactions.hpp"
#include "reactions.hpp"
#include "reactions_iterator.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist::kproc {

/**
 * \brief SurfaceReactionBase is a container for regular surface reactions and
 * voltage dependent surface reactions. It factors common functionalities
 * between the two types of surface reactions.
 *
 * \tparam PropensityType either a scalar or a function that takes as input a
 * potential
 */
template <typename RDefT>
class SurfaceReactionsBase {
  public:
    using iterator_type = reactions_iterator<SurfaceReactionsBase<RDefT>>;
    using const_iterator_type = reactions_iterator<const SurfaceReactionsBase<RDefT>>;
    using _RDefT = RDefT;
    /**
     * Surface reactions constructor
     * \param statedef model definition
     * \param mesh distributed mesh
     */
    SurfaceReactionsBase(const Statedef& statedef, DistMesh& mesh, MolState& mol_state);

    virtual ~SurfaceReactionsBase() = default;

    inline size_t size() const noexcept {
        return reacdefs_.size();
    }

    inline const RDefT& getReacDef(size_t index) const noexcept {
        return reacdefs_[index];
    }

    /**
     * \brief Returns a list of molecular state elements that effect the
     * propensity of the reaction 'index'.
     */
    inline const std::vector<MolStateElementID>& getPropensityDependency(
        size_t index) const noexcept {
        return reaction_lhs_[index];
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
     * \return kind of surface reaction
     */
    static std::string name();

    /**
     * \brief Returns a list of molecular state elements updated in the
     * event of the reaction identified by the index occurring.
     */
    inline const std::vector<MolStateElementID>& getMolStateElementsUpdates(
        size_t index) const noexcept {
        return reaction_upd_[index];
    }


    /**
     * \brief Returns a list of complex molecular state elements updated in the
     * event of the reaction identified by the index occuring.
     */
    virtual const std::vector<MolStateComplexElementID>& getComplexElementsUpdates(
        size_t) const noexcept {
        return empty_complex_element_id;
    }

    inline mesh::tetrahedron_id_t getInnerCompartmentElementId(size_t index) const noexcept {
        return inner_compartment_element_id_[index];
    }

    inline const std::optional<mesh::tetrahedron_id_t>& getOuterCompartmentElementId(
        size_t index) const noexcept {
        return outer_compartment_element_id_[index];
    }


    /** Computes the exchange rate r in moles/s
     *
     * The link with the current I is: r = I/(z*F)
     * where:
     *
     * - z is the valence
     * - F is the Faraday constant = electron_charge * N_avogadro
     *
     */
    osh::Real computeRate(const MolState& mol_state, size_t index) const;

    const std::vector<MolStateElementID>& updateMolStateAndOccupancy(
        MolState& mol_state,
        rng::RNG& rng,
        size_t index,
        const osh::Real event_time) const;

    /**
     * \name Iterators
     * \{
     */

    /// \return an iterator to the beginning
    inline iterator_type begin() noexcept {
        return {*this};
    }

    /// \return an iterator to the end
    inline iterator_type end() noexcept {
        return {*this, this->size()};
    }

    /// \return an iterator to the beginning
    inline const_iterator_type begin() const noexcept {
        return {*this};
    }

    /// \return an iterator to the end
    inline const_iterator_type end() const noexcept {
        return {*this, this->size()};
    }

    /** \} */

    /**
     * \brief A report for surf. reac. index
     *
     * \param report_stream stream
     * \param index index
     */
    void report(std::ostream& report_stream, size_t index) const;

    const std::vector<mesh::triangle_id_t>& boundaries() const noexcept {
        return boundary_id_;
    }

  protected:
    /**
     * \brief Factor of the kinetic constant.
     * \param index kproc index
     * \return the geometric part of the kin constant.
     */
    osh::Real kinConstantGeomFactor(const DistMesh& mesh, size_t index) const;

    using Stoichiometry = std::vector<osh::I64>;

    template <PoolChangeType PoolChange>
    [[nodiscard]] std::
        tuple<std::vector<MolStateElementID>, Stoichiometry, std::vector<model::region_id>>
        reactionMolStateDependencyAndStoichiometry(
            const RDefT& reacdef,
            mesh::triangle_id_t patch_element_id,
            mesh::tetrahedron_id_t inner_compartment_element_id,
            const std::optional<mesh::tetrahedron_id_t>& outer_compartment_element) const;

    /// local_index of element on the patch for ith surface reaction
    std::vector<mesh::triangle_id_t> boundary_id_;
    /// local_index of element in inner compartment for ith surface reaction
    std::vector<mesh::tetrahedron_id_t> inner_compartment_element_id_;
    /// local_index of element in outer compartment for ith surface reaction
    std::vector<std::optional<mesh::tetrahedron_id_t>> outer_compartment_element_id_;

    /**
     * \name
     * size of dim 1: number of surface reactions
     * size of dim 2: number of reactants involved
     * \{
     */
    /// species-element id of each reactant in the ith surface reaction
    std::vector<std::vector<MolStateElementID>> reaction_lhs_;
    /// stoichiometry coefficient of each reactant in the ith surface reaction
    std::vector<Stoichiometry> stoichiometry_lhs_;
    /** \} */

    /**
     * \name
     * size of dim 1: number of surface reactions
     * size of dim 2: number of species involved
     * \{
     */
    /// species-element id of each species in the ith surface reaction
    std::vector<std::vector<MolStateElementID>> reaction_upd_;
    /// stoichiometry difference of each species in the ith surface reaction
    /// \TODO TCL: might be able to reduce memory footprint by accessing directly
    /// in reacdefs
    std::vector<Stoichiometry> stoichiometry_upd_;
    /** \} */

    /// reaction definition for the ith surface reaction
    std::vector<std::reference_wrapper<RDefT>> reacdefs_;
    /// propensity rate constant for ith surface reaction
    std::vector<osh::Real> ccsts_;

    const Statedef& state_def_;
};

//-------------------------------------------------------

/**
 * \brief Generic class for surface reactions with rate constant
 *
 * \tparam RDefT surface reaction definition class
 */
template <typename RDefT>
class ConstantSurfaceReactions: public SurfaceReactionsBase<RDefT> {
  public:
    ConstantSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state);

    void updateKCst(const model::patch_id& patch_id,
                    container::surface_reaction_id id,
                    osh::Real kCst,
                    DistMesh& mesh) {
        for (size_t k = 0; k < this->size(); k++) {
            if (patch_id == this->reacdefs_[k].get().patchdef().getID() &&
                this->reacdefs_[k].get().surfaceReactionID() == id) {
                this->ccsts_[k] = this->kinConstantGeomFactor(mesh, k) * kCst;

                // If you reach these asserts probably your mesh is too big/too small or
                // kcst is an invalid value
                assert(this->ccsts_[k] != std::numeric_limits<double>::infinity());
                assert(this->ccsts_[k] >= 0);
            }
        }
    }

  private:
    void updateCcst(DistMesh& mesh);
};

//-------------------------------------------------------

class SurfaceReactions: public ConstantSurfaceReactions<SReacdef> {
  public:
    SurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : ConstantSurfaceReactions<SReacdef>::ConstantSurfaceReactions(statedef, mesh, mol_state) {}

    inline constexpr KProcType getKProcType() const {
        return KProcType::SReac;
    }
};

//-------------------------------------------------------

template <typename RDefT>
class VDepSurfaceReactionsBase: public SurfaceReactionsBase<RDefT> {
  public:
    VDepSurfaceReactionsBase(const Statedef& statedef, DistMesh& mesh, MolState& mol_state);

    void kCstUpdate(osh::Reals& potential_on_verts);

  private:
    std::vector<osh::Real> kinConstantGeomFactor_;
    const osh::LOs tri2verts_;
};

//-------------------------------------------------------

class VDepSurfaceReactions: public VDepSurfaceReactionsBase<VDepSReacdef> {
  public:
    VDepSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : VDepSurfaceReactionsBase(statedef, mesh, mol_state) {}

    inline constexpr KProcType getKProcType() const noexcept {
        return KProcType::VDepSReac;
    }
};

//-------------------------------------------------------

/**
 * \brief Generic class for GHK surface reactions
 *
 * \tparam RDefT GHK surface reaction definition class
 */
template <typename RDefT>
class GHKSurfaceReactionsBase: public SurfaceReactionsBase<RDefT> {
  public:
    GHKSurfaceReactionsBase(const Statedef& statedef, DistMesh& mesh, MolState& mol_state);

    /** Get currents
     *
     * /Note: This must be called after finalizeCurrents. Otherwise we get the charge flow not the
     * currents
     */
    inline const auto& currents() const noexcept {
        return currents_;
    }

    const osh::Write<osh::GO>& getTri2Curr(const model::ghk_current_id& curr_id) const;

    void updatePotential(osh::Reals& potential_on_verts);

    void resetCurrents();

    /** Update currents_ with the net charge flow for the particular reaction
     *
     * /Note: when this function is called currents_ is actually the count of charge exchanged
     * during the time step. Only after finalizeCurrents we get the real currents
     *
     * /param reaction_index
     */
    void updateChargeFlow(size_t reaction_index);

    /**  Rescale currents by the period
     *
     * Before this function is called the currents are actually measured in
     * Coulomb and represent the total charge flow for a particular reaction. In formulae:
     *
     * i (before rescaling) = n_reactions_in_ef_dt * valence * Q_charge.
     *
     * where the valence is the net exchange of charges per reaction. It is usually the same as the
     * ion valence except if multiple ions are involved.
     *
     * @param period it is the efield_dt
     */
    void finalizeCurrents(double period) {
        const auto rescaleByThePeriod = OMEGA_H_LAMBDA(osh::LO reac_idx) {
            currents_[reac_idx] /= period;
        };
        osh::parallel_for(currents_.size(), rescaleByThePeriod);
    }

    // Number of specific ghk reactions per triangle (inward and outward)
    constexpr uint rpt() const {
        return 2;
    }

  protected:
    /** Compute the GHK-voltage dependent reaction rate
     *
     * the concentrations are in n_molecules/m^3
     *
     * The GHK current is split in 2 reactions (as it is the case in general for
     * the rest of the code, not steps 3). Thus, the return value is a pair with
     * sign that depends on which direction the GHK current is flowing. Baudouin
     * verified the signs very carefully (since he solved a bug on these
     * currents where the sign was swapped).
     *
     * the rate is: permeability [m/s] * nuFoRT [1] * (conc_i - conc_o *
     * eNuFoRT) [n_molecules/m^3] * n_channels [1] = J [A/m^2]/(valence [1] *
     * Q_charge [C])
     *
     * This comes from a comparison with the GHK current formula on wikipedia.
     * In fact, confronting the 2 equations we have: rate = J [A/m^2] *
     * N_avogadro [mol] /(valence [1] * FARADAY [A/mol]).
     *
     * Since Q_charge [C] * N_avogadro [mol] = FARADAY we have the
     * aforementioned dimensional formula for the rate: J [A/m^2]/(valence [1] *
     * Q_charge [C])
     *
     * @return rate: J [A/m^2]/(valence [1] * Q_charge [C])
     */
    inline osh::Real ghkRate(const GHKInfo& info,
                             size_t index,
                             double conc_i,
                             double conc_o,
                             double nbOpenChan) const;

    /// a mapping from a triangle id to its vertices ids
    const osh::LOs tri2verts_;
    /// a mapping from a reaction index to a ghk current
    osh::Write<osh::Real> currents_;
    /// a mapping from a reaction index to the inner element volume
    osh::Reals inner_element_vol_;
    /// a mapping from a reaction index to the outer element volume
    osh::Reals outer_element_vol_;
    /// a mapping from a reaction index to the potential on the triangle
    osh::Write<osh::Real> potential_on_boundary_;

    /// a mapping from a ghk current identifier to a tri to reaction idx mapping
    /// the second mapping associates a local tri id to 2 reaction indices
    /// (corresponding to the inward and outward GHK reactions)
    // TODO use strong id for the value
    std::map<model::ghk_current_id, osh::Write<osh::GO>> curr2tri2reac_;
};

//-------------------------------------------------------

class GHKSurfaceReactions: public GHKSurfaceReactionsBase<GHKSReacdef> {
  public:
    GHKSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : GHKSurfaceReactionsBase<GHKSReacdef>::GHKSurfaceReactionsBase(statedef, mesh, mol_state) {
    }

    osh::Real computeRate(const MolState& mol_state, size_t index) const;

    inline constexpr KProcType getKProcType() const noexcept {
        return KProcType::GHKSReac;
    }
};

//-------------------------------------------------------

class ComplexGHKSurfaceReactions: public GHKSurfaceReactionsBase<ComplexGHKSReacdef> {
  public:
    ComplexGHKSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state);

    osh::Real computeRate(const MolState& mol_state, size_t index) const;

    inline constexpr KProcType getKProcType() const noexcept {
        return KProcType::ComplexGHKSReac;
    }

    /**
     * \brief Returns a list of complex molecular state elements that effect the
     * propensity of the reaction index.
     */
    const std::vector<MolStateComplexElementID>& getComplexPropensityDependency(
        size_t index) const noexcept {
        return complex_reactions_deps[index];
    }

  private:
    std::vector<ComplexLHSCandidates<mesh::triangle_id_t>> surface_candidates;
    std::vector<std::vector<MolStateComplexElementID>> complex_reactions_deps;
};

//-------------------------------------------------------

/**
 * \brief Generic class for complex surface reactions
 *
 * \tparam surfReacT Surface reaction base class to which complex candidates should be added
 */
template <typename surfReacT>
class ComplexSurfaceReactionsBase: public surfReacT {
  public:
    ComplexSurfaceReactionsBase(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : surfReacT(statedef, mesh, mol_state) {
        for (uint i = 0; i < this->reacdefs_.size(); ++i) {
            addComplexSurfaceReaction(this->reacdefs_[i],
                                      mol_state,
                                      this->inner_compartment_element_id_[i],
                                      this->outer_compartment_element_id_[i],
                                      this->boundary_id_[i]);
        }
    }

    osh::Real computeRate(const MolState& mol_state, size_t index) const;

    const std::vector<MolStateElementID>& updateMolStateAndOccupancy(MolState& mol_state,
                                                                     rng::RNG& rng,
                                                                     size_t index,
                                                                     osh::Real event_time) const;

    /**
     * \brief Returns a list of complex molecular state elements that effect the
     * propensity of the reaction index.
     */
    const std::vector<MolStateComplexElementID>& getComplexPropensityDependency(
        size_t index) const noexcept {
        return complex_reactions_deps[index];
    }

    /**
     * \brief Returns a list of complex molecular state elements updated in the
     * event of the reaction identified by the index occuring.
     */
    const std::vector<MolStateComplexElementID>& getComplexElementsUpdates(
        size_t index) const noexcept {
        return complex_reactions_upds[index];
    }

  private:
    void addComplexSurfaceReaction(const typename surfReacT::_RDefT& reacdef,
                                   MolState& mol_state,
                                   const mesh::tetrahedron_id_t& tet_in,
                                   const std::optional<mesh::tetrahedron_id_t>& tet_out,
                                   const mesh::triangle_id_t& tri);

    std::vector<std::vector<ComplexLHSCandidates<mesh::tetrahedron_id_t>>> inner_candidates;
    std::vector<std::vector<ComplexLHSCandidates<mesh::tetrahedron_id_t>>> outer_candidates;
    std::vector<std::vector<ComplexLHSCandidates<mesh::triangle_id_t>>> surface_candidates;
    std::vector<std::vector<MolStateComplexElementID>> complex_reactions_deps;
    std::vector<std::vector<MolStateComplexElementID>> complex_reactions_upds;
};

//-------------------------------------------------------

class ComplexSurfaceReactions
    : public ComplexSurfaceReactionsBase<ConstantSurfaceReactions<ComplexSReacdef>> {
  public:
    ComplexSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : ComplexSurfaceReactionsBase<ConstantSurfaceReactions<ComplexSReacdef>>(statedef,
                                                                                 mesh,
                                                                                 mol_state) {}
    constexpr KProcType getKProcType() const noexcept {
        return KProcType::ComplexSReac;
    }
};

//-------------------------------------------------------

class VDepComplexSurfaceReactions
    : public ComplexSurfaceReactionsBase<VDepSurfaceReactionsBase<VDepComplexSReacdef>> {
  public:
    VDepComplexSurfaceReactions(const Statedef& statedef, DistMesh& mesh, MolState& mol_state)
        : ComplexSurfaceReactionsBase<VDepSurfaceReactionsBase<VDepComplexSReacdef>>(statedef,
                                                                                     mesh,
                                                                                     mol_state) {}
    constexpr KProcType getKProcType() const noexcept {
        return KProcType::VDepComplexSReac;
    }
};

}  // namespace steps::dist::kproc
