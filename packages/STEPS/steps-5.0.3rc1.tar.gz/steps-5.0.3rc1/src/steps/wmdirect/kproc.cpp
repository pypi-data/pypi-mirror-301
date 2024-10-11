/*
 ___license_placeholder___
 */

// STEPS headers.
#include "kproc.hpp"
// logging
#include "util/error.hpp"

#include "util/checkpointing.hpp"

namespace steps::wmdirect {

KProc::KProc() = default;

////////////////////////////////////////////////////////////////////////////////

KProc::~KProc() = default;

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

solver::ComplexReacdef& KProc::defcr() const {
    // Should only be called on derived object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

solver::SReacdef* KProc::defsr() const {
    // Should only be called on derived object
    AssertLog(false);
}

////////////////////////////////////////////////////////////////////////////////

solver::ComplexSReacdef& KProc::defcsr() const {
    // Should only be called on derived object
    AssertLog(false);
}

}  // namespace steps::wmdirect
