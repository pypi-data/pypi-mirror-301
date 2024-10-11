/*
 ___license_placeholder___
 */

#pragma once

#include <algorithm>
#include <memory>
#include <vector>

#include <mpi.h>

// STEPS headers.
#include "dVsolver.hpp"
#include "slusystem.hpp"

namespace steps::solver::efield {

class dVSolverSLU: public dVSolverBase {
  public:
    explicit dVSolverSLU(MPI_Comm comm)
        : pMpiComm(comm) {}

    void initMesh(TetMesh* mesh) override {
        dVSolverBase::initMesh(mesh);
        sparsity_template S(pNVerts);

        for (auto i = 0u; i < pNVerts; ++i) {
            VertexElement* ve = mesh->getVertex(i);

            int idx = ve->getIDX();
            int ncon = ve->getNCon();

            S.emplace(idx, idx);
            for (int j = 0; j < ncon; ++j) {
                S.emplace(idx, static_cast<int>(ve->nbrIdx(j)));
            }
        }

        pSLUSys.reset(new SLUSystem(S, pMpiComm));
    }

    void advance(double dt) override {
        _advance(pSLUSys.get(), dt);
    }

  private:
    std::unique_ptr<SLUSystem> pSLUSys;
    MPI_Comm pMpiComm;
};

}  // namespace steps::solver::efield
