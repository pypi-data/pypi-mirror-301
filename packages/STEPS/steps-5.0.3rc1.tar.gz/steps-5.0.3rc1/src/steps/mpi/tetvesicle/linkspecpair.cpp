/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/linkspecpair.hpp"

// STEPS headers.
#include "math/point.hpp"
#include "mpi/tetvesicle/linkspec.hpp"
#include "mpi/tetvesicle/tetvesicle_vesraft.hpp"
#include "util/checkpointing.hpp"

namespace steps::mpi::tetvesicle {

LinkSpecPair::LinkSpecPair(LinkSpec* linkspec1,
                           LinkSpec* linkspec2,
                           Vesicle* ves1,
                           Vesicle* ves2,
                           double min_length,
                           double max_length)
    : pLinkSpec1(linkspec1)
    , pLinkSpec2(linkspec2)
    , pVesicle1(ves1)
    , pVesicle2(ves2)
    , pMaxLength(max_length)
    , pMinLength(min_length) {
    AssertLog(pLinkSpec1 != nullptr);
    AssertLog(pLinkSpec2 != nullptr);
    AssertLog(pVesicle1 != nullptr);
    AssertLog(pVesicle2 != nullptr);

    AssertLog(pMaxLength > pMinLength);
    AssertLog(pMinLength >= 0.0);
    AssertLog(pLinkSpec1 != pLinkSpec2);
    AssertLog(pVesicle1 != pVesicle2);

    pIsSymmetric = (pVesicle1->idx() == pVesicle2->idx() and
                    pLinkSpec1->getGidx() == pLinkSpec2->getGidx());
}

////////////////////////////////////////////////////////////////////////////////

LinkSpecPair::LinkSpecPair(std::fstream& cp_file, TetVesicleVesRaft* solver) {
    solver::linkspec_individual_id lspec1_id;
    solver::linkspec_individual_id lspec2_id;
    util::restore(cp_file, lspec1_id);
    util::restore(cp_file, lspec2_id);

    pLinkSpec1 = solver->getLinkSpec_(lspec1_id);
    pLinkSpec2 = solver->getLinkSpec_(lspec2_id);
    pLinkSpec1->addLinkSpecPair(this);
    pLinkSpec2->addLinkSpecPair(this);


    solver::vesicle_individual_id ves1_id;
    solver::vesicle_individual_id ves2_id;
    util::restore(cp_file, ves1_id);
    util::restore(cp_file, ves2_id);

    pVesicle1 = pLinkSpec1->getVesicle();
    pVesicle2 = pLinkSpec2->getVesicle();
    AssertLog(pVesicle1->getUniqueIndex() == ves1_id);
    AssertLog(pVesicle2->getUniqueIndex() == ves2_id);


    util::restore(cp_file, pMaxLength);
    util::restore(cp_file, pMinLength);
    util::restore(cp_file, pIsSymmetric);
}

////////////////////////////////////////////////////////////////////////////////

LinkSpecPair::~LinkSpecPair() = default;

////////////////////////////////////////////////////////////////////////////////

void LinkSpecPair::checkpoint(std::fstream& cp_file) const {
    util::checkpoint(cp_file, getLinkSpec1_uniqueID());
    util::checkpoint(cp_file, getLinkSpec2_uniqueID());
    util::checkpoint(cp_file, getVesicle1()->getUniqueIndex());
    util::checkpoint(cp_file, getVesicle2()->getUniqueIndex());
    util::checkpoint(cp_file, pMaxLength);
    util::checkpoint(cp_file, pMinLength);
    util::checkpoint(cp_file, pIsSymmetric);
}

////////////////////////////////////////////////////////////////////////////////

LinkSpec* LinkSpecPair::getPairedLinkSpec(const LinkSpec* ls) const {
    if (ls == pLinkSpec1) {
        return pLinkSpec2;
    }
    if (ls == pLinkSpec2) {
        return pLinkSpec1;
    }

    std::ostringstream os;
    os << "LinkSpec argument unknown in LinkSpecPair. ";
    ProgErrLog(os.str());
}

////////////////////////////////////////////////////////////////////////////////

solver::linkspec_individual_id LinkSpecPair::getLinkSpecLowID() const noexcept {
    solver::linkspec_individual_id ls1_id = pLinkSpec1->getUniqueID();
    solver::linkspec_individual_id ls2_id = pLinkSpec2->getUniqueID();

    return (ls1_id < ls2_id) ? ls1_id : ls2_id;
}

////////////////////////////////////////////////////////////////////////////////

inline solver::linkspec_individual_id LinkSpecPair::getLinkSpec1_uniqueID() const noexcept {
    return pLinkSpec1->getUniqueID();
}

////////////////////////////////////////////////////////////////////////////////

inline solver::linkspec_individual_id LinkSpecPair::getLinkSpec2_uniqueID() const noexcept {
    return pLinkSpec2->getUniqueID();
}

}  // namespace steps::mpi::tetvesicle
