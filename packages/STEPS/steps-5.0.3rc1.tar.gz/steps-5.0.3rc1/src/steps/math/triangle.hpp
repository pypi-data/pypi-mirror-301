/*
 ___license_placeholder___
 */

/** \file math/triangle.hpp
 *  Geometric functions on triangles in 3-d space.
 */

#pragma once

#include "point.hpp"

namespace steps::math {

/** Calculate area of triangle.
 *
 * \param p0,p1,p2 Vertices of triangle.
 * \return Area.
 */
double tri_area(const point3d& p0, const point3d& p1, const point3d& p2);

/** Calculate triangle barycenter.
 *
 * \param p0,p1,p2 Vertices of triangle.
 * \return Barycenter.
 */
point3d tri_barycenter(const point3d& p0, const point3d& p1, const point3d& p2);

/** Calculate triangle normal vector.
 *
 * \param p0,p1,p2 Vertices of triangle.
 * \return Unit length normal vector.
 */
point3d tri_normal(const point3d& p0, const point3d& p1, const point3d& p2);

/** Select point in triangle from uniformly generated variates.
 *
 * \param p0,p1,p2 Vertices of triangle.
 * \param s,t Two uniformly-generated variates in [0,1].
 * \return Sampled point.
 */
point3d tri_ranpnt(const point3d& p0, const point3d& p1, const point3d& p2, double s, double t);

/** Intersects a triangle with a line segment
 *
 * \param tp0, tp1, tp2: Vertices of triangle
 * \param lp0, lp1: Two points of the ray/segment
 * \param is_segment: When true, the two points delimit a segment.
 *     Otherwise they define a ray starting at lp0 and passing by lp1
 * \return The intersection point if exists, else
 */
bool tri_intersect_line(const point3d& tp0,
                        const point3d& tp1,
                        const point3d& tp2,
                        const point3d& lp0,
                        const point3d& lp1,
                        point3d& intersection,
                        bool is_segment = true);

/** Intersects a triangle with a point
 *
 * \param tp0, tp1, tp2: Vertices of triangle
 * \param lp0, lp1: Point
 * \param is_triangle: When true, the three points delimit a triangle.
 * \return True if the point belongs to the triangle
 */
bool tri_intersect_point(const point3d& tp0,
                         const point3d& tp1,
                         const point3d& tp2,
                         const point3d& p,
                         const bool is_triangle = true);


////////////////////////////////////////////////////////////////////////////////

// For a given face of a tetrahedron tell if a particular point (pi) is in the
// same side than the opposite point (opposite) than the triangle defined by
// (center, p1, p2). To know it, it only look if dot-product of (norm of
// (center, p1, p2) * (center, opposite) is the same sign than norm of (center,
// p1, p2) * (center, pi).
bool same_direction(const point3d& center,
                    const point3d& opposite,
                    const point3d& p1,
                    const point3d& p2,
                    const point3d& pi);

}  // namespace steps::math
