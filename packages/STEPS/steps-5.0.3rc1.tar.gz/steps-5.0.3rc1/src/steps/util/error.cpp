/*
 ___license_placeholder___
 */

#include "error.hpp"

namespace steps {

const char* Err::getMsg() const noexcept {
    return pMessage.c_str();
}

}  // namespace steps
