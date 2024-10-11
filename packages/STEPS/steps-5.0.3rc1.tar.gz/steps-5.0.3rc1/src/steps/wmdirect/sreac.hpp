/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "kproc.hpp"
#include "solver/sreacdef.hpp"

namespace steps::wmdirect {

// Forward declarations
class Comp;
class Patch;

class SReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    SReac(solver::SReacdef* srdef, Patch* patch);
    ~SReac() override;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) override;

    /// restore data
    void restore(std::fstream& cp_file) override;

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////

    static const int INACTIVATED = 1;

    bool active() const;

    inline bool inactive() const {
        return !active();
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;
    bool depSpecComp(solver::spec_global_id gidx, Comp* comp) override;
    bool depSpecPatch(solver::spec_global_id gidx, Patch* patch) override;
    void reset() override;
    double rate() const override;
    std::vector<solver::kproc_global_id> const& apply() override;

    ////////////////////////////////////////////////////////////////////////

    inline solver::SReacdef* defsr() const noexcept override {
        return pSReacdef;
    }

    void resetCcst() override;

    inline double c() const noexcept override {
        return pCcst;
    }

    inline double h() const noexcept override {
        return rate() / pCcst;
    }

    inline uint updVecSize() const noexcept override {
        return pUpdVec.size();
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::SReacdef* pSReacdef;
    Patch* pPatch;
    std::vector<solver::kproc_global_id> pUpdVec;

    /// Properly scaled reaction constant.
    double pCcst;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmdirect
