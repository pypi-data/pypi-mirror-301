/*
 ___license_placeholder___
 */

#pragma once

#include <cinttypes>

#include "type_traits.hpp"

/** /file Hashing support for aggregates, containers, based
 * on the Fowler-Noll-Vo FNV-1a hash function.
 */

namespace steps::util {

typedef uint64_t hash_type;

template <typename T>
inline hash_type fnv1a_combine(hash_type h, const T& v) {
    const unsigned char* k = reinterpret_cast<const unsigned char*>(&v);
    for (size_t i = 0; i < sizeof(T); ++i) {
        h ^= k[i];
        h *= 0x100000001b3ull;
    }
    return h;
}

template <typename T, typename... Rest>
inline hash_type fnv1a_combine(hash_type h, const T& v, const Rest&... vs) {
    return fnv1a_combine(fnv1a_combine(h, v), vs...);
}

template <typename... T>
inline hash_type fnv1a(const T&... vs) {
    return fnv1a_combine(0xcbf29ce484222325ull, vs...);
}

namespace impl {
template <typename T, typename enable = void>
struct fnv_hash;

template <typename T>
struct fnv_hash<T, typename std::enable_if<is_scalar_or_array<T>::value>::type> {
    size_t operator()(const T& v) const {
        return static_cast<size_t>(fnv1a(v));
    }
};
}  // namespace impl

/* Define fnv::hash for scalar types and arrays of scalar types by default */

template <typename T>
struct fnv_hash: impl::fnv_hash<T> {};

}  // namespace steps::util
