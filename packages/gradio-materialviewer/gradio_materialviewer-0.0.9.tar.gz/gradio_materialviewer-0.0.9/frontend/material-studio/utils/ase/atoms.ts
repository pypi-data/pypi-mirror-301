import * as math from 'mathjs';
import { Atom } from './ase/atom';
import { Cell } from './ase/cell';
import { atomic_masses, atomic_masses_common } from './ase/data';
import { full_3x3_to_voigt_6_stress, voigt_6_to_full_3x3_stress } from './ase/stress';
import { Symbols, symbols2numbers } from './ase/symbols';
import { deprecated, string2index } from './ase/utils';

export class Atoms {
    private _cellobj: any;
    private _pbc: boolean[];

    // Properties and methods here mirror Python definitions, adjusted for TypeScript
    constructor(
        symbols: string | string[] | Atom[] | null = null,
        positions: number[][] | null = null,
        numbers: number[] | null = null,
        tags: number[] | null = null,
        momenta: number[][] | null = null,
        masses: number[] | null = null,
        magmoms: number[] | null = null,
        charges: number[] | null = null,
        scaled_positions: number[][] | null = null,
        cell: number[][] | null = null,
        pbc: boolean[] | null = null,
        celldisp: number[] | null = null,
        constraint: any = null,
        calculator: any = null,
        info: any = null,
        velocities: number[][] | null = null
    ) {
        this._cellobj = Cell.new();
        this._pbc = [false, false, false]; // Assuming default pbc value

        let atoms: Atoms | null = null;

        // Conversion from Python-like structure to TypeScript
        if (symbols instanceof Atom || (Array.isArray(symbols) && symbols.length > 0 && symbols[0] instanceof Atom)) {
            // Handle case where symbols is a list of Atom objects
            // Conversion logic not implemented due to complexity
            throw new Error('Conversion from list of Atom objects not implemented in TypeScript.');
        }

        if (atoms !== null) {
            // Logic to initialize Atoms object from another Atoms object
            // Conversion logic not implemented due to complexity
            throw new Error('Initialization from another Atoms object not fully implemented in TypeScript.');
        }

        // Initialize arrays
        this.arrays = {};

        // Handle initialization based on provided arguments
        if (symbols === null) {
            if (numbers === null) {
                // Logic to handle case when numbers are not provided
                throw new Error('Initialization logic for numbers not fully implemented in TypeScript.');
            }
            this.new_array('numbers', numbers, 'int');
        } else {
            // Logic to handle symbols provided instead of numbers
            throw new Error('Handling symbols instead of numbers not fully implemented in TypeScript.');
        }

        if (this.numbers.length !== 1) {
            throw new Error('"numbers" must be 1-dimensional.');
        }

        if (cell === null) {
            cell = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ];
        }
        this.set_cell(cell);

        if (celldisp === null) {
            celldisp = [0, 0, 0];
        }
        this.set_celldisp(celldisp);

        if (positions === null) {
            if (scaled_positions === null) {
                positions = [[0, 0, 0]];
            } else {
                // Logic to handle scaled positions
                throw new Error('Handling scaled positions not fully implemented in TypeScript.');
            }
        } else {
            // Logic to handle positions provided directly
            throw new Error('Handling positions directly not fully implemented in TypeScript.');
        }

