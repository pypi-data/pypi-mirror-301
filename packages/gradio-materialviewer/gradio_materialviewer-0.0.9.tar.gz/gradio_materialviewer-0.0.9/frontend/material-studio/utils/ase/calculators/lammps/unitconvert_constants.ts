import { sqrt } from 'mathjs';

// Constants
export const boltz_si = 1.38064852e-23; // [J K^-1] Boltzmann's factor (NIST value)
export const Nav = 6.022140857e23; // [unitless] Avogadro's number
export const mole_si = Nav; // [unitless] Avogadro's number (alias)
export const me_si = 9.10938356e-31; // [kg] electron rest mass
export const e_si = 1.6021766208e-19; // [C] elementary charge

// Distance units
export const meter_si = 1.0;
export const bohr_si = 5.2917721067e-11; // [m] Bohr unit (distance between nucleus and electron in H)
export const angstrom_si = 1e-10; // [m] Angstrom
export const centimeter_si = 1e-2; // [m] centimeter
export const micrometer_si = 1e-6; // [m] micrometer (micron)
export const nanometer_si = 1e-9; // [m] nanometer

// Mass units
export const kilogram_si = 1.0;
export const gram_per_mole_si = 1e-3 / Nav; // [kg] gram per mole i.e. amu
export const amu_si = gram_per_mole_si; // [kg] gram per mole i.e. amu
export const gram_si = 1e-3; // [kg] gram
export const picogram_si = 1e-15; // [kg] picogram
export const attogram_si = 1e-21; // [kg] attogram

// Time units
export const second_si = 1.0;
export const atu_si = 2.418884326509e-17; // [s] atomic time unit ( = hbar/E_h where E_h is the Hartree energy) (NIST value)
export const atu_electron_si = atu_si * (sqrt(amu_si / me_si) as number); // [s] atomic time unit used in electron system
export const microsecond_si = 1e-6; // [s] microsecond
export const nanosecond_si = 1e-9; // [s] nanosecond
export const picosecond_si = 1e-12; // [s] picosecond
export const femtosecond_si = 1e-15; // [s] femtosecond

// Density units
export const gram_per_centimetercu_si = gram_si / Math.pow(centimeter_si, 3); // [kg/m^3] gram/centimeter^3
export const amu_per_bohrcu_si = amu_si / Math.pow(bohr_si, 3); // [kg/m^3] amu/bohr^3
export const picogram_per_micrometercu_si = picogram_si / Math.pow(micrometer_si, 3); // [kg/m^3] picogram/micrometer^3
export const attogram_per_nanometercu_si = attogram_si / Math.pow(nanometer_si, 3); // [kg/m^3] attogram/nanometer^3

// Energy/torque units
export const joule_si = 1.0;
export const kcal_si = 4184.0; // [J] kilocalorie (heat energy involved in warming up one kilogram of water by one degree Kelvin)
export const ev_si = 1.6021766208e-19; // [J] electron volt (amount of energy gained or lost by the charge of a single electron moving across an electric potential difference of one volt.) (NIST value)
export const hartree_si = 4.35974465e-18; // [J] Hartree (approximately the electric potential energy of the hydrogen atom in its ground state) (NIST value)
export const kcal_per_mole_si = kcal_si / Nav; // [J] kcal/mole
export const erg_si = 1e-7; // [J] erg
export const dyne_centimeter_si = 1e-7; // [J] dyne*centimeter
export const picogram_micrometersq_per_microsecondsq_si =
    (picogram_si * Math.pow(micrometer_si, 2)) / Math.pow(microsecond_si, 2); // [J] picogram*micrometer^2/microsecond^2
export const attogram_nanometersq_per_nanosecondsq_si =
    (attogram_si * Math.pow(nanometer_si, 2)) / Math.pow(nanosecond_si, 2); // [J] attogram*nanometer^2/nanosecond^2

