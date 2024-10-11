/*
 ___license_placeholder___
 */

#include <string>

#include <mpi.h>

#include "mpi/mpi_init.hpp"
#include "util/error.hpp"

namespace steps::mpi {

bool internally_initialized = false;
void mpiInit() {
    /* Initialize MPI */
    {
        int flag;
        MPI_Initialized(&flag);
        if (flag == 0) {
            internally_initialized = true;
            MPI_Init(nullptr, nullptr);
        }
    }

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // This will replace the general log setup in serial init()
    // parallel Logger
    el::Configurations parallel_conf;

    // Global conf for the logger
    parallel_conf.set(el::Level::Global,
                      el::ConfigurationType::Format,
                      "[%datetime][%level][%loc][%func]: %msg");
    parallel_conf.set(el::Level::Global, el::ConfigurationType::ToStandardOutput, "false");
    parallel_conf.set(el::Level::Global, el::ConfigurationType::ToFile, "true");
    std::string file = ".logs/general_log_";
    file += std::to_string(rank);
    file += ".txt";
    parallel_conf.set(el::Level::Global, el::ConfigurationType::Filename, file);
    parallel_conf.set(el::Level::Global, el::ConfigurationType::MaxLogFileSize, "2097152");

    parallel_conf.set(el::Level::Fatal, el::ConfigurationType::ToStandardOutput, "true");
    parallel_conf.set(el::Level::Error, el::ConfigurationType::ToStandardOutput, "true");
    parallel_conf.set(el::Level::Warning, el::ConfigurationType::ToStandardOutput, "true");

    el::Loggers::getLogger("general_log");
    el::Loggers::reconfigureLogger("general_log", parallel_conf);

    MPI_Barrier(MPI_COMM_WORLD);
}

int getRank(MPI_Comm comm) {
    int rank;
    MPI_Comm_rank(comm, &rank);
    return rank;
}

int getNHosts(MPI_Comm comm) {
    int nhosts;
    MPI_Comm_size(comm, &nhosts);
    return nhosts;
}

}  // namespace steps::mpi
