/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "tetmesh.hpp"

namespace steps::solver::efield {

/// It is temporarily created in the constructor of class EField, after a
/// TetMesh has been (partially) constructed.
///
/// \author Robert Cannon
///
class TetCoupler {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    /// Constructor. Just copies the mesh pointer.
    ///
    TetCoupler(TetMesh* mesh);

    /// Destructor.
    ///
    ~TetCoupler();

    ////////////////////////////////////////////////////////////////////////

    /// The major method in this class... it couples a mesh!
    ///
    /// The coupling constants are stored in the VertexConnection
    /// objects stored in the mesh.
    ///
    void coupleMesh();

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////
    // AUXILIARY FUNCTIONS FOR COUPLEMESH()
    ////////////////////////////////////////////////////////////////////////

    /// Checks whether two doubles differ.
    ///
    bool dblsDiffer(double, double);

    /// Compute the corss product between two vectors
    void cross_product(double* a, double* b, double* c);

    /// Computes the actual flux coefficients.
    ///
    ///
    void fluxCoeficients(VertexElement*, VertexElement**, double* ret);

    ////////////////////////////////////////////////////////////////////////
    // DATA FIELDS
    ////////////////////////////////////////////////////////////////////////

    TetMesh* pMesh;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::solver::efield
