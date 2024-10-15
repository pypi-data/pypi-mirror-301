/**
 * ase.units
 *
 * Physical constants and units derived from CODATA for converting
 * to and from ase internal units.
 */

import { pi, sqrt } from 'mathjs';

// the version we actually use
const __codata_version__ = '2014';

// Dictionary for units that supports .attribute access
class Units {
    [key: string]: number;

    constructor(initialData: { [key: string]: number }) {
        Object.assign(this, initialData);
    }
}

// this is the hard-coded CODATA values
const CODATA: { [key: string]: { [key: string]: number } } = {
    // the "original" CODATA version ase used ever since
    // Constants from Konrad Hinsen's PhysicalQuantities module (1986 CODATA)
    // Add the constant pi used to define the mu0 and hbar here for reference
    // as well
    '1986': {
        _c: 299792458, // speed of light, m/s
        _mu0: 4e-7 * pi, // permeability of vacuum
        _Grav: 6.67259e-11, // gravitational constant
        _hplanck: 6.6260755e-34, // Planck constant, J s
        _e: 1.60217733e-19, // elementary charge
        _me: 9.1093897e-31, // electron mass
        _mp: 1.6726231e-27, // proton mass
        _Nav: 6.0221367e23, // Avogadro number
        _k: 1.380658e-23, // Boltzmann constant, J/K
        _amu: 1.6605402e-27,
    }, // atomic mass unit, kg

    // CODATA 1998 taken from
    // https://doi.org/10.1103/RevModPhys.72.351
    '1998': {
        _c: 299792458,
        _mu0: 4.0e-7 * pi,
        _Grav: 6.673e-11,
        _hplanck: 6.62606876e-34,
        _e: 1.602176462e-19,
        _me: 9.10938188e-31,
        _mp: 1.67262158e-27,
        _Nav: 6.02214199e23,
        _k: 1.3806503e-23,
        _amu: 1.66053873e-27,
    },

    // CODATA 2002 taken from
    // https://doi.org/10.1103/RevModPhys.77.1
    '2002': {
        _c: 299792458,
        _mu0: 4.0e-7 * pi,
        _Grav: 6.6742e-11,
        _hplanck: 6.6260693e-34,
        _e: 1.60217653e-19,
        _me: 9.1093826e-31,
        _mp: 1.67262171e-27,
        _Nav: 6.0221415e23,
        _k: 1.3806505e-23,
        _amu: 1.66053886e-27,
    },

    // CODATA 2006 taken from
    // https://doi.org/10.1103/RevModPhys.80.633
    '2006': {
        _c: 299792458,
        _mu0: 4.0e-7 * pi,
        _Grav: 6.67428e-11,
        _hplanck: 6.62606896e-34,
        _e: 1.602176487e-19,
        _me: 9.10938215e-31,
        _mp: 1.672621637e-27,
        _Nav: 6.02214179e23,
        _k: 1.3806504e-23,
        _amu: 1.660538782e-27,
    },

    // CODATA 2010 taken from
    // https://doi.org/10.1103/RevModPhys.84.1527
    '2010': {
        _c: 299792458,
        _mu0: 4.0e-7 * pi,
        _Grav: 6.67384e-11,
        _hplanck: 6.62606957e-34,
        _e: 1.602176565e-19,
        _me: 9.10938291e-31,
        _mp: 1.672621777e-27,
        _Nav: 6.02214129e23,
        _k: 1.3806488e-23,
        _amu: 1.660538921e-27,
    },

    // CODATA 2014 taken from
    // http://arxiv.org/pdf/1507.07956.pdf
    '2014': {
        _c: 299792458,
        _mu0: 4.0e-7 * pi,
        _Grav: 6.67408e-11,
        _hplanck: 6.62607004e-34,
        _e: 1.6021766208e-19,
        _me: 9.10938356e-31,
        _mp: 1.672621898e-27,
        _Nav: 6.022140857e23,
        _k: 1.38064852e-23,
        _amu: 1.66053904e-27,
    },

    // CODATA 2018 taken from
    // https://physics.nist.gov/cuu/Constants/index.html
    '2018': {
        _c: 299792458, // Exact
        _mu0: 4.0e-7 * pi, // Exact
        _Grav: 6.6743e-11, // +/- 0.000_15e-11
        _hplanck: 6.62607015e-34, // Exact
        _e: 1.602176634e-19, // Exact
        _me: 9.1093837015e-31, // +/- 0.000_000_0028e-31
        _mp: 1.67262192369e-27, // +/- 0.000_000_000_51e-27
        _Nav: 6.02214076e23, // Exact
        _k: 1.380649e-23, // Exact
        _amu: 1.6605390666e-27,
    }, // +/- 0.000_000_000_50e-27
};

