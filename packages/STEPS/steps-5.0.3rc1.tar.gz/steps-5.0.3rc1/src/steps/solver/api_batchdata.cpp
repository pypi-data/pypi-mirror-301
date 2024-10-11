/*
 ___license_placeholder___
 */

#include "api.hpp"

#include "util/error.hpp"

namespace steps::solver {

std::vector<double> API::getBatchTetSpecCounts(const std::vector<index_t>& /* tets */,
                                               std::string const& /* s */) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

std::vector<double> API::getBatchTetSpecConcs(const std::vector<index_t>& /* tets */,
                                              std::string const& /* s */) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setBatchTetSpecConcs(const std::vector<index_t>& /*tets*/,
                               std::string const& /*s*/,
                               const std::vector<double>& /*concs*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

std::vector<double> API::getBatchTriSpecCounts(const std::vector<index_t>& /* tris */,
                                               std::string const& /* s */) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::getBatchTetSpecCountsNP(const index_t* /* indices */,
                                  size_t /* input_size */,
                                  std::string const& /* s */,
                                  double* /* counts */,
                                  size_t /* output_size */) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::getBatchTetSpecConcsNP(const index_t* /* indices */,
                                 size_t /* input_size */,
                                 std::string const& /* s */,
                                 double* /* counts */,
                                 size_t /* output_size */) const {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::setBatchTetSpecConcsNP(const index_t* /*indices*/,
                                 size_t /*ntets*/,
                                 std::string const& /*s*/,
                                 const double* /*concs*/,
                                 size_t /*output_size*/) {
    NotImplErrLog("");
}

////////////////////////////////////////////////////////////////////////////////

void API::getBatchTriSpecCountsNP(const index_t* /* indices */,
                                  size_t /* input_size */,
                                  std::string const& /* s */,
                                  double* /* counts */,
                                  size_t /* output_size */) const {
    NotImplErrLog("");
}

}  // namespace steps::solver
