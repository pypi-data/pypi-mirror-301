/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <array>
#include <fstream>
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "kproc.hpp"
#include "math/constants.hpp"
#include "solver/diffdef.hpp"
#include "tetexact.hpp"

namespace steps::tetexact {

// Forward declarations.
class Tri;

class SDiff: public KProc {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    SDiff(solver::SurfDiffdef* sdef, Tri* tri);
    SDiff(const SDiff&) = delete;
    ~SDiff() override;

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

    inline solver::SurfDiffdef* def() const noexcept {
        return pSDiffdef;
    }

    double dcst(int direction = -1);
    void setDcst(double d);
    void setDirectionDcst(int direction, double dcst);

    void setupDeps() override;

    bool depSpecTet(solver::spec_global_id gidx, WmVol* tet) override;
    bool depSpecTri(solver::spec_global_id gidx, Tri* tri) override;

    void reset() override;
    double rate(Tetexact* solver = nullptr) override;

    std::vector<KProc*> const& apply(const rng::RNGptr& rng, double dt, double simtime) override;

    uint updVecSize() const override;

    ////////////////////////////////////////////////////////////////////////

    void setSDiffBndActive(uint i, bool active);

    bool getSDiffBndActive(uint i) const;

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    solver::spec_local_id lidxTri;
    solver::SurfDiffdef* pSDiffdef;
    Tri* pTri;
    std::vector<KProc*> pUpdVec[3];

    // Storing the species local index for each neighbouring tri: Needed
    // because neighbours may belong to different patches for
    // diffusion boundary for surfaces
    std::array<solver::spec_local_id, 3> pNeighbPatchLidx{std::nullopt, std::nullopt, std::nullopt};

    /// Properly scaled diffusivity constant.
    double pScaledDcst{};
    // Compartmental dcst. Stored for convenience
    double pDcst{};
    std::map<uint, double> directionalDcsts;

    std::array<double, 2> pCDFSelector{0.0, 0.0};

    // A flag to see if the species can move between compartments
    std::array<bool, 3> pSDiffBndActive{false, false, false};

    // Flags to store if a direction is a diffusion boundary direction
    std::array<bool, 3> pSDiffBndDirection{false, false, false};

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetexact
