/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/raftproxy.hpp"

#include "mpi/tetvesicle/patch_rdef.hpp"
#include "mpi/tetvesicle/raftsreac.hpp"
#include "solver/raftdef.hpp"

namespace steps::mpi::tetvesicle {

RaftProxy::RaftProxy(solver::Raftdef* raftdef,
                     TriRDEF* central_tri,
                     solver::raft_individual_id unique_index)
    : pDef(raftdef)
    , pIndex(unique_index)
    , pTri(central_tri)
    , pImmobilityUpdate(0) {
    AssertLog(pDef != nullptr);
    AssertLog(pTri != nullptr);

    pRaftIndex = pDef->gidx();

    pPoolCount.resize(def()->countSpecs_global());
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::checkpoint(std::fstream& /*cp_file*/) {
    // Reserve. Nothing to do here because only created when rafts are created
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::restore(std::fstream& /*cp_file*/) {
    // Reserve.
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::setSpecCountByLidx(solver::spec_local_id slidx, uint count) {
    AssertLog(slidx < def()->countSpecs());
    solver::spec_global_id spec_gidx = def()->specL2G(slidx);
    pPoolCount[spec_gidx.get()] = count;
}

////////////////////////////////////////////////////////////////////////////////

uint RaftProxy::getSpecCountByLidx(solver::spec_local_id slidx) {
    AssertLog(slidx < def()->countSpecs());
    solver::spec_global_id spec_gidx = def()->specL2G(slidx);
    return pPoolCount[spec_gidx.get()];
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::setSpecCountByGidx(solver::spec_global_id sgidx, uint count) {
    AssertLog(sgidx < def()->countSpecs_global());
    pPoolCount[sgidx.get()] = count;
}

////////////////////////////////////////////////////////////////////////////////

uint RaftProxy::getSpecCountByGidx(solver::spec_global_id sgidx) {
    AssertLog(sgidx < def()->countSpecs_global());
    return pPoolCount[sgidx.get()];
}

////////////////////////////////////////////////////////////////////////////////

std::map<steps::index_t, uint> RaftProxy::getSpecs() {
    std::map<steps::index_t, uint> specs;
    for (auto spec_gidx: solver::spec_global_id::range(def()->countSpecs_global())) {
        uint count = pPoolCount[spec_gidx.get()];
        if (count > 0) {
            specs[spec_gidx.get()] = count;
        }
    }
    return specs;
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::updImmobility(int mob_upd) {
    pImmobilityUpdate += mob_upd;
}

////////////////////////////////////////////////////////////////////////////////

bool RaftProxy::getRaftSReacActive(solver::raftsreac_global_id rsreacidx) const {
    return pRaftSReac_inactive.find(rsreacidx) == pRaftSReac_inactive.end();
}

////////////////////////////////////////////////////////////////////////////////

void RaftProxy::setRaftSReacInActive(solver::raftsreac_global_id rsreacidx) {
    pRaftSReac_inactive.insert(rsreacidx);
}

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::mpi::tetvesicle
