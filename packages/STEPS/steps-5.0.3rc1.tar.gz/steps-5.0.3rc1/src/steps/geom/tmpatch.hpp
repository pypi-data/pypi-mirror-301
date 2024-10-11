/*
 ___license_placeholder___
 */

#pragma once

#include <string>
#include <vector>

#include "geom/fwd.hpp"
#include "geom/patch.hpp"
#include "math/bbox.hpp"
#include "util/vocabulary.hpp"

namespace steps::tetmesh {

/// Provides annotation for a group of surface triangles of a Tetmesh.
///
/// \warning Methods start with an underscore are not exposed to Python.
class TmPatch: public wm::Patch {
  public:
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////

    /// Constructor.
    ///
    /// \param id ID of the TmPatch.
    /// \param container Pointer to the Tetmesh container.
    /// \param tris A sequence of triangles (by index) as a vector
    ///             of unsigned integers which is represented as
    ///             a sequence of positive integer values) in Python.
    /// \param icomp Reference to the inner compartment.
    /// \param ocomp Pointer to the outer compartment.
    ///
    /// This is the constructor for the wm (well-mixed) namespace.
    TmPatch(std::string const& id,
            Tetmesh& container,
            std::vector<index_t> const& tris,
            wm::Comp& wmicomp,
            wm::Comp* wmocomp = nullptr);

    TmPatch(const TmPatch&) = delete;
    TmPatch& operator=(const TmPatch&) = delete;

    /// Destructor.
    ~TmPatch();

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS (EXPOSED TO PYTHON):
    ////////////////////////////////////////////////////////////////////////

    /// Return whether triangles (specified by index) are inside this patch.
    ///
    /// \param tris List of indices of triangles.
    /// \return Results of whether the triangles are inside the patch.
    std::vector<bool> isTriInside(const std::vector<index_t>& tris) const;

    /// Return all triangles (by index) in the patch.
    ///

    /// \return List of indices of triangles.
    std::vector<index_t> getAllTriIndices() const {
        return strong_type_to_value_type(pTri_indices);
    }

    /// Get the minimal coordinate of the rectangular bounding box or a plane.
    ///
    /// \return Minimal coordinate of the rectangular bounding box or a plane.
    std::vector<double> getBoundMin() const;

    /// Get the maximal coordinate of the rectangular bounding box or a plane.
    ///
    /// \return Maximal coordinate of the rectangular bounding box or a plane.
    std::vector<double> getBoundMax() const;

    /// Get all endocytic zones declared in the patch
    const std::vector<EndocyticZone*>& getAllEndocyticZones() const {
        return pEndoZones;
    }

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS (EXPOSED TO C++)
    ////////////////////////////////////////////////////////////////////////

    /// Return all triangles (by index) in the patch.
    ///
    /// \return List of indices of triangles.
    inline std::vector<triangle_global_id> const& _getAllTriIndices() const {
        return pTri_indices;
    }

    ////////////////////////////////////////////////////////////////////////

    /// Add an endocytic zone to the patch
    ///
    /// \param endoZone The endocytic zone
    void _addEndocyticZone(EndocyticZone* endoZone);

  private:
    Tetmesh& pTetmesh;
    std::vector<triangle_global_id> pTri_indices;
    std::size_t pTrisN;

    math::bounding_box pBBox;

    std::vector<EndocyticZone*> pEndoZones;
};

}  // namespace steps::tetmesh
