/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "kproc.hpp"
#include "solver/reacdef.hpp"

namespace steps::wmrssa {

// Forward declarations
class Patch;
class Comp;

class Reac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    Reac(solver::Reacdef* rdef, Comp* comp);
    ~Reac() override;

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
    double rate(wmrssa::PropensityRSSA prssa = wmrssa::CURRENT) override;
    std::vector<solver::kproc_global_id> const& apply() override;

    inline uint updVecSize() const noexcept override {
        return pUpdVec.size();
    }

    ////////////////////////////////////////////////////////////////////////

    inline solver::Reacdef* defr() const noexcept override {
        return pReacdef;
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

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::Reacdef* pReacdef;
    Comp* pComp;
    std::vector<solver::kproc_global_id> pUpdVec;
    std::vector<solver::kproc_global_id> emptyVec;
    /// Properly scaled reaction constant.
    double pCcst;
    double pPropensityLB{};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::wmrssa
