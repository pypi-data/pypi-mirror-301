/*
 ___license_placeholder___
 */

#include "vertexelement.hpp"

#include "util/checkpointing.hpp"
#include "vertexconnection.hpp"

namespace steps::solver::efield {

VertexElement::VertexElement(uint idx, const double* vpos)
    : pIDX(idx)
    , pXPos(vpos[0])
    , pYPos(vpos[1])
    , pZPos(vpos[2])
    , pSurface(0.0)
    , pVolume(0.0)
    , pCapacitance(0.0)
    , pNCon(0)
    , pNbrs(nullptr) {}

////////////////////////////////////////////////////////////////////////////////

VertexElement::~VertexElement() {
    delete[] pNbrs;
}

////////////////////////////////////////////////////////////////////////////////

void VertexElement::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pSurface);
    util::checkpoint(cp_file, pVolume);
    util::checkpoint(cp_file, pCapacitance);
    util::checkpoint(cp_file, pNCon);
    util::checkpoint(cp_file, pCcs);
}

////////////////////////////////////////////////////////////////////////////////

void VertexElement::restore(std::fstream& cp_file) {
    util::compare(cp_file, pSurface, "Mismatched pSurface restore value.");
    util::compare(cp_file, pVolume, "Mismatched pVolume restore value.");
    util::restore(cp_file, pCapacitance);
    util::compare(cp_file, pNCon, "Mismatched pNCon restore value.");
    util::restore(cp_file, pCcs);
}

////////////////////////////////////////////////////////////////////////////////

void VertexElement::fix() {
    pNCon = static_cast<uint>(pConnections.size());
    pNbrs = new VertexElement*[pNCon];
    pCcs.resize(pNCon);

    for (auto i = 0u; i < pNCon; ++i) {
        pNbrs[i] = pConnections[i]->getOther(this);
        pCcs[i] = 0.0;
    }
}

////////////////////////////////////////////////////////////////////////////////

void VertexElement::applyConductance(double a) {
    // this has some effect on compilation/optimization: without it,
    // the coupling constants are wrong
    // Iain : what on earth was the following line doing in here?
    // double* uu = new double[pNCon];

    for (auto i = 0u; i < pNCon; ++i) {
        pCcs[i] = a * pConnections[i]->getGeomCouplingConstant();
    }
}

}  // namespace steps::solver::efield
