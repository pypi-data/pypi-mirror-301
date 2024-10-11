/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "kproc.hpp"
#include "solver/sreacdef.hpp"

namespace steps::wmrssa {

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

    inline bool inactive() const noexcept {
        return !active();
    }

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;
    bool depSpecComp(solver::spec_global_id gidx, Comp* comp) override;
    bool depSpecPatch(solver::spec_global_id gidx, Patch* patch) override;
    void reset() override;
    double rate(wmrssa::PropensityRSSA prssa = wmrssa::CURRENT) override;
    std::vector<solver::kproc_global_id> const& apply() override;

    ////////////////////////////////////////////////////////////////////////

    inline solver::SReacdef* defsr() const noexcept override {
        return pSReacdef;
    }

    void resetCcst() override;

    inline double c() const noexcept override {
        return pCcst;
    }

    inline double propensityLB() const noexcept override {
        return pPropensityLB;
    }

    inline double h() noexcept override {
        return rate() / pCcst;
    }

    uint updVecSize() const override {
        return pUpdVec.size();
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::SReacdef* pSReacdef;
    Patch* pPatch;
    std::vector<solver::kproc_global_id> pUpdVec;

    /// Properly scaled reaction constant.
    double pCcst{0.0};
    double pPropensityLB{0.0};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmrssa
