/*
 ___license_placeholder___
 */

// STEPS headers.
#include "comp.hpp"
// logging
#include "util/error.hpp"

#include "util/checkpointing.hpp"

namespace steps::tetode {

////////////////////////////////////////////////////////////////////////////////

Comp::Comp(solver::Compdef* compdef)
    : pCompdef(compdef) {
    AssertLog(pCompdef != nullptr);
}

////////////////////////////////////////////////////////////////////////////////

Comp::~Comp() = default;

////////////////////////////////////////////////////////////////////////////////

void Comp::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void Comp::restore(std::fstream& cp_file) {
    util::compare(cp_file, pVol);
}

////////////////////////////////////////////////////////////////////////////////

void Comp::addTet(Tet* tet) {
    AssertLog(tet->compdef() == &def());
    tetrahedron_local_id lidx(static_cast<index_t>(pTets.size()));
    pTets.push_back(tet);
    pTets_GtoL.emplace(tet->idx(), lidx);
    pVol += tet->vol();
}

////////////////////////////////////////////////////////////////////////////////

Tet* Comp::getTet(tetrahedron_local_id lidx) {
    AssertLog(lidx < static_cast<index_t>(pTets.size()));
    return pTets[lidx.get()];
}

////////////////////////////////////////////////////////////////////////////////

steps::tetrahedron_local_id Comp::getTet_GtoL(tetrahedron_global_id gidx) {
    auto lidx_it = pTets_GtoL.find(gidx);
    AssertLog(lidx_it != pTets_GtoL.end());
    return lidx_it->second;
}

}  // namespace steps::tetode
