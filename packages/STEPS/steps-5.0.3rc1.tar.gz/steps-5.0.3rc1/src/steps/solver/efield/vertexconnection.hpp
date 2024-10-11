/*
 ___license_placeholder___
 */

#pragma once

// STL headers.
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// STEPS headers.

namespace steps::solver::efield {

// Forward declarations.
class VertexElement;
class VertexConnection;
class Mesh;

// Auxiliary declarations.
typedef VertexConnection* VertexConnectionP;
typedef std::vector<VertexConnectionP> VertexConnectionPVec;
typedef VertexConnectionPVec::iterator VertexConnectionPVecI;
typedef VertexConnectionPVec::const_iterator VertexConnectionPVecCI;

////////////////////////////////////////////////////////////////////////////////

/// Class VertexConnection only contains pointers to vertices, so when
/// vertex indices are changed, there is no need to update anything in
/// these objects.
///
class VertexConnection {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    /// Constructor. Copies the VertexElement pointers and notifies them
    /// that they are a part of this connection.
    ///
    VertexConnection(VertexElement* v1, VertexElement* v2);

    /// Destructor.
    ///
    ~VertexConnection();

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::fstream& cp_file);

    /// restore data
    void restore(std::fstream& cp_file);

    ////////////////////////////////////////////////////////////////////////

    // bool isEdge();
    // bool hasInternalEnd();

    /// When called with a VertexElement that is part of this connection,
    /// this method returns the VertexElement on the other side of the
    /// connection. If the parameter is not a part of the connection,
    /// an assertion is raised.
    ///
    VertexElement* getOther(VertexElement*);

    inline void setGeomCouplingConstant(double d) noexcept {
        pGeomCC = d;
    }

    inline VertexElement* getA() const noexcept {
        return pVert1;
    }

    inline VertexElement* getB() const noexcept {
        return pVert2;
    }

    inline double getGeomCouplingConstant() const noexcept {
        return pGeomCC;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT DATA
    ////////////////////////////////////////////////////////////////////////

    ///@{
    /// Point to the vertices on this connection.
    VertexElement* pVert1;
    VertexElement* pVert2;
    ///@}

    /// Geometric coupling constant.
    double pGeomCC;

    ////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::solver::efield