// Velocity units
export const meter_per_second_si = 1.0;
export const angstrom_per_femtosecond_si = angstrom_si / femtosecond_si; // [m/s] Angstrom/femtosecond
export const angstrom_per_picosecond_si = angstrom_si / picosecond_si; // [m/s] Angstrom/picosecond
export const micrometer_per_microsecond_si = micrometer_si / microsecond_si; // [m/s] micrometer/microsecond
export const nanometer_per_nanosecond_si = nanometer_si / nanosecond_si; // [m/s] nanometer/nanosecond
export const centimeter_per_second_si = centimeter_si; // [m/s] centimeter/second
export const bohr_per_atu_si = bohr_si / atu_electron_si; // [m/s] bohr/atu

// Force units
export const newton_si = 1.0;
export const kcal_per_mole_angstrom_si = kcal_per_mole_si / angstrom_si; // [N] kcal/(mole*Angstrom)
export const ev_per_angstrom_si = ev_si / angstrom_si; // [N] eV/Angstrom
export const dyne_si = dyne_centimeter_si / centimeter_si; // [N] dyne
export const hartree_per_bohr_si = hartree_si / bohr_si; // [N] hartree/bohr
export const picogram_micrometer_per_microsecondsq_si = (picogram_si * micrometer_si) / Math.pow(microsecond_si, 2); // [N] picogram*micrometer/microsecond^2
export const attogram_nanometer_per_nanosecondsq_si = (attogram_si * nanometer_si) / Math.pow(nanosecond_si, 2); // [N] attogram*nanometer/nanosecond^2

// Temperature units
export const kelvin_si = 1.0;

// Pressure units
export const pascal_si = 1.0;
export const atmosphere_si = 101325.0; // [Pa] standard atmosphere (NIST value)
export const bar_si = 1e5; // [Pa] bar
export const dyne_per_centimetersq_si = dyne_centimeter_si / Math.pow(centimeter_si, 3); // [Pa] dyne/centimeter^2
export const picogram_per_micrometer_microsecondsq_si = picogram_si / (micrometer_si * Math.pow(microsecond_si, 2)); // [Pa] picogram/(micrometer*microsecond^2)
export const attogram_per_nanometer_nanosecondsq_si = attogram_si / (nanometer_si * Math.pow(nanosecond_si, 2)); // [Pa] attogram/(nanometer*nanosecond^2)

// Viscosity units
export const poise_si = 0.1; // [Pa*s] Poise
export const amu_per_bohr_femtosecond_si = amu_si / (bohr_si * femtosecond_si); // [Pa*s] amu/(bohr*femtosecond)
export const picogram_per_micrometer_microsecond_si = picogram_si / (micrometer_si * microsecond_si); // [Pa*s] picogram/(micrometer*microsecond)
export const attogram_per_nanometer_nanosecond_si = attogram_si / (nanometer_si * nanosecond_si); // [Pa*s] attogram/(nanometer*nanosecond)

// Charge units
export const coulomb_si = 1.0;
export const echarge_si = e_si; // [C] electron charge unit
export const statcoulomb_si = e_si / 4.8032044e-10; // [C] Statcoulomb or esu (value from LAMMPS units documentation)
export const picocoulomb_si = 1e-12; // [C] picocoulomb

// Dipole units
export const coulomb_meter_si = 1;
export const electron_angstrom_si = echarge_si * angstrom_si; // [C*m] electron*angstrom
export const statcoulomb_centimeter_si = statcoulomb_si * centimeter_si; // [C*m] statcoulomb*centimeter
export const debye_si = 1e-18 * statcoulomb_centimeter_si; // [C*m] Debye
export const picocoulomb_micrometer_si = picocoulomb_si * micrometer_si; // [C*m] picocoulomb*micrometer
export const electron_nanometer_si = echarge_si * nanometer_si; // [C*m] electron*nanometer

// Electric field units
export const volt_si = 1.0;
export const volt_per_meter_si = 1;
export const volt_per_angstrom_si = 1.0 / angstrom_si; // [V/m] volt/angstrom
export const statvolt_per_centimeter_si = erg_si / (statcoulomb_si * centimeter_si); // [V/m] statvolt/centimeter
export const volt_per_centimeter_si = 1.0 / centimeter_si; // [V/m] volt/centimeter
export const volt_per_micrometer_si = 1.0 / micrometer_si; // [V/m] volt/micrometer
export const volt_per_nanometer_si = 1.0 / nanometer_si; // [V/m] volt/nanometer
