/*
 ___license_placeholder___
 */

#pragma once

#include <cmath>
#include <iostream>

#include "kproc.hpp"

// logging
#include "util/error.hpp"

namespace steps::tetexact {

class KProc;

struct CRGroup {
    CRGroup(int power, uint init_size = 1024) {
        max = pow(2, power);
        sum = 0.0;
        capacity = init_size;
        size = 0;
        indices = static_cast<KProc**>(malloc(sizeof(KProc*) * init_size));
        if (indices == NULL)
            SysErrLog("DirectCR: unable to allocate memory for SSA group.");

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
        indices = 0;
    }

    unsigned capacity;
    unsigned size;
    double max;
    double sum;
    KProc** indices;
};

struct CRKProcData {
    CRKProcData() {
        recorded = false;
        pow = 0;
        pos = 0;
        rate = 0.0;
    }

    bool recorded;
    int pow;
    unsigned pos;
    double rate;
};

}  // namespace steps::tetexact
