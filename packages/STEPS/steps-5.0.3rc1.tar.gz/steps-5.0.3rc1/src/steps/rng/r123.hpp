/*
 ___license_placeholder___
 */

#pragma once

// STEPS headers.
#include "Random123/philox.h"
#include "rng.hpp"

namespace steps::rng {

////////////////////////////////////////////////////////////////////////////////

// Based on the original Mersenne Twister code (mt19937.c).
//
// Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
//
//   1. Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//   2. Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//   3. The names of its contributors may not be used to endorse or promote
//      products derived from this software without specific prior written
//      permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER
// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Any feedback is very welcome.
// http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
// email: m-mat @ math.sci.hiroshima-u.ac.jp (remove space)

class R123: public RNG {
  public:
    /// R123 Philox typedef
    typedef r123::Philox4x32_R<8> r123_type;

    /// Constructor
    ///
    /// \param bufsize Size of the buffer.
    explicit R123(uint bufsize)
        : RNG(bufsize) {}

    /// Destructor
    ///
    virtual ~R123() {}

    void checkpoint(std::ostream& cp_file) const override;

    void restore(std::istream& cp_file) override;

  protected:
    /// Initialize the generator with seed.
    ///
    /// \param seed Seed for the generator.
    virtual void concreteInitialize(unsigned long seed) override;

    /// Fills the buffer with random numbers on [0,0xffffffff]-interval.
    ///
    virtual void concreteFillBuffer() override;

  private:
    r123_type::key_type key;
    r123_type::ctr_type ctr;
    r123_type r;
};

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::rng
