/*
 ___license_placeholder___
 */

// STEPS headers.
#include "wmrssa/kproc.hpp"

// logging
#include "util/error.hpp"

#include "util/checkpointing.hpp"

namespace steps::wmrssa {

////////////////////////////////////////////////////////////////////////////////

void KProc::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, rExtent);
}

////////////////////////////////////////////////////////////////////////////////

void KProc::restore(std::fstream& cp_file) {
    util::restore(cp_file, rExtent);
}

////////////////////////////////////////////////////////////////////////////////

solver::Reacdef* KProc::defr() const {
    // Should only be called on derived object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

solver::SReacdef* KProc::defsr() const {
    // Should only be called on derived object
    AssertLog(false);
}

}  // namespace steps::wmrssa
