/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <fstream>
#include <set>
#include <vector>

// STEPS headers.
#include "rng/rng.hpp"
#include "solver/fwd.hpp"
#include "util/collections.hpp"

// TetVesicle CR header
#include "mpi/tetvesicle/crstruct.hpp"

namespace steps::mpi::tetvesicle {

// Forward declaration
class Tet;
class Tri;
class KProc;
class Vesicle;
class TetVesicleRDEF;

////////////////////////////////////////////////////////////////////////////////

typedef KProc* KProcP;
typedef std::vector<KProcP> KProcPVec;

////////////////////////////////////////////////////////////////////////////////

enum TYPE {
    KP_REAC,
    KP_SREAC,
    KP_DIFF,
    KP_SDIFF,
    KP_GHK,
    KP_VDEPSREAC,
    KP_VESBIND,
    KP_VESSREAC,
    KP_EXO,
    KP_RAFTGEN,
    KP_RAFTSREAC
};

class KProc

{
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    KProc();
    virtual ~KProc();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    virtual void checkpoint(std::fstream& cp_file);

    /// restore data
    virtual void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    static const int INACTIVATED = 1;

    inline bool active() const noexcept {
        return (pFlags & INACTIVATED) == 0;
    }
    inline bool inactive() const noexcept {
        return (pFlags & INACTIVATED) != 0;
    }
    void setActive(bool active);

    inline uint flags() const noexcept {
        return pFlags;
    }

    ////////////////////////////////////////////////////////////////////////

    solver::kproc_global_id schedIDX() const noexcept {
        return pSchedIDX;
    }

    void setSchedIDX(solver::kproc_global_id idx) noexcept {
        pSchedIDX = idx;
    }

    uint getType() const noexcept {
        return pType;
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    /// This function is called when all kproc objects have been created,
    /// allowing the kproc to pre-compute its SchedIDXVec.
    ///
    virtual void setupDeps() = 0;

    /// Reset this Kproc.
    ///
    virtual void reset() = 0;

    // Recompute the Ccst for this KProc
    virtual void resetCcst();

    /// Compute the rate for this kproc (its propensity value).
    ///
#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Woverloaded-virtual"
    virtual double rate(TetVesicleRDEF* solver = nullptr) = 0;
#pragma clang diagnostic pop
#elif defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Woverloaded-virtual"
    virtual double rate(TetVesicleRDEF* solver = nullptr) = 0;
#pragma GCC diagnostic pop
#endif


    // Return the ccst for this kproc
    // NOTE: not pure for this solver because doesn't make sense for Diff
    virtual double c() const;

    // Return the h value for this kproc (number of available reaction channels)
    // NOTE: not pure for this solver because doesn;t make sense for Diff
    virtual double h();

    unsigned long long getExtent() const;
    void resetExtent();

    ////////////////////////////////////////////////////////////////////////

    /// Apply a single discrete instance of the kinetic process, returning
    /// a vector of kproc schedule indices that need to be updated as a
    /// result.
    ///
    // NOTE: Random number generator available to this function for use
    // by Diff

#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Woverloaded-virtual"
    virtual int apply(const rng::RNGptr& rng);
    virtual int apply(const rng::RNGptr& rng, uint nmolcs);
    virtual void apply(const rng::RNGptr& rng,
                       double dt,
                       double simtime,
                       double period,
                       TetVesicleRDEF* solver = nullptr);
    virtual void apply(TetVesicleRDEF* solver);
    virtual void apply();
#pragma clang diagnostic pop
#elif defined(__GNUC__) || defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Woverloaded-virtual"
    virtual int apply(const rng::RNGptr& rng);
    virtual int apply(const rng::RNGptr& rng, uint nmolcs);
    virtual void apply(const rng::RNGptr& rng,
                       double dt,
                       double simtime,
                       double period,
                       TetVesicleRDEF* solver = nullptr);
    virtual void apply(TetVesicleRDEF* solver);
    virtual void apply();
#pragma GCC diagnostic pop
#endif

    ////////////////////////// ADDED VESICLE FUNCTIONALITY
    ////////////////////////////

    // virtual bool depLinkSpecTet(solver::linkspec_global_id /*gidx*/,
    // Tet * /*tet*/) { return false; }
    // This is replaced now by KProcDepLinkSpecTet in Tet

    // Useful for dynamic kprocs
    // virtual bool depSpecGidx(solver::spec_global_id /*spec_gidx*/) { return
    // false; } virtual bool depLinkSpecGidx(solver::linkspec_global_id
    // /*spec_gidx*/) { return false; }

    // Now need to know which tets a KProc affects so can only update dynamic
    // kprocs in that region rather than all dynamic kprocs after every move.
    // inline std::vector<Tet *> const & getConnectedTets() const
    // noexcept {return pConnectedTets; }

    // Handy vector of all species involved in this kproc
    // inline std::set<solver::spec_global_id > const & spec_gidx_change() const
    // noexcept { return pSpecChange; }

    // inline std::set<solver::linkspec_global_id  > const &
    // linkspec_gidx_change() const noexcept { return pLinkSpecChange; }

    ////////////////////// MPI FUNCTIONALITY /////////////////////

    virtual std::vector<KProc*> const& getLocalUpdVec(int direction = -1) const;
    virtual std::vector<solver::kproc_global_id> const& getRemoteUpdVec(int direction = -1) const;

    virtual void resetOccupancies() = 0;

    virtual bool getInHost() const = 0;
    virtual int getHost() const = 0;

    ////////////////////////////////////////////////////////////////////////

    // data for CR SSA
    CRKProcData crData;

  protected:
    unsigned long long rExtent;

    ////////////////////////////////////////////////////////////////////////

    uint pFlags;

    solver::kproc_global_id pSchedIDX;

    uint pType{};

    ////////////////////////////////////////////////////////////////////////
};

inline bool operator<(const KProc& lhs, const KProc& rhs) {
    return lhs.schedIDX() < rhs.schedIDX();
}

using KProcPSet = std::set<KProc*, util::DerefPtrLess<KProc>>;

}  // namespace steps::mpi::tetvesicle

namespace std {
// Compilation trap in case std::set<KProc*> is used in the code that will sort KProc instances
// by their pointer addresses, not their schedule identifier.
// Prefer KProcPSet for such usage
template <>
class set<steps::mpi::tetvesicle::KProc*> {};
}  // namespace std
