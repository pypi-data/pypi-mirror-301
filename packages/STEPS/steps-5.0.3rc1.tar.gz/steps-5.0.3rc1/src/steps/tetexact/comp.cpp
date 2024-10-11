/*
 ___license_placeholder___
 */

// STEPS headers.
#include "comp.hpp"
#include "model/reac.hpp"

// logging
#include "util/error.hpp"

namespace steps::tetexact {


Comp::Comp(solver::Compdef* compdef)
    : pCompdef(compdef)
    , pVol(0.0) {
    AssertLog(pCompdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

Comp::~Comp() = default;

////////////////////////////////////////////////////////////////////////////////

void Comp::checkpoint(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Comp::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

void Comp::addTet(WmVol* tet) {
    AssertLog(tet->compdef() == def());
    pTets.push_back(tet);
    pVol += tet->vol();
}

////////////////////////////////////////////////////////////////////////////////

WmVol* Comp::pickTetByVol(double rand01) const {
    if (countTets() == 0) {
        return nullptr;
    }
    if (countTets() == 1) {
        return pTets[0];
    }

    double accum = 0.0;
    double selector = rand01 * vol();
    auto t_end = endTet();
    for (auto t = bgnTet(); t != t_end; ++t) {
        accum += (*t)->vol();
        if (selector < accum) {
            return *t;
        }
    }
    AssertLog(false);
    return nullptr;
}

}  // namespace steps::tetexact
