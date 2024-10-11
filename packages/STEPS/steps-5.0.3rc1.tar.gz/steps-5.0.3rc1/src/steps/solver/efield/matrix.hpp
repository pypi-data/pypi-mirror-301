/*
 ___license_placeholder___
 */

#pragma once

#include <fstream>
#include <iostream>

// STEPS headers.

namespace steps::solver::efield {

/// \todo Clean up (especially get rid of the pointer-to-pointer storage);
/// could be a useful addition for Boost STEPS.
///
/// \author Robert Cannon
///
class Matrix {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    /// Constructor that creates an uninitialized n0 * n0 matrix.
    ///
    Matrix(uint n0);

    /// Constructor that creates an nn * nn matrix and initializes it
    /// by copying the contents of da.
    ///
    Matrix(uint nn, double** da);

    /// Destructor.
    ///
    ~Matrix();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////
    // MATRIX OPERATIONS
    ////////////////////////////////////////////////////////////////////////

    /// Makes a deep copy of the matrix.
    ///
    Matrix* copy();

    /// Computes left-hand vector product.
    ///
    /// The resulting array needs to deallocated by the caller!
    ///
    double* lvprod(double* v);

    /// Returns the transpose of this matrix.
    ///
    Matrix* transpose();

    /// Computes the determinant of this matrix.
    ///
    double det();

    /// Returns the inverse of this matrix.
    ///
    Matrix* inverse();

    /// Compute the LU decomposition.
    ///
    void LU();

    ///
    double* lubksb(double*);

    /// NOT IMPLEMENTED????
    double* rvprod(double*);

    ////////////////////////////////////////////////////////////////////////

  private:
    double** pA;
    double* pWS;
    uint pN;
    int* pPerm;
    int pSign;
};

}  // namespace steps::solver::efield
