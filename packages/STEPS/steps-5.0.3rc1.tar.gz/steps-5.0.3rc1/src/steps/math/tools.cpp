/*
 ___license_placeholder___
 */

#include "tools.hpp"

#include <ctime>

namespace steps::math {

void setSysRandInitTime() {
    srand(static_cast<unsigned int>(time(nullptr)));
}

}  // namespace steps::math
