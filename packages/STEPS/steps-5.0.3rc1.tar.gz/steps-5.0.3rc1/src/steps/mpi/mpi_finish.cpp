/*
 ___license_placeholder___
 */

#include <mpi.h>

#include "mpi/mpi_common.hpp"
#include "mpi/mpi_finish.hpp"

#ifdef USE_PETSC
#include <petscsys.h>
#endif

#include "util/profile/profiler_interface.hpp"

namespace steps::mpi {

void mpiFinish() {
    steps::Instrumentor::finalize_profile();

    if (!internally_initialized) {
        return;
    }

    int flag;
    MPI_Finalized(&flag);
    if (flag == 0) {
        MPI_Finalize();
    }
}

void mpiAbort() {
    MPI_Abort(MPI_COMM_WORLD, 1);
}

}  // namespace steps::mpi
