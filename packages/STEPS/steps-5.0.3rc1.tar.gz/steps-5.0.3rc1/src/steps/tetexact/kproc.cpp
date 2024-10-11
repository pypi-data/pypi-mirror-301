/*
 ___license_placeholder___
 */

// STEPS headers.
#include "kproc.hpp"

#include "util/error.hpp"

#include "util/checkpointing.hpp"

namespace steps::tetexact {

KProc::KProc() = default;

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

void KProc::resetCcst() const {
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

}  // namespace steps::tetexact
