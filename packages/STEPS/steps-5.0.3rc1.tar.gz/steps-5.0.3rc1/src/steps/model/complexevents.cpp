/*
 ___license_placeholder___
 */


#include "model/complexevents.hpp"

#include "util/error.hpp"

namespace steps::model {

ComplexEvent::ComplexEvent(std::string const& cmplxId)
    : pcomplexId(cmplxId) {}

ComplexCreateEvent::ComplexCreateEvent(std::string const& cmplxId, const std::vector<uint>& in)
    : ComplexEvent::ComplexEvent(cmplxId)
    , pinit(in) {}

ComplexLHSEvent::ComplexLHSEvent(std::string const& cmplxId,
                                 const std::vector<std::vector<SubunitStateFilter>>& filts)
    : ComplexEvent::ComplexEvent(cmplxId) {
    pfilters.reserve(filts.size());
    for (const auto& filt: filts) {
        pfilters.emplace_back(filt);
    }
}

ComplexUpdateEvent::ComplexUpdateEvent(std::string const& cmplxId,
                                       const std::vector<std::vector<SubunitStateFilter>>& filts,
                                       const std::vector<uint>& reac,
                                       const std::vector<ComplexUpdate>& upd,
                                       Location destLoc)
    : ComplexLHSEvent::ComplexLHSEvent(cmplxId, filts)
    , preactants(reac)
    , pupdates(upd)
    , pdestLoc(destLoc) {}

ComplexDeleteEvent::ComplexDeleteEvent(std::string const& cmplxId,
                                       const std::vector<std::vector<SubunitStateFilter>>& filts)
    : ComplexLHSEvent::ComplexLHSEvent(cmplxId, filts) {}


}  // namespace steps::model
