/*
 ___license_placeholder___
 */


// Standard library & STL headers.
#include <iostream>
#include <string>

// STEPS headers.
#include "create.hpp"
#include "mt19937.hpp"
#include "r123.hpp"
#include "std_mt19937.hpp"
// util
#include "util/error.hpp"
// logging
////////////////////////////////////////////////////////////////////////////////

namespace steps::rng {

RNGptr create(const std::string& rng_name, uint bufsize) {
    if (rng_name == "mt19937") {
        return RNGptr(new MT19937(bufsize));
    } else if (rng_name == "r123") {
        return RNGptr(new R123(bufsize));
    } else if (rng_name == "std::mt19937") {
        return RNGptr(new STDMT19937(bufsize));
    } else {
        ArgErrLog("Random number generator " + rng_name + " currently not included in STEPS.");
    }
}

RNGptr create_mt19937(uint bufsize) {
    return RNGptr(new MT19937(bufsize));
}

}  // namespace steps::rng
