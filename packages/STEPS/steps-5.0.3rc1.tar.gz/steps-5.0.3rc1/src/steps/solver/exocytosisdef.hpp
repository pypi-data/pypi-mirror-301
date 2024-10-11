/*
 ___license_placeholder___
 */

#pragma once

#include <iosfwd>
#include <map>
#include <string>
#include <vector>

#include "fwd.hpp"
#include "model/fwd.hpp"
#include "solver/fwd.hpp"
#include "util/vocabulary.hpp"

namespace steps::solver {

// Events struct
class ExocytosisEvent {
  public:
    ExocytosisEvent()
        : time(0)
        , vidx(vesicle_individual_id::unknown_value())
        , tidx(triangle_global_id::unknown_value())
        , ridx(raft_individual_id::unknown_value()) {}
    ExocytosisEvent(double t, vesicle_individual_id v, triangle_global_id ti, raft_individual_id r)
        : time(t)
        , vidx(v)
        , tidx(ti)
        , ridx(r) {}
    double time;
    vesicle_individual_id vidx;
    triangle_global_id tidx;
    raft_individual_id ridx;
};

/// Defined Exocytosis Reaction.
class Exocytosisdef {
  public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the exocytotic reaction.
    /// \param endo Reference to the Exocytosis object.
    Exocytosisdef(Statedef& sd, exocytosis_global_id idx, model::Exocytosis& exo);

    Exocytosisdef(const Exocytosisdef&) = delete;
    Exocytosisdef& operator=(const Exocytosisdef&) = delete;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: EXOCYTOTIC REACTION RULE
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of this exocytotic reaction rule.
    inline exocytosis_global_id gidx() const noexcept {
        return pIdx;
    }

    /// Return the name of the exocytotic reaction.
    inline std::string const& name() const noexcept {
        return pName;
    }

    /// Return the MACROscopic reaction constant.
    inline double kcst() const noexcept {
        return pKcst;
    }

    void setKcst(double k);

    // Need reset function to reset extent
    void reset();

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Setup the object.
    void setup(const Statedef& sd);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: STOICHIOMETRY
    ////////////////////////////////////////////////////////////////////////

    /// Returns the number of molecules of species idx required in
    /// the surface patch (_S)
    /// to activate exocytosis.
    ///
    uint lhs_V(spec_global_id gidx) const;

    const auto& lhs_V() const noexcept {
        return pSpec_V_LHS;
    }

    uint countSpecs_V() const noexcept {
        return pSpec_V_LHS.size();
    }

    uint vdepssize() const noexcept {
        return pVDeps.size();
    }

    ////////////////////////////////////////////////////////////////////////

    /// Returns a description of how an occurrence of this exocytosis reaction
    /// depends on some surface species, defined by its global index idx, to
    /// occur.
    ///
    depT dep_V(spec_global_id gidx) const;

    inline Raftdef* raftdef() const noexcept {
        return pRaftdef;
    }

    inline bool getKissAndRun() const noexcept {
        return pKissAndRun;
    }

    inline const auto& getKissAndRunSpecChanges() const noexcept {
        return pKissAndRunSpecChanges;
    }

    inline double getKissAndRunPartRelease() const noexcept {
        return pKissAndRunPartRelease;
    }

    inline unsigned long getExtent() const noexcept {
        return pExtent;
    }

    std::vector<ExocytosisEvent> getEvents();

    inline void addEvent(double time,
                         vesicle_individual_id vidx,
                         triangle_global_id tidx,
                         raft_individual_id ridx) noexcept {
        pExtent++;
        pEvents.emplace_back(time, vidx, tidx, ridx);
    }

  private:
    const exocytosis_global_id pIdx;
    const std::string pName;
    double pKcst;
    // Store default Kcst to avoid using model object during reset()
    const double pDefaultKcst;

    bool pSetupdone{false};

    unsigned long pExtent{};

    std::vector<ExocytosisEvent> pEvents;

    ////////////////////////////////////////////////////////////////////////
    // DATA: STOICHIOMETRY
    ////////////////////////////////////////////////////////////////////////

    // Only used during setup
    const std::vector<model::Spec*>& pVDeps;
    const model::Raft* pRaft;

    // The following two are used like usual STEPS arrays to say how this
    // SSA event depends on the presence of certain species
    util::strongid_vector<spec_global_id, uint> pSpec_V_LHS;
    util::strongid_vector<spec_global_id, depT> pSpec_V_DEP;

    // Store the raft of creation as a Raftdef pointer
    Raftdef* pRaftdef{nullptr};

    // Store whether this is a kiss-and-run exocytosis event
    bool pKissAndRun;

    // Store any species that will be transfered from vesicle to membrane upon kiss-and-run
    std::map<spec_global_id, spec_global_id> pKissAndRunSpecChanges;

    // Store kiss-and-run partial release factor
    double pKissAndRunPartRelease;
};

}  // namespace steps::solver
