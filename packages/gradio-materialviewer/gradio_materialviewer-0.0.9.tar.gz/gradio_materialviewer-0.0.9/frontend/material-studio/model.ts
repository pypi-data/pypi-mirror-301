export type MaterialFormat = 'cif' | 'dump' | 'xyz' | 'POSCAR' | 'mol' | 'mol2' | 'sdf';

export enum MaterialMode {
    CreateAtom,
    Selection,
    Measure,
}

export enum MeasureType {
    Distance = 'Distance',
    Angle = 'Angle',
    Dihedral = 'Dihedral',
}

export interface SpaceGroup {
    symbol: string;
    no: number;
}

export interface LatticeValue {
    a: number;
    b: number;
    c: number;
    alpha: number;
    beta: number;
    gamma: number;
}

export interface LatticeParams extends LatticeValue {
    matrix?: number[][];
    spacegroup: SpaceGroup;
}

export interface AtomParams {
    element: string;
    xyz?: number[];
    abc?: number[];
}

export interface Lattice extends LatticeParams {
    vecA: number[];
    vecB: number[];
    vecC: number[];
    // center: number[]
    matrix: number[][];
    invertMatrix: number[][];
    volume: number;
}

export interface Atom {
    order?: number;
    symmetry?: number[];
    element: string;
    xyz: number[];
    abc?: number[];
}

export interface MaterialItem {
    expand: number[];
    atoms: Atom[];
    lattice?: Lattice;
}

export interface ASEAtom {
    cart_coord: number[];
    formula: string;
    frac_coord: number[];
    id: number;
}

export interface ASEDataItem {
    atoms: ASEAtom[];
    angle?: number[];
    length?: number[];
    matrix?: number[][];
    spacegroup?: [number, string];
}

export interface MaterialCleaveParams {
    h: number;
    k: number;
    l: number;
    depth: number;
}

export interface MaterialCleave extends MaterialCleaveParams {
    depth: number;
}

export interface MaterialAxesParams {
    hideX?: boolean;
    hideY?: boolean;
    hideZ?: boolean;
    vecA?: number[];
    vecB?: number[];
    vecC?: number[];
    labelX?: string;
    labelY?: string;
    labelZ?: string;
}

export interface Ligand {
    element: string;
    color: string;
}
