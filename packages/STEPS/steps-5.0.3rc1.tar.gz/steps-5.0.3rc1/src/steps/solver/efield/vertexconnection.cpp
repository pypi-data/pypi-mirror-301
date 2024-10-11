/*
 ___license_placeholder___
 */

#include "vertexconnection.hpp"

#include "util/checkpointing.hpp"
#include "util/error.hpp"
#include "vertexelement.hpp"

namespace steps::solver::efield {

VertexConnection::VertexConnection(VertexElement* v1, VertexElement* v2)
    : pVert1(v1)
    , pVert2(v2)
    , pGeomCC(0.0) {
    AssertLog(v1 != nullptr);
    AssertLog(v2 != nullptr);
    pVert1->addConnection(this);
    pVert2->addConnection(this);
}

////////////////////////////////////////////////////////////////////////////////

VertexConnection::~VertexConnection() = default;

////////////////////////////////////////////////////////////////////////////////

void VertexConnection::checkpoint(std::fstream& cp_file) {
    util::checkpoint(cp_file, pGeomCC);
}

////////////////////////////////////////////////////////////////////////////////

void VertexConnection::restore(std::fstream& cp_file) {
    util::compare(cp_file, pGeomCC, "Mismatched pGeomCC restore value.");
}

////////////////////////////////////////////////////////////////////////////////

VertexElement* VertexConnection::getOther(VertexElement* element) {
    VertexElement* ret;
    if (pVert1 == element) {
        ret = pVert2;
    } else if (pVert2 == element) {
        ret = pVert1;
    } else {
        AssertLog(false);
    }
    return ret;
}

}  // namespace steps::solver::efield
