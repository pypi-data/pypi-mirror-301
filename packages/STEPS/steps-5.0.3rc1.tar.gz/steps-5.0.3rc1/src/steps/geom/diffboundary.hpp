/*
 ___license_placeholder___
 */

#pragma once

#include <vector>

#include "fwd.hpp"

#include "util/vocabulary.hpp"

namespace steps::tetmesh {

/// Provides annotation for a group of diffusion boundary triangles of a
/// Tetmesh.
///
/// Tetmesh object is responsible for maintaining lifetime of associated
/// DiffBoundary objects (Python proxy class must set thisown to zero.)
///
/// \warning Methods start with an underscore are not exposed to Python.
class DiffBoundary {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    /// Constructor.
    ///
    /// \param id ID of the DiffBoundary.
    /// \param container Reference to the \a Tetmesh container.
    /// \param tris A sequence of triangles (by index) as a vector
    ///             of unsigned integers which is represented as
    ///             a sequence of positive integer values in Python.

    ///
    /// This is the constructor for the tetmesh (tetrahedron mesh) namespace.
    DiffBoundary(std::string id, Tetmesh& container, std::vector<index_t> const& tris);
    DiffBoundary(const DiffBoundary&) = delete;
    DiffBoundary& operator=(const DiffBoundary&) = delete;

    /// Destructor.
    virtual ~DiffBoundary();

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS (EXPOSED TO PYTHON):
    ////////////////////////////////////////////////////////////////////////

    /// Return the patch id.
    ///
    /// \return ID of the diffusion boundary.
    inline std::string const& getID() const noexcept {
        return pID;
    }

    /// Set or change the diffusion boundary id.
    ///
    /// \param id ID of the diffusion boundary.
    void setID(std::string const& id);

    /// Return a reference to the geometry container object.
    ///
    /// \return Reference to the parent geometry container.
    inline tetmesh::Tetmesh& getContainer() const noexcept {
        return pTetmesh;
    }

    /// Return whether triangles (specified by index) are inside this diffusion
    /// boundary.
    ///
    /// \param tri List of indices of triangles.
    /// \return Results of whether the triangles are inside the diffusion
    /// boundary.
    std::vector<bool> isTriInside(std::vector<index_t> const& tris) const;

    /// Return all triangles (by index) in the diffusion boundary.
    ///
    /// \return List of indices of triangles.
    inline std::vector<index_t> getAllTriIndices() const noexcept {
        return strong_type_to_value_type(pTri_indices);
    }

    /// Return the compartments this diffusion boundary connects
    ///
    /// \return List of the two compartments.
    inline std::vector<wm::Comp*> getComps() const noexcept {
        return {pIComp, pOComp};
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS (EXPOSED TO C++)
    ////////////////////////////////////////////////////////////////////////

    /// Return all triangles (by index) in the diffusion boundary.
    ///
    /// \return List of indices of triangles.
    inline std::vector<triangle_global_id> const& _getAllTriIndices() const noexcept {
        return pTri_indices;
    }

    ////////////////////////////////////////////////////////////////////////

  private:
    ////////////////////////////////////////////////////////////////////////

    std::string pID;
    tetmesh::Tetmesh& pTetmesh;
    wm::Comp* pIComp{nullptr};
    wm::Comp* pOComp{nullptr};
    std::vector<triangle_global_id> pTri_indices;

    ////////////////////////////////////////////////////////////////////////////////
};

}  // namespace steps::tetmesh
