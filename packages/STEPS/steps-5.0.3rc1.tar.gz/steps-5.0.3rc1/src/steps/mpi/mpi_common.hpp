/*
 ___license_placeholder___
 */

// Rationale:
// Store common definitions for MPI, such as communication tags

#pragma once

#include <limits.h>
#include <stdint.h>

namespace steps::mpi {

extern bool internally_initialized;

enum MsgTag {
    MPI_CONDITIONAL_BCAST = 1000,
    OPSPLIT_MOLECULE_CHANGE = 10000,
    OPSPLIT_MOLECULE_CHANGE_COMPLETE = 10001,
    OPSPLIT_COUNT_SYNC_INFO = 10100,
    OPSPLIT_COUNT_SYNC_DATA = 10101,
    OPSPLIT_SYNC_COMPLETE = 10102,
    OPSPLIT_KPROC_UPD = 10200,
    OPSPLIT_UPD_COMPLETE = 10201,

    RDEF_VESRAFT_POOL_SYNC = 20000
};

#ifdef STEPS_USE_64BITS_INDICES
#define MPI_STEPS_INDEX MPI_UNSIGNED_LONG
#else
#define MPI_STEPS_INDEX MPI_UNSIGNED
#endif

#if SIZE_MAX == UCHAR_MAX
#define MPI_STD_SIZE_T MPI_UNSIGNED_CHAR
#elif SIZE_MAX == USHRT_MAX
#define MPI_STD_SIZE_T MPI_UNSIGNED_SHORT
#elif SIZE_MAX == UINT_MAX
#define MPI_STD_SIZE_T MPI_UNSIGNED
#elif SIZE_MAX == ULONG_MAX
#define MPI_STD_SIZE_T MPI_UNSIGNED_LONG
#elif SIZE_MAX == ULLONG_MAX
#define MPI_STD_SIZE_T MPI_UNSIGNED_LONG_LONG
#endif

}  // namespace steps::mpi
