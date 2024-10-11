#pragma once

#include <functional>
#include <optional>
#include <string>

#include <Omega_h_defines.hpp>

#include "model/complexsreac.hpp"
#include "model/fwd.hpp"
#include "model/ghkcurr.hpp"
#include "model/sreac.hpp"
#include "model/vdepsreac.hpp"
#include "util/vocabulary.hpp"

namespace steps::dist {

namespace osh = Omega_h;

// Forward declaration
class Compdef;
class Diffdef;
class Complexdef;
template <typename P>
class ReacdefBase;
using Reacdef = ReacdefBase<steps::model::Reac>;
class ComplexReacdef;

template <typename Entity>
struct EntityMolecules;
struct ComplexFilterDescr;
template <typename Entity>
class ComplexFilter;
struct FilterHash;
template <typename Entity>
class ComplexState;

template <typename P>
class SReacdefBase;
template <typename T>
class ModelSReacdef;
template <typename T>
class ModelComplexSReacdef;
struct SReacInfo {
    osh::Real kCst;
};
using SReacdef = ModelSReacdef<steps::model::SReac>;
using ComplexSReacdef = ModelComplexSReacdef<steps::model::ComplexSReac>;
using VDepComplexSReacdef = ModelComplexSReacdef<steps::model::VDepComplexSReac>;

using vdep_propensity_fun_t = std::function<osh::Real(osh::Real)>;
struct VDepInfo {
    vdep_propensity_fun_t kCstFun;
};
using VDepSReacdef = ModelSReacdef<steps::model::VDepSReac>;

/// Parameters of the particular GHK reaction.
struct GHKInfo {
    /// GHK current identifier
    model::ghk_current_id curr_id;
    /// if true, the surface reaction involves an ion transfer from the inner to outer compartment,
    /// and conversely otherwise.
    bool in2out;
    /// permeability per ion channel
    osh::Real permeability;
    /// ion valence
    osh::I64 valence;
    /// optional locked-in inner compartment concentration of the ion
    std::optional<osh::Real> inner_conc;
    /// optional locked-in outer compartment concentration of the ion
    std::optional<osh::Real> outer_conc;
};
class GHKSReacdef;
class ComplexGHKSReacdef;
class Patchdef;

class Simulation;
class Statedef;

template <typename SReacT>
struct Model2Def;

template <>
struct Model2Def<steps::model::Reac> {
    using def_type = Reacdef;
};

template <>
struct Model2Def<steps::model::ComplexReac> {
    using def_type = ComplexReacdef;
};

template <>
struct Model2Def<steps::model::SReac> {
    using def_type = SReacdef;
};

template <>
struct Model2Def<steps::model::ComplexSReac> {
    using def_type = ComplexSReacdef;
};

template <>
struct Model2Def<steps::model::VDepComplexSReac> {
    using def_type = VDepComplexSReacdef;
};

template <>
struct Model2Def<steps::model::VDepSReac> {
    using def_type = VDepSReacdef;
};

template <>
struct Model2Def<steps::model::GHKcurr> {
    using def_type = GHKSReacdef;
};

template <>
struct Model2Def<steps::model::ComplexGHKcurr> {
    using def_type = ComplexGHKSReacdef;
};

}  // namespace steps::dist
