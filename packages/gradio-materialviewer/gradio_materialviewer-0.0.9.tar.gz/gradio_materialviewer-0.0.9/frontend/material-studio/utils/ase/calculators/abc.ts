/**
 * This module defines abstract helper classes with the objective of reducing
 * boilerplace method definitions (i.e. duplication) in calculators.
 */

interface Mapping {
    [key: string]: any;
}

export abstract class GetPropertiesMixin {
    /**
     * Mixin class which provides get_forces(), get_stress() and so on.
     *
     * Inheriting class must implement get_property().
     */

    abstract getProperty(name: string, atoms?: any, allowCalculation?: boolean): any;

    getPotentialEnergy(atoms?: any, forceConsistent: boolean = false): any {
        const name = forceConsistent ? 'free_energy' : 'energy';
        return this.getProperty(name, atoms);
    }

    getPotentialEnergies(atoms?: any): any {
        return this.getProperty('energies', atoms);
    }

    getForces(atoms?: any): any {
        return this.getProperty('forces', atoms);
    }

    getStress(atoms?: any): any {
        return this.getProperty('stress', atoms);
    }

    getStresses(atoms?: any): any {
        /**
         * The calculator should return intensive stresses, i.e., such that
         * stresses.sum(axis=0) == stress
         */
        return this.getProperty('stresses', atoms);
    }

    getDipoleMoment(atoms?: any): any {
        return this.getProperty('dipole', atoms);
    }

    getCharges(atoms?: any): any {
        return this.getProperty('charges', atoms);
    }

    getMagneticMoment(atoms?: any): any {
        return this.getProperty('magmom', atoms);
    }

    getMagneticMoments(atoms?: any): any {
        /**
         * Calculate magnetic moments projected onto atoms.
         */
        return this.getProperty('magmoms', atoms);
    }
}

export abstract class GetOutputsMixin {
    /**
     * Mixin class for providing get_fermi_level() and others.
     *
     * Effectively this class expresses data in calc.results as
     * methods such as get_fermi_level().
     *
     * Inheriting class must implement _outputmixin_get_results(),
     * typically returning self.results, which must be a mapping
     * using the naming defined in ase.outputs.Properties.
     */

    abstract _outputMixinGetResults(): Mapping;

    private _get(name: string): any {
        // Cyclic import, should restructure.
        const results = this._outputMixinGetResults();
        if (results[name] !== undefined) {
            return results[name];
        } else {
            throw new Error(`PropertyNotPresent: ${name}`);
        }
    }

    getFermiLevel(): any {
        return this._get('fermi_level');
    }

    getIbzKPoints(): any {
        return this._get('ibz_kpoints');
    }

    getKPointWeights(): any {
        return this._get('kpoint_weights');
    }

    getEigenvalues(kpt: number = 0, spin: number = 0): any {
        const eigs = this._get('eigenvalues');
        return eigs[spin][kpt];
    }

    private _eigshape(): number[] {
        // We don't need this if we already have a Properties object.
        return this._get('eigenvalues').shape;
    }

    getOccupationNumbers(kpt: number = 0, spin: number = 0): any {
        const occs = this._get('occupations');
        return occs[spin][kpt];
    }

    getNumberOfBands(): number {
        return this._eigshape()[2];
    }

    getNumberOfSpins(): number {
        const nspins = this._eigshape()[0];
        if (nspins !== 1 && nspins !== 2) {
            throw new Error('Number of spins must be 1 or 2');
        }
        return nspins;
    }

    getSpinPolarized(): boolean {
        return this.getNumberOfSpins() === 2;
    }
}
