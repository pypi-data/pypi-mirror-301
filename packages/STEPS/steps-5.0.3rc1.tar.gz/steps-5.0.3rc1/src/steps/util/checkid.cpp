/*
 ___license_placeholder___
 */

#include <string>

#include "checkid.hpp"
#include "util/error.hpp"
// logging
namespace steps::util {

static inline bool ascii_is_alpha(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_';
}

static inline bool ascii_is_alphanum(char c) {
    // return ascii_is_alpha(c) || (c >= '0' && c <= '9');
    // TODO revert this temporary change for split meshes
    return ascii_is_alpha(c) || (c >= '0' && c <= '9') || c == '.';
}

bool isValidID(const char* s) {
    if (!ascii_is_alpha(*s)) {
        return false;
    }
    while (*++s != 0) {
        if (!ascii_is_alphanum(*s)) {
            return false;
        }
    }

    return true;
}

bool isValidID(const std::string& s) {
    return isValidID(s.c_str());
}

void checkID(const char* s) {
    ArgErrLogIf(!isValidID(s), "'" + std::string(s) + "' is not a valid id.");
}

void checkID(const std::string& s) {
    ArgErrLogIf(!isValidID(s), "'" + s + "' is not a valid id.");
}

}  // namespace steps::util
