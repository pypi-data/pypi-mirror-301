/*
 ___license_placeholder___
 */

#pragma once

#include <cmath>
#include <iostream>

#include "kproc.hpp"
// logging
#include "util/error.hpp"

namespace steps::mpi::tetopsplit {

class KProc;

struct CRGroup {
    explicit CRGroup(int power, uint init_size = 1024)
        : capacity(init_size)
        , max(std::pow(2, power)) {
        indices = static_cast<KProc**>(malloc(sizeof(KProc*) * init_size));
        SysErrLogIf(indices == nullptr, "DirectCR: unable to allocate memory for SSA group.");

#ifdef SSA_DEBUG
        CLOG(INFO, "general_log") << "SSA: CRGroup Created\n";
        CLOG(INFO, "general_log") << "power: " << power << "\n";
        CLOG(INFO, "general_log") << "max: " << max << "\n";
        CLOG(INFO, "general_log") << "capacity: " << capacity << "\n";
        CLOG(INFO, "general_log") << "--------------------------------------------------------\n";
#endif
    }

    void free_indices() {
        free(indices);
        indices = nullptr;
    }

    unsigned capacity;
    unsigned size{0};
    double max;
    double sum{0};
    KProc** indices;
};

struct CRKProcData {
    bool recorded{false};
    int pow{0};
    unsigned pos{0};
    double rate{0.0};
};

}  // namespace steps::mpi::tetopsplit
