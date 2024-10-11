/*
 ___license_placeholder___
 */

#pragma once

#include <vector>

#include <petscksp.h>

#include "dVsolver.hpp"


namespace steps::solver::efield {

class dVSolverPETSC: public dVSolverBase {
  public:
    /// c-tor (*calls PetscInitialize*)
    explicit dVSolverPETSC(MPI_Comm petsc_comm);

    /// d-tor (*calls PetscFinalize*)
    ~dVSolverPETSC();

    /// Initialize mesh and sparsity pattern
    void initMesh(TetMesh* mesh) override final;

    /// Assemble and solve linear system to get potential at time t(n+1)
    void advance(double dt) override final;
    // Delete previous implementation in dVSolverBase for safety reasons
    void _advance() = delete;

    /// Init function, here for debugging, remove later
    void init();

  private:
    PetscInt prbegin{}, prend{};
    PetscInt pNlocal{};                       // number of rows handled by this processor
    std::vector<VertexElement*> pIdxToVert;   // map each idx to relative vertex
    std::vector<triangle_local_id> loc_tris;  // vector with all the idxs of triangles on this petsc
                                              // partition
    std::vector<int> petsc_locsizes;
    std::vector<int> petsc_displ;
    Mat pA{};        // lhs
    Vec pb{}, px{};  // rhs and approximate solution : pA * px = pb
    KSP pKsp{};      // Krylov solver
    PC pPc{};        // preconditioner
                     // std::vector<double> deltaV;
                     // PetscViewer viewer;
};

}  // namespace steps::solver::efield
