/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/vdepsreacdef.hpp"

namespace steps::tetexact {

// Forward declarations.
class Tri;
class Tetexact;

class VDepSReac: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    VDepSReac(solver::VDepSReacdef* vdsrdef, Tri* tri);
    VDepSReac(const VDepSReac&) = delete;
    ~VDepSReac() override;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) override;

    /// restore data
    void restore(std::fstream& cp_file) override;

    ////////////////////////////////////////////////////////////////////////
    // VIRTUAL INTERFACE METHODS
    ////////////////////////////////////////////////////////////////////////

    void setupDeps() override;
    bool depSpecTet(solver::spec_global_id gidx, WmVol* tet) override;
    bool depSpecTri(solver::spec_global_id gidx, Tri* tri) override;
    void reset() override;

    double rate(Tetexact* solver = nullptr) override;
    std::vector<KProc*> const& apply(const rng::RNGptr& rng, double dt, double simtime) override;

    uint updVecSize() const noexcept override {
        return static_cast<uint>(pUpdVec.size());
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::VDepSReacdef* pVDepSReacdef;
    Tri* pTri;
    std::vector<KProc*> pUpdVec;

    // The information about the size of the comaprtment or patch, and the
    // dimensions. Important for scaling the constant.
    // As volumes and areas currently don't change this can be stored as
    // a constant.
    double pScaleFactor;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetexact
