/*
 ___license_placeholder___
 */

#include "finish.hpp"

#ifdef OMEGA_H_USE_GMSH
#include <gmsh.h>
#endif  // OMEGA_H_USE_GMSH

#include "util/profile/profiler_interface.hpp"

void steps::finish() {
#ifdef OMEGA_H_USE_GMSH
    ::gmsh::finalize();
#endif  // OMEGA_H_USE_GMSH

    // Finalize if not already finalized
    steps::Instrumentor::finalize_profile();
}