function create_units(codata_version: string): Units {
    let u: Units;

    try {
        u = new Units(CODATA[codata_version]);
    } catch (e) {
        throw new Error(`CODATA version "${codata_version}" not implemented`);
    }

    // derived from the CODATA values
    u['_eps0'] = 1 / u['_mu0'] / u['_c'] ** 2;
    u['_hbar'] = u['_hplanck'] / (2 * pi);

    u['Ang'] = u['Angstrom'] = 1.0;
    u['nm'] = 10.0;
    u['Bohr'] = (4e10 * pi * u['_eps0'] * u['_hbar'] ** 2) / u['_me'] / u['_e'] ** 2;

    u['eV'] = 1.0;
    u['Hartree'] = (u['_me'] * u['_e'] ** 3) / 16 / pi ** 2 / u['_eps0'] ** 2 / u['_hbar'] ** 2;
    u['kJ'] = 1000.0 / u['_e'];
    u['kcal'] = 4.184 * u['kJ'];
    u['mol'] = u['_Nav'];
    u['Rydberg'] = 0.5 * u['Hartree'];
    u['Ry'] = u['Rydberg'];
    u['Ha'] = u['Hartree'];

    u['second'] = 1e10 * (sqrt(u['_e'] / u['_amu']) as number);
    u['fs'] = 1e-15 * u['second'];

    u['kB'] = u['_k'] / u['_e'];

    u['Pascal'] = 1 / u['_e'] / 1e30;
    u['GPa'] = 1e9 * u['Pascal'];
    u['bar'] = 1e5 * u['Pascal'];

    u['Debye'] = 1.0 / 1e11 / u['_e'] / u['_c'];
    u['alpha'] = u['_e'] ** 2 / (4 * pi * u['_eps0']) / u['_hbar'] / u['_c'];
    u['invcm'] = (100 * u['_c'] * u['_hplanck']) / u['_e'];

    u['_aut'] = u['_hbar'] / (u['alpha'] ** 2 * u['_me'] * u['_c'] ** 2);
    u['_auv'] = u['_e'] ** 2 / u['_hbar'] / (4 * pi * u['_eps0']);
    u['_auf'] = (u['alpha'] ** 3 * u['_me'] ** 2 * u['_c'] ** 3) / u['_hbar'];
    u['_aup'] = (u['alpha'] ** 5 * u['_me'] ** 4 * u['_c'] ** 5) / u['_hbar'] ** 3;

    u['AUT'] = u['second'] * u['_aut'];

    // SI units
    u['m'] = 1e10 * u['Ang'];
    u['kg'] = 1 / u['_amu'];
    u['s'] = u['second'];
    u['A'] = 1.0 / u['_e'] / u['s'];
    u['J'] = u['kJ'] / 1000;
    u['C'] = 1.0 / u['_e'];

    return u;
}

// Define all the expected symbols with dummy values so that introspection
// will know that they exist when the module is imported, even though their
// values are immediately overwritten.
// Now update the module scope:
export const units = create_units(__codata_version__);

// const {
//     _Grav,
//     _Nav,
//     _amu,
//     _auf,
//     _aup,
//     _aut,
//     _auv,
//     _c,
//     _e,
//     _eps0,
//     _hbar,
//     _hplanck,
//     _k,
//     _me,
//     _mp,
//     _mu0,
//     alpha,
//     eV,
//     fs,
//     invcm,
//     kB,
//     kJ,
//     kcal,
//     kg,
//     m,
//     mol,
//     nm,
//     s,
//     second,
//     A,
//     AUT,
//     Ang,
//     Angstrom,
//     Bohr,
//     C,
//     Debye,
//     GPa,
//     Ha,
//     Hartree,
//     J,
//     Pascal,
//     bar,
//     Ry,
//     Rydberg,
// } = units;
