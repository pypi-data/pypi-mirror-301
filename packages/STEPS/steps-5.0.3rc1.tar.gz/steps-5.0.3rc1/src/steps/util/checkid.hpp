/*
 ___license_placeholder___
 */

#pragma once

#include <string>

namespace steps::util {

/** Test string for validity as steps object identifier.
 *
 * \param s  ID string.
 * \return   True if valid.
 *
 * Valid ID strings consist of an alphabetic character [A-Za-z_]
 * followed by a possibly empty sequence of alphanumeric characters
 * [A-Za-z_0-9].
 */
bool isValidID(const char* s);

/** Test string for validity as steps object identifier.
 *
 * \param s  ID string.
 * \return   True if valid.
 *
 * See isValidID(const char *)
 */
bool isValidID(const std::string& s);

/** Throw exception if string is an invalid identifier.
 *
 * \param s  ID string.
 *
 * Throws steps::ArgErr if isValidID(s) is false.
 */
void checkID(const char* s);

/** Throw exception if string is an invalid identifier.
 *
 * \param s  ID string.
 *
 * Throws steps::ArgErr if isValidID(s) is false.
 */
void checkID(const std::string& s);

}  // namespace steps::util
