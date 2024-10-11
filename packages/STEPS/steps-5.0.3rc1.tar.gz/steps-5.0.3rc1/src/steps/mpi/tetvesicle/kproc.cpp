/*
 ___license_placeholder___
 */

#include "mpi/tetvesicle/kproc.hpp"

// STEPS headers.
#include "util/checkpointing.hpp"

namespace steps::mpi::tetvesicle {

////////////////////////////////////////////////////////////////////////////////

KProc::KProc()
    : rExtent(0)
    , pFlags(0)
    , pSchedIDX(0u) {}

////////////////////////////////////////////////////////////////////////////////

KProc::~KProc() = default;

////////////////////////////////////////////////////////////////////////////////

void KProc::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, rExtent);
    util::checkpoint(cp_file, pFlags);
    util::checkpoint(cp_file, crData);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::restore(std::fstream& cp_file) {
    util::restore(cp_file, rExtent);
    util::restore(cp_file, pFlags);
    util::restore(cp_file, crData);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::setActive(bool active) {
    if (active == true) {
        pFlags &= ~INACTIVATED;
    } else {
        pFlags |= INACTIVATED;
    }
}

////////////////////////////////////////////////////////////////////////////////

unsigned long long KProc::getExtent() const {
    return rExtent;
}

////////////////////////////////////////////////////////////////////////////////

void KProc::resetExtent() {
    rExtent = 0;
}
////////////////////////////////////////////////////////////////////////////////

void KProc::resetCcst() {
    // This should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

double KProc::c() const {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

double KProc::h() {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

double KProc::rate(TetVesicleRDEF* /*solver*/) {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

int KProc::apply(const rng::RNGptr& /*rng*/) {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

int KProc::apply(const rng::RNGptr& /*rng*/, uint /*nmolcs*/) {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::apply(const rng::RNGptr& /*rng*/,
                  double /*dt*/,
                  double /*simtime*/,
                  double /*period*/,
                  TetVesicleRDEF* /*solver*/) {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::apply(TetVesicleRDEF* /*solver*/) {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::apply() {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

std::vector<KProc*> const& KProc::getLocalUpdVec(int /*direction*/) const {
    // Should never get called on base object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

std::vector<solver::kproc_global_id> const& KProc::getRemoteUpdVec(int /*direction*/) const {
    // Should never get called on base object
    AssertLog(false);
}

}  // namespace steps::mpi::tetvesicle
