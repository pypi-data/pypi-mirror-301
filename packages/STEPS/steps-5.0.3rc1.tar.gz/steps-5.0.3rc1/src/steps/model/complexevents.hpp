/*
 ___license_placeholder___
 */

#pragma once

#include "solver/fwd.hpp"
#include "util/common.hpp"
#include "util/vocabulary.hpp"

namespace steps::model {

inline constexpr uint COMPLEX_FILTER_MAX_VALUE = std::numeric_limits<uint>::max();

////////////////////////////////////////////////////////////////////////////////
/// Subunit state filter that holds the minimum and maximum number of subunits
/// that can be in a given state in order to match a filter.
struct SubunitStateFilter {
    SubunitStateFilter() = default;
    SubunitStateFilter(uint _min, uint _max)
        : min(_min)
        , max(_max) {}
    uint min{};
    uint max{};
};

inline bool operator==(const SubunitStateFilter& lhs, const SubunitStateFilter& rhs) {
    return lhs.min == rhs.min and lhs.max == rhs.max;
}

////////////////////////////////////////////////////////////////////////////////
/// Complex filter description
/// A single std::vector<SubunitStateFilter> describes a slice of the complex
/// state space, the union of several of these slices corresponds to the overall
/// filter. If a complex state is within one of these slices, it matches the
/// filter.
struct ComplexFilterDescr {
    ComplexFilterDescr(const std::string& _complexId,
                       std::vector<std::vector<SubunitStateFilter>> _filters)
        : complexId(_complexId)
        , filters(_filters) {}
    const std::string complexId;
    const std::vector<std::vector<SubunitStateFilter>> filters;
};

////////////////////////////////////////////////////////////////////////////////
/// A specific complex update that holds:
///     - the subunit states that are required for an update to be possible
///     - the update vector that represents the changes in subunit state numbers
struct ComplexUpdate {
    ComplexUpdate(std::vector<uint> req, std::vector<int> upd)
        : requirement(req)
        , update(upd) {}
    util::strongid_vector<solver::complex_substate_id, uint> requirement;
    util::strongid_vector<solver::complex_substate_id, int> update;
};

inline bool operator==(const ComplexUpdate& lhs, const ComplexUpdate& rhs) {
    return lhs.requirement == rhs.requirement and lhs.update == rhs.update;
}


////////////////////////////////////////////////////////////////////////////////
/// Base class for all complex events
/// A complex event describes what happens to a specific complex during a complex
/// reaction.
class ComplexEvent {
  public:
    ComplexEvent(std::string const& cmplxId);
    virtual ~ComplexEvent() = default;

    const std::string& complexId() const noexcept {
        return pcomplexId;
    };

  protected:
    const std::string pcomplexId;
};

////////////////////////////////////////////////////////////////////////////////
/// Complex event representing the creation of a new complex in a specific state
/// The corresponding complex only appears on the right hand side of a reaction.
class ComplexCreateEvent: public ComplexEvent {
  public:
    ComplexCreateEvent(std::string const& cmplxId, const std::vector<uint>& in);

    const std::vector<uint>& init() const noexcept {
        return pinit;
    }

  protected:
    const std::vector<uint> pinit;
};

////////////////////////////////////////////////////////////////////////////////
/// Base class for complex events that affect complexes present on the left hand
/// side of a reaction.
/// Contains a filter that determines which specific states match the reaction.
class ComplexLHSEvent: public ComplexEvent {
  public:
    ComplexLHSEvent(std::string const& cmplxId,
                    const std::vector<std::vector<SubunitStateFilter>>& filts);

    const std::vector<util::strongid_vector<solver::complex_substate_id, SubunitStateFilter>>&
    filters() const noexcept {
        return pfilters;
    }

  protected:
    std::vector<util::strongid_vector<solver::complex_substate_id, SubunitStateFilter>> pfilters;
};

////////////////////////////////////////////////////////////////////////////////
/// Complex event representing a modification in the state of a complex
/// It holds:
///     - a vector of reactants, that are used to indicate complex reactions that
///       directly involve subunit states
///     - a vector of possible updates
///     - a potential change of location
class ComplexUpdateEvent: public ComplexLHSEvent {
  public:
    ComplexUpdateEvent(std::string const& cmplxId,
                       const std::vector<std::vector<SubunitStateFilter>>& filts,
                       const std::vector<uint>& reac,
                       const std::vector<ComplexUpdate>& upd,
                       Location destLoc);

    const std::vector<uint>& reactants() const noexcept {
        return preactants;
    }
    const std::vector<ComplexUpdate>& updates() const noexcept {
        return pupdates;
    }
    Location destLoc() const noexcept {
        return pdestLoc;
    }

  protected:
    const std::vector<uint> preactants;
    const std::vector<ComplexUpdate> pupdates;
    const Location pdestLoc;
};

////////////////////////////////////////////////////////////////////////////////
/// Complex event representing the deletion of a complex
class ComplexDeleteEvent: public ComplexLHSEvent {
  public:
    ComplexDeleteEvent(std::string const& cmplxId,
                       const std::vector<std::vector<SubunitStateFilter>>& filt);
};

}  // namespace steps::model

// END
