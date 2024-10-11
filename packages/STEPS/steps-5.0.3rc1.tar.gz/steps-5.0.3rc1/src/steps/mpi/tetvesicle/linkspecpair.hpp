/*
 ___license_placeholder___
 */

#pragma once

// Standard library & STL headers.
#include <fstream>
#include <map>
#include <string>
#include <vector>

// STEPS headers.
#include "math/constants.hpp"
#include "math/point.hpp"
#include "mpi/tetvesicle/vesicle.hpp"
#include "solver/linkspecdef.hpp"

namespace steps::mpi::tetvesicle {

class LinkSpec;

class LinkSpecPair {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    // What info do we ned here?
    LinkSpecPair(LinkSpec* linkspec1,
                 LinkSpec* linkspec2,
                 Vesicle* ves1,
                 Vesicle* ves2,
                 double min_length,
                 double max_length);

    LinkSpecPair(std::fstream& cp_file, TetVesicleVesRaft* solver);

    ~LinkSpecPair();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file) const;

    /// restore is done by 2nd constructor

    ////////////////////////////////////////////////////////////////////////

    inline LinkSpec* getLinkSpec1() const noexcept {
        return pLinkSpec1;
    }
    inline LinkSpec* getLinkSpec2() const noexcept {
        return pLinkSpec2;
    }

    solver::linkspec_individual_id getLinkSpecLowID() const noexcept;

    LinkSpec* getPairedLinkSpec(const LinkSpec* ls) const;

    solver::linkspec_individual_id getLinkSpec1_uniqueID() const noexcept;
    solver::linkspec_individual_id getLinkSpec2_uniqueID() const noexcept;

    inline Vesicle* getVesicle1() const noexcept {
        return pVesicle1;
    }
    inline Vesicle* getVesicle2() const noexcept {
        return pVesicle2;
    }

    inline double max_length() const noexcept {
        return pMaxLength;
    }

    inline double min_length() const noexcept {
        return pMinLength;
    }

    inline bool isSymmetric() const noexcept {
        return pIsSymmetric;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    LinkSpec* pLinkSpec1;
    LinkSpec* pLinkSpec2;

    Vesicle* pVesicle1;
    Vesicle* pVesicle2;

    double pMaxLength;
    double pMinLength;

    bool pIsSymmetric;

    ////////////////////////////////////////////////////////////////////////
};

inline bool operator<(const LinkSpecPair& lhs, const LinkSpecPair& rhs) {
    return lhs.getLinkSpecLowID() < rhs.getLinkSpecLowID();
}

}  // namespace steps::mpi::tetvesicle
