/*
 ___license_placeholder___
 */

#include "diffdef.hpp"

#include "model/diff.hpp"
#include "model/spec.hpp"
#include "statedef.hpp"
#include "util/checkpointing.hpp"

namespace steps::solver {

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>
MetaDiffdef<GlobalId>::MetaDiffdef(Statedef& sd, GlobalId idx, model::Diff& d)
    : pIdx(idx)
    , pName(d.getID())
    , pDcst(d.getDcst())
    , ligGIdx(sd.getSpecIdx(d.getLig().getID())) {
    const uint nspecs = sd.countSpecs();
    pSpec_DEP.resize(nspecs, DEP_NONE);
}

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>
void MetaDiffdef<GlobalId>::checkpoint(std::fstream& /*cp_file*/) const {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>

void MetaDiffdef<GlobalId>::restore(std::fstream& /*cp_file*/) {
    // reserve
}

////////////////////////////////////////////////////////////////////////////////


template <typename GlobalId>
void MetaDiffdef<GlobalId>::setup(const Statedef&) {
    AssertLog(pSetupdone == false);

    pSpec_DEP[lig().get()] = DEP_STOICH;

    pSetupdone = true;
}

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>
spec_global_id MetaDiffdef<GlobalId>::lig() const {
    return ligGIdx;
}

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>
int MetaDiffdef<GlobalId>::dep(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_DEP.at(gidx.get());
}

////////////////////////////////////////////////////////////////////////////////

template <typename GlobalId>
bool MetaDiffdef<GlobalId>::reqspec(spec_global_id gidx) const {
    AssertLog(pSetupdone == true);
    return pSpec_DEP.at(gidx.get()) != DEP_NONE;
}

// explicit template instantiation definitions
template class MetaDiffdef<diff_global_id>;
template class MetaDiffdef<surfdiff_global_id>;

}  // namespace steps::solver
