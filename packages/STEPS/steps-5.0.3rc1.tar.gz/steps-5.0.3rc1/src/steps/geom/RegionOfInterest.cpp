/*
 ___license_placeholder___
 */

#include "RegionOfInterest.hpp"

#include "util/error.hpp"

namespace steps::tetmesh {

template <ROIType value>
typename ROITypeTraits<value>::roi_map_type::const_iterator
RegionOfInterest::get(const std::string& id, unsigned int count, bool warning) const {
    auto const& eax = ROITypeTraits<value>::get_container(*this).find(id);
    const auto end_it = end<value>();
    if (warning && eax == end_it) {
        CLOG(WARNING, "general_log") << "Unable to find ROI data with id " << id << ".\n";
    } else if (warning && count != 0 && eax->second.size() != count) {
        CLOG(WARNING, "general_log") << "Element count mismatch for ROI " << id << ".\n";
        return end_it;
    }
    return eax;
}

// explicit template instantiation definitions
template typename ROITypeTraits<ROI_VERTEX>::roi_map_type::const_iterator
RegionOfInterest::get<ROI_VERTEX>(const std::string& id,
                                  unsigned int count = 0,
                                  bool warning = true) const;
template typename ROITypeTraits<ROI_TRI>::roi_map_type::const_iterator
RegionOfInterest::get<ROI_TRI>(const std::string& id,
                               unsigned int count = 0,
                               bool warning = true) const;
template typename ROITypeTraits<ROI_TET>::roi_map_type::const_iterator
RegionOfInterest::get<ROI_TET>(const std::string& id,
                               unsigned int count = 0,
                               bool warning = true) const;

}  // namespace steps::tetmesh
