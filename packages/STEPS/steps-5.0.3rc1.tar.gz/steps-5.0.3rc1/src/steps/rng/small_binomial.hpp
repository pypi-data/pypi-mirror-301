/*
   ___license_placeholder___
   */

#pragma once

namespace steps::rng {

// Produces random non-negative integer values distributed according to the
// binomial probability distribution. This class is optimized for small
// number of trials t.
// \param t Number of trials
// \param p Probability of single trial
template <class IntType = int>
class small_binomial_distribution {
  public:
    typedef IntType result_type;

    explicit small_binomial_distribution(IntType t = 1, double p = 0.5)
        : t_(t)
        , p_(p) {}

    template <class Generator>
    result_type operator()(Generator& g) {
        result_type tot(0);
        // limits are inclusive, we add 1 to the right one so that "<" produces the
        // correct output
        const double s(static_cast<double>(g.max()) - static_cast<double>(g.min()) + 1.0);

        for (IntType tt = 0; tt < t_; ++tt) {
            const auto val_g = g();

            if (static_cast<double>(val_g - g.min()) < p_ * s) {
                ++tot;
            }
        }
        return tot;
    }

    double p() const {
        return p_;
    };
    result_type t() const {
        return t_;
    };
    void reset(){};

    result_type min() const {
        return 0;
    };
    result_type max() const {
        return t_;
    };

  private:
    IntType t_;
    double p_;
};

}  // namespace steps::rng
