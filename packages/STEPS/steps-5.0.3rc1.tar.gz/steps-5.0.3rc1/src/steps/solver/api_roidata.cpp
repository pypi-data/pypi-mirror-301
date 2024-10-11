/*
 ___license_placeholder___
 */

#include "api.hpp"

#include "util/error.hpp"

namespace steps::solver {

std::vector<double> API::getROITetSpecCounts(const std::string& /*ROI_id*/,
                                             std::string const& /*s*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

std::vector<double> API::getROITriSpecCounts(const std::string& /*ROI_id*/,
                                             std::string const& /*s*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::getROITetSpecCountsNP(const std::string& /*ROI_id*/,
                                std::string const& /*s*/,
                                double* /*counts*/,
                                size_t /*output_size*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::getROITriSpecCountsNP(const std::string& /*ROI_id*/,
                                std::string const& /*s*/,
                                double* /*counts*/,
                                size_t /*output_size*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

double API::getROIVol(const std::string& /*ROI_id*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

double API::getROIArea(const std::string& /*ROI_id*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

double API::getROISpecCount(const std::string& /*ROI_id*/, std::string const& /*s*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISpecCount(const std::string& /*ROI_id*/,
                          std::string const& /*s*/,
                          double /*count*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

double API::getROISpecAmount(const std::string& /*ROI_id*/, std::string const& /*s*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISpecAmount(const std::string& /*ROI_id*/,
                           std::string const& /*s*/,
                           double /*amount*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

double API::getROISpecConc(const std::string& /*ROI_id*/, std::string const& /*s*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISpecConc(const std::string& /*ROI_id*/, std::string const& /*s*/, double /*conc*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISpecClamped(const std::string& /*ROI_id*/, std::string const& /*s*/, bool /*b*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROIReacK(const std::string& /*ROI_id*/, std::string const& /*r*/, double /*kf*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISReacK(const std::string& /*ROI_id*/, std::string const& /*sr*/, double /*kf*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROIDiffD(const std::string& /*ROI_id*/, std::string const& /*d*/, double /*dk*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROIReacActive(const std::string& /*ROI_id*/, std::string const& /*r*/, bool /*a*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROISReacActive(const std::string& /*ROI_id*/, std::string const& /*sr*/, bool /*a*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROIDiffActive(const std::string& /*ROI_id*/, std::string const& /*d*/, bool /*act*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setROIVDepSReacActive(const std::string& /*ROI_id*/,
                                std::string const& /*vsr*/,
                                bool /*a*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

unsigned long long API::getROIReacExtent(const std::string& /*ROI_id*/,
                                         std::string const& /*r*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::resetROIReacExtent(const std::string& /*ROI_id*/, std::string const& /*r*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

unsigned long long API::getROISReacExtent(const std::string& /*ROI_id*/,
                                          std::string const& /*sr*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::resetROISReacExtent(const std::string& /*ROI_id*/, std::string const& /*sr*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

unsigned long long API::getROIDiffExtent(const std::string& /*ROI_id*/,
                                         std::string const& /*d*/) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::resetROIDiffExtent(const std::string& /*ROI_id*/, std::string const& /*d*/) {
    NotImplErrLog("");
}

}  // namespace steps::solver
