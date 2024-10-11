/*
 ___license_placeholder___
 */

#include "dVsolver.hpp"

#include <algorithm>
#include <cmath>
#include <utility>

#include "geom/tetmesh.hpp"
#include "util/checkpointing.hpp"

namespace steps::solver::efield {

void dVSolverBase::initMesh(TetMesh* mesh) {
    pMesh = mesh;
    pNVerts = pMesh->countVertices();
    pNTris = pMesh->getNTri();

    pV.assign(pNVerts, 0.0);
    pGExt.assign(pNVerts, 0.0);
    pVertexClamp.assign(pNVerts, 0);
    pVertCur.assign(pNVerts, 0.0);
    pVertCurClamp.assign(pNVerts, 0.0);

    pTriCur.assign(pNTris, 0.0);
    pTriCurClamp.assign(pNTris, 0.0);
}

////////////////////////////////////////////////////////////////////////////////

void dVSolverBase::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pNVerts);
    util::checkpoint(cp_file, pNTris);
    util::checkpoint(cp_file, pV);
    util::checkpoint(cp_file, pGExt);
    util::checkpoint(cp_file, conductance);
    util::checkpoint(cp_file, pVExt);
    util::checkpoint(cp_file, pVertexClamp);
    util::checkpoint(cp_file, pTriCur);
    util::checkpoint(cp_file, pTriCurClamp);
    util::checkpoint(cp_file, pVertCur);
    util::checkpoint(cp_file, pVertCurClamp);
}

////////////////////////////////////////////////////////////////////////////////

void dVSolverBase::restore(std::fstream& cp_file) {
    util::compare(cp_file, pNVerts, "Mismatched EField pNVerts restore value.");
    util::compare(cp_file, pNTris, "Mismatched EField pNTris restore value.");
    util::restore(cp_file, pV);
    util::restore(cp_file, pGExt);
    util::restore(cp_file, conductance);
    util::restore(cp_file, pVExt);
    util::restore(cp_file, pVertexClamp);
    util::restore(cp_file, pTriCur);
    util::restore(cp_file, pTriCurClamp);
    util::restore(cp_file, pVertCur);
    util::restore(cp_file, pVertCurClamp);
}

void dVSolverBase::setSurfaceConductance(double g_surface, double v_rev) {
    conductance = g_surface;
    pVExt = v_rev;
    if (pMesh == nullptr) {
        return;
    }

    for (auto i: vertex_id_t::range(pNVerts)) {
        VertexElement* ve = pMesh->getVertex(i);
        pGExt[ve->getIDX()] = g_surface * ve->getSurfaceArea();
    }
}

std::pair<double, double> dVSolverBase::getSurfaceConductance() {
    return {conductance, pVExt};
}

int dVSolverBase::meshHalfBW(TetMesh* mesh) {
    int halfbw = 0;
    auto nVerts = mesh->countVertices();
    for (auto i: vertex_id_t::range(nVerts)) {
        VertexElement* ve = mesh->getVertex(i);

        int idx = ve->getIDX();
        int ncon = ve->getNCon();
        for (int j = 0; j < ncon; ++j) {
            halfbw = std::max(halfbw, std::abs(idx - static_cast<int>(ve->nbrIdx(j))));
        }
    }

    return halfbw;
}

}  // namespace steps::solver::efield
