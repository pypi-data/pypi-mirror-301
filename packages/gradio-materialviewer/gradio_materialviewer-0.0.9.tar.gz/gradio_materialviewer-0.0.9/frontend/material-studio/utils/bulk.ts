import { MathArray, add, clone, concat, inv, multiply } from 'mathjs';
import _ from 'lodash';

export class Bulk {
    private cell: number[][] = [];
    private symbols: string[] = [];
    private fractionalCoordinates: MathArray | undefined;
    private coordinates: number[][] = [];
    private pbc: [boolean, boolean, boolean] = [true, true, true];
    private invCell: number[][] = [];

    constructor(
        cell: number[][],
        symbols: string[],
        coordinates: number[][],
        fractionalCoordinates: MathArray | undefined,
        pbc: [boolean, boolean, boolean] = [true, true, true]
    ) {
        if (cell.length != 3 || cell[0].length != 3 || cell[1].length != 3 || cell[2].length != 3) {
            throw new Error('The cell should be a 3x3 matrix.');
        }
        this.cell = cell;
        this._computeInverseCell();
        this.symbols = symbols;
        if (coordinates) {
            this.coordinates = coordinates;
        }
        if (fractionalCoordinates) {
            this.fractionalCoordinates = fractionalCoordinates;
        }
        this.pbc = pbc;
        if (this.coordinates.length != this.symbols.length) {
            throw new Error('The number of coordinates and symbols are not equal.');
        }
    }

    copy() {
        return new Bulk(this.cell, this.symbols, this.coordinates, this.fractionalCoordinates, this.pbc);
    }

    _computeInverseCell() {
        this.invCell = inv(this.cell);
    }

    getSymbols() {
        return this.symbols;
    }

    getFractionalCoordinates(): MathArray {
        // fractionalCoordinates * cell = coordinates
        // fractionalCoordinates = coordinates * inverse(cell)
        return multiply(this.coordinates, this.invCell);
    }
    setFractionalCoordinates(fractionalCoordinates: MathArray) {
        this.coordinates = multiply(fractionalCoordinates, this.cell).valueOf() as number[][];
    }

    getCoordinates(): number[][] {
        return this.coordinates;
    }
    setCoordinates(coordinates: number[][]) {
        this.coordinates = coordinates;
    }

    getCell(): number[][] {
        let cell = _.cloneDeep(this.cell);
        for (let i = 0; i < 3; i++) {
            if (!this.pbc[i]) {
                cell[i] = [0, 0, 0];
            }
        }
        return cell;
    }
    setCell(cell: number[][], move_atoms: boolean = false) {
        if (move_atoms) {
            const M = multiply(this.invCell, cell);
            this.coordinates = multiply(this.coordinates, M);
        }
        this.cell = cell;
        this._computeInverseCell();
    }

    setPBC(pbc: [boolean, boolean, boolean]) {
        this.pbc = pbc;
    }
    getPBC() {
        return this.pbc;
    }
    getInverseABC() {
        return this.invCell;
    }

    makeSuperCell(n: number, m: number, l: number) {
        // 在abc方向重复的次数
        this._repeatSingleAxis(n, 0);
        this._repeatSingleAxis(m, 1);
        this._repeatSingleAxis(l, 2);
    }

    _repeatSingleAxis(n: number, nAxis: number) {
        if (n < 2) return;
        let coordinates: MathArray = [];
        let symbols: string[] = [];
        let axisVec = this.cell[nAxis];

        for (let i = 2; i <= n; i++) {
            const _vec = multiply(i - 1, axisVec);
            let newCoordinates = add(this.coordinates, _vec).valueOf() as number[][];
            if (coordinates.length == 0) {
                coordinates = clone(newCoordinates);
            } else {
                coordinates = concat(coordinates, newCoordinates, 0) as MathArray;
            }
            symbols = symbols.concat(this.symbols);
        }
        this.coordinates = concat(this.coordinates, coordinates, 0).valueOf() as number[][];
        this.symbols = this.symbols.concat(symbols);
        this.cell[nAxis] = multiply(n, axisVec).valueOf() as number[];
    }
}
