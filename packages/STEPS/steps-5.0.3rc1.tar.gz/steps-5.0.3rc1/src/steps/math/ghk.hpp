/*
 ___license_placeholder___
 */

#pragma once

namespace steps::math {

////////////////////////////////////////////////////////////////////////////////

// Return the permeability in the GHK flux equation from given values of:
// G (slope conductance in siemens), V (voltage in volts), z (valence),
// T (temperature in kelvin),
// iconc (inner concentration of ion in mol per litre),
// oconc (outer concentration of ion in mol per litre)

double permeability(double G, double V, int z, double T, double iconc, double oconc);

////////////////////////////////////////////////////////////////////////////////

// Return the single-channel current from the GHK flux equation from given
// value of:
// P (single-channel permeability in meters cubed/second), V (voltage in volts),
// z (valence), T (temperature in kelvin),
// iconc (inner concentration of ion in mol per cubic meter),
// oconc (outer concentration of ion in mol per cubic meter)

double GHKcurrent(double P, double V, int z, double T, double iconc, double oconc);

////////////////////////////////////////////////////////////////////////////////

}  // namespace steps::math
