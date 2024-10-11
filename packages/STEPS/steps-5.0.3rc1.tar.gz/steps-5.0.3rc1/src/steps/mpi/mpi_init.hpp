/*
 ___license_placeholder___
 */

// Rationale:
// We need a function to initialize stuffs such as logs
// before other STEPS object being created.
// The main function may also be used to fetch arguments
// passed from Python command.

#include <mpi.h>

namespace steps::mpi {

void mpiInit();
int getRank(MPI_Comm comm = MPI_COMM_WORLD);
int getNHosts(MPI_Comm comm = MPI_COMM_WORLD);

}  // namespace steps::mpi
