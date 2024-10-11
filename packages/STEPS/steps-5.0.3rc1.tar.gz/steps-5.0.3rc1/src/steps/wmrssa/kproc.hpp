/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <fstream>
#include <vector>

// STEPS headers.
#include "solver/reacdef.hpp"
#include "solver/sreacdef.hpp"

namespace steps::wmrssa {

// Forward declaration
class Comp;
class Patch;
class KProc;

typedef wmrssa::KProc* KProcP;
typedef std::vector<KProcP> KProcPVec;
typedef KProcPVec::iterator KProcPVecI;
typedef KProcPVec::const_iterator KProcPVecCI;

enum PropensityRSSA { CURRENT, LOWERBOUND, BOUNDS };

class KProc

{
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    virtual ~KProc() = default;

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

    inline solver::kproc_global_id schedIDX() const noexcept {
        return pSchedIDX;
    }

    inline void setSchedIDX(solver::kproc_global_id idx) noexcept {
        pSchedIDX = idx;
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    /// This function is called when all kproc objects have been created,
    /// allowing the kproc to pre-compute its SchedIDXVec.
    ///
    virtual void setupDeps() = 0;

    virtual bool depSpecComp(solver::spec_global_id gidx, Comp* comp) = 0;
    virtual bool depSpecPatch(solver::spec_global_id gidx, Patch* patch) = 0;

    /// Reset this Kproc.
    ///
    virtual void reset() = 0;

    // Recompute the Ccst for this KProc
    virtual void resetCcst() = 0;

    /// Compute the rate for this kproc (its propensity value).
    ///
    virtual double rate(PropensityRSSA prssa = CURRENT) = 0;

    // Return the ccst for this kproc
    virtual double c() const = 0;

    // Return the lower bound on propensity for this kproc
    virtual double propensityLB() const = 0;

    // Return the h value for this kproc (number of available reaction channels)
    virtual double h() = 0;

    /// Apply a single discrete instance of the kinetic process, returning
    /// a vector of kproc schedule indices that need to be updated as a
    /// result.
    ///
    virtual std::vector<solver::kproc_global_id> const& apply() = 0;

    virtual uint updVecSize() const = 0;

    ////////////////////////////////////////////////////////////////////////

    inline unsigned long long getExtent() const noexcept {
        return rExtent;
    }
    inline void resetExtent() noexcept {
        rExtent = 0;
    }

    ////////////////////////////////////////////////////////////////////////

    // Return a pointer to the corresponding Reacdef or SReacdef object
    // Separate methods to avoid makeing a base KProcdef class
    //
    virtual solver::Reacdef* defr() const;
    virtual solver::SReacdef* defsr() const;

    ////////////////////////////////////////////////////////////////////////

  protected:
    unsigned long long rExtent{0};

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::kproc_global_id pSchedIDX{0u};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmrssa
