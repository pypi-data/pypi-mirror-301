/*
 ___license_placeholder___
 */

#pragma once
#include <cmath>
#include <iostream>

#include "util/error.hpp"

namespace steps::mpi::tetvesicle {

class KProc;

struct CRGroup {
    CRGroup(int power, uint init_size = 1024) {
        max = pow(2, power);
        sum = 0.0;
        capacity = init_size;
        size = 0;
        indices = (KProc**) malloc(sizeof(KProc*) * init_size);
        SysErrLogIf(indices == nullptr, "DirectCR: unable to allocate memory for SSA group.");
#ifdef SSA_DEBUG
        std::cout << "SSA: CRGroup Created\n";
        std::cout << "power: " << power << "\n";
        std::cout << "max: " << max << "\n";
        std::cout << "capacity: " << capacity << "\n";
        std::cout << "--------------------------------------------------------\n";
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

}  // namespace steps::mpi::tetvesicle
