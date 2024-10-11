/*
 ___license_placeholder___
 */

// Rationale:
// We need a function to initialize stuffs such as logs
// before other STEPS object being created.
// The main function may also be used to fetch arguements
// passed from Python command.

#pragma once

namespace steps::mpi {

void mpiFinish();
void mpiAbort();

}  // namespace steps::mpi
