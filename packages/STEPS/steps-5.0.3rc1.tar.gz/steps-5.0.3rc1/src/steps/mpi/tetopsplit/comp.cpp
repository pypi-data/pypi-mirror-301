/*
 ___license_placeholder___
 */

// STEPS headers.
#include "comp.hpp"
#include "model/reac.hpp"
#include "solver/compdef.hpp"
#include "wmvol.hpp"

// logging
#include "util/error.hpp"

#include "util/checkpointing.hpp"

namespace steps::mpi::tetopsplit {

Comp::Comp(solver::Compdef* compdef)
    : pCompdef(compdef) {
    AssertLog(pCompdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

void Comp::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void Comp::restore(std::fstream& cp_file) {
    util::compare(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void Comp::addTet(WmVol* tet) {
    AssertLog(tet->compdef() == def());
    pTets.push_back(tet);
    pVol += tet->vol();
}

////////////////////////////////////////////////////////////////////////////////

void Comp::modCount(solver::spec_local_id slidx, double count) const {
    AssertLog(slidx < def()->countSpecs());
    double newcount = (def()->pools()[slidx] + count);
    AssertLog(newcount >= 0.0);
    def()->setCount(slidx, newcount);
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
    for (auto const& t: pTets) {
        accum += t->vol();
        if (selector < accum) {
            return t;
        }
    }
    AssertLog(false);
}

}  // namespace steps::mpi::tetopsplit
