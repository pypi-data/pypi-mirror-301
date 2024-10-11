/*
 ___license_placeholder___
 */

/** \file math/tetrahedron.hpp
 *  Geometric functions on tetrahedra in 3-d space.
 */

#pragma once

#include "point.hpp"

namespace steps::math {

/** Calculate volume of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Volume.
 */
double tet_vol(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Calculate tetrahedron barycenter.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Barycenter.
 */
point3d tet_barycenter(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Test for point inclusion in tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \param pi Point to test
 * \return True if pi lies within tetrahedron.
 */
bool tet_inside(const point3d& p0,
                const point3d& p1,
                const point3d& p2,
                const point3d& p3,
                const point3d& pi);

/** Select point in tetrahedron from uniformly generated variates.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \param s,t,u Three uniformly-generated variates in [0,1].
 * \return Sampled point.
 */
point3d tet_ranpnt(const point3d& p0,
                   const point3d& p1,
                   const point3d& p2,
                   const point3d& p3,
                   double s,
                   double t,
                   double u);

/** Caclulate circumradius of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Circumradius.
 */
double tet_circumrad(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Caclulate square of circumradius of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Circumradius squared.
 */
double tet_circumrad2(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Caclulate length of shortest edge of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Shortest edge length.
 */
double tet_shortestedge(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Caclulate squared length of shortest edge of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Shortest edge length squared.
 */
double tet_shortestedge2(const point3d& p0,
                         const point3d& p1,
                         const point3d& p2,
                         const point3d& p3);

/** Caclulate length of longest edge of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Shortest edge length.
 */
double tet_longestedge(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

/** Caclulate squared length of longest edge of tetrahedron.
 *
 * \param p0,p1,p2,p3 Vertices of tetrahedron.
 * \return Shortest edge length squared.
 */
double tet_longestedge2(const point3d& p0, const point3d& p1, const point3d& p2, const point3d& p3);

}  // namespace steps::math
