/*
 ___license_placeholder___
 */

#include "api.hpp"

#include "compdef.hpp"
#include "patchdef.hpp"
#include "specdef.hpp"
#include "statedef.hpp"
#include "util/error.hpp"

namespace steps::solver {

uint API::getNComps() const {
    return pStatedef->countComps();
}

////////////////////////////////////////////////////////////////////////////////

uint API::getNPatches() const {
    return pStatedef->countPatches();
}

////////////////////////////////////////////////////////////////////////////////

std::string API::getCompName(comp_global_id c_idx) const {
    return pStatedef->compdef(c_idx).name();
}

////////////////////////////////////////////////////////////////////////////////

std::string API::getPatchName(patch_global_id p_idx) const {
    return pStatedef->patchdef(p_idx).name();
}

////////////////////////////////////////////////////////////////////////////////

uint API::getNCompSpecs(comp_global_id c_idx) const {
    return pStatedef->compdef(c_idx).countSpecs();
}

////////////////////////////////////////////////////////////////////////////////

uint API::getNPatchSpecs(patch_global_id p_idx) const {
    return pStatedef->patchdef(p_idx).countSpecs();
}

////////////////////////////////////////////////////////////////////////////////

std::string API::getCompSpecName(comp_global_id c_idx, spec_local_id s_idx) const {
    return pStatedef->specdef(pStatedef->compdef(c_idx).specL2G(s_idx)).name();
}

////////////////////////////////////////////////////////////////////////////////

std::string API::getPatchSpecName(patch_global_id p_idx, spec_local_id s_idx) const {
    return pStatedef->specdef(pStatedef->patchdef(p_idx).specL2G(s_idx)).name();
}

}  // namespace steps::solver