        // Handle constraints, tags, masses, momenta, magmoms, charges, pbc, velocities, info, calculator
        // Conversion logic not implemented due to complexity
        throw new Error('Handling constraints, tags, masses, etc. not fully implemented in TypeScript.');
    }

    private arrays: { [key: string]: any } = {};

    get symbols(): Symbols {
        // Getter for symbols
        return new Symbols(this.numbers);
    }

    set symbols(obj: any) {
        // Setter for symbols
        let newSymbols = Symbols.fromsymbols(obj);
        this.numbers = newSymbols.numbers;
    }

    @deprecated('Please use atoms.calc = calc')
    set_calculator(calc: any): void {
        // Deprecated setter for calculator
        this.calc = calc;
    }

    @deprecated('Please use atoms.calc')
    get_calculator(): any {
        // Deprecated getter for calculator
        return this.calc;
    }

    private _calc: any;

    get calc(): any {
        // Getter for calculator
        return this._calc;
    }

    set calc(calc: any) {
        // Setter for calculator
        this._calc = calc;
        if (calc.set_atoms) {
            calc.set_atoms(this);
        }
    }

    @deprecated('Please use atoms.cell.rank instead')
    get number_of_lattice_vectors(): number {
        // Deprecated getter for number_of_lattice_vectors
        return this.cell.rank;
    }

    set_constraint(constraint: any = null): void {
        // Setter for constraint
        if (constraint === null) {
            this._constraints = [];
        } else if (Array.isArray(constraint)) {
            this._constraints = [...constraint];
        } else {
            this._constraints = [constraint];
        }
    }

    private _constraints: any[] = [];

    get constraints(): any[] {
        // Getter for constraints
        return this._constraints;
    }

    get_number_of_degrees_of_freedom(): number {
        // Method to calculate number of degrees of freedom
        return Object.keys(this).length * 3 - this._constraints.reduce((sum, c) => sum + c.get_removed_dof(this), 0);
    }

    set_cell(cell: number[][], scale_atoms: boolean = false, apply_constraint: boolean = true): void {
        // Method to set cell
        const newCell = Cell.new(cell);

        if (apply_constraint && this._constraints) {
            for (const constraint of this._constraints) {
                if (constraint.adjust_cell) {
                    constraint.adjust_cell(this, newCell);
                }
            }
        }

        if (scale_atoms) {
            const M = math.lusolve(this.cell.complete(), newCell.complete());
            this.positions = math.multiply(this.positions, M);
        }

        this.cell = newCell;
    }

    set_celldisp(celldisp: number[]): void {
        // Method to set celldisp
        this._celldisp = [...celldisp];
    }

    get celldisp(): number[] {
        // Getter for celldisp
        return [...this._celldisp];
    }

    get_cell(complete: boolean = false): number[][] {
        // Method to get cell
        const cell = complete ? this.cell.complete() : this.cell.copy();
        return cell;
    }

    @deprecated('Please use atoms.cell.cellpar() instead')
    get_cell_lengths_and_angles(): number[] {
        // Deprecated method to get cell lengths and angles
        return this.cell.cellpar();
    }

    @deprecated('Please use atoms.cell.reciprocal()')
    get_reciprocal_cell(): number[][] {
        // Deprecated method to get reciprocal cell
        return this.cell.reciprocal();
    }

    private _pbc: boolean[];

    get pbc(): boolean[] {
        // Getter for pbc
        return [...this._pbc];
    }

    set pbc(pbc: boolean[]) {
        // Setter for pbc
        this._pbc = [...pbc];
    }

    set_pbc(pbc: boolean[]): void {
        // Method to set pbc
        this.pbc = [...pbc];
    }

    get_pbc(): boolean[] {
        // Method to get pbc
        return [...this.pbc];
    }

    new_array(name: string, a: any[], dtype?: string, shape?: number[]): void {
        // Method to add new array
        if (!dtype) {
            a = new Array(a).ascontiguousarray(a);
        } else {
            a = a.slice();
        }

        if (this.arrays[name]) {
            throw new Error(`Array ${name} already present`);
        }

        for (const b of Object.values(this.arrays)) {
            if (a.length !== b.length) {
                throw new Error(`Array "${name}" has wrong length: ${a.length} != ${b.length}.`);
            }
        }

        if (shape && a.slice(1) !== shape) {
            throw new Error(`Array "${name}" has wrong shape ${a.slice(0)} != ${a.slice(0, 1) + shape}.`);
        }

        this.arrays[name] = a;
    }
}
