/*
 ___license_placeholder___
 */

/* \brief math/smallsort.hpp
 *  Inline sorting of small, fixed-size random-access sequences.
 */

#pragma once

#include <algorithm>
#include <iostream>
#include <utility>

#ifndef GNU_FORCE_INLINE
#define GNU_FORCE_INLINE
#endif

namespace steps::math {

namespace impl {
// compare-and-sort two elements of a:

template <int m, int n>
struct S {
    template <typename A>
    GNU_FORCE_INLINE static void run(A& a) {
        if (a[m] > a[n])
            std::swap(a[m], a[n]);
    }
};

// minimal networks up to 6, then recusive merge

template <int n, typename A>
struct small_sort_inplace {
    GNU_FORCE_INLINE static void run(A& a) {
        std::sort(std::begin(a), std::end(a));
    }
};

template <typename A>
struct small_sort_inplace<0, A> {
    static void run(A& /*a*/) {}
};

template <typename A>
struct small_sort_inplace<1, A> {
    static void run(A& /*a*/) {}
};

template <typename A>
struct small_sort_inplace<2, A> {
    GNU_FORCE_INLINE static void run(A& a) {
        S<0, 1>::run(a);
    }
};

template <typename A>
struct small_sort_inplace<3, A> {
    GNU_FORCE_INLINE static void run(A& a) {
        S<0, 1>::run(a);
        S<1, 2>::run(a);
        S<0, 1>::run(a);
    }
};

template <typename A>
struct small_sort_inplace<4, A> {
    GNU_FORCE_INLINE static void run(A& a) {
        S<0, 1>::run(a);
        S<2, 3>::run(a);
        S<0, 2>::run(a);
        S<1, 3>::run(a);
        S<1, 2>::run(a);
    }
};

template <typename A>
struct small_sort_inplace<5, A> {
    GNU_FORCE_INLINE static void run(A& a) {
        S<0, 1>::run(a);
        S<2, 4>::run(a);
        S<0, 3>::run(a);
        S<1, 4>::run(a);
        S<1, 2>::run(a);
        S<3, 4>::run(a);
        S<0, 1>::run(a);
        S<2, 3>::run(a);
        S<1, 2>::run(a);
    }
};

template <typename A>
struct small_sort_inplace<6, A> {
    GNU_FORCE_INLINE static void run(A& a) {
        S<0, 1>::run(a);
        S<2, 3>::run(a);
        S<4, 5>::run(a);
        S<0, 2>::run(a);
        S<1, 4>::run(a);
        S<3, 5>::run(a);
        S<0, 1>::run(a);
        S<2, 3>::run(a);
        S<4, 5>::run(a);
        S<1, 2>::run(a);
        S<3, 4>::run(a);
        S<2, 3>::run(a);
    }
};

}  // namespace impl

template <int n, typename A>
GNU_FORCE_INLINE inline void small_sort_inplace(A& a) {
    impl::small_sort_inplace<n, A>::run(a);
}

template <int n, typename A>
GNU_FORCE_INLINE inline A small_sort(A a) {
    impl::small_sort_inplace<n, A>::run(a);
    return a;
}

}  // namespace steps::math
