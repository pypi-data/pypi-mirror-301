import { reshape, sort, multiply, inv } from 'mathjs';
// import { Atoms } from 'ase.atoms';
// import { convert } from 'ase.calculators.lammps';
// import { SinglePointCalculator } from 'ase.calculators.singlepoint';
// import { Quaternions } from 'ase.quaternions';
import { convert } from '../calculators/lammps/unitconvert';
// import { PeriodicTable } from '../../periodic-table';

function Atoms(params: {
    symbols: string[];
    positions?: number[];
    scaled_positions?: number[];
    pbc: boolean;
    celldisp: number[];
    cell: number[][];
}) {
    const { symbols, positions, scaled_positions, cell } = params;
    if (!positions && !scaled_positions) {
        throw new Error('lammpsrun: can not find positions. ');
    }

    const cart_coords = positions || multiply(scaled_positions!, cell);
    const frac_coords = scaled_positions || multiply(positions!, inv(cell));

    return symbols.map((symbol, idx) => {
        return {
            id: 0,
            formula: typeof symbol === 'number' ? `Type ${symbol}` : symbol,
            cart_coord: cart_coords[idx],
            frac_coord: frac_coords[idx],
        };
    });
}

function lammpsDataToAseAtoms(
    data: any,
    colnames: string[],
    cell: any,
    celldisp: any,
    pbc: boolean = false,
    atomsobj: any = Atoms,
    order: boolean = true,
    // specorder: string[] | null = null,
    // prismobj: any = null,
    units: string = 'metal'
) {
    if (data.length === 1) {
        data = reshape(data, [1, data.length]);
    }

    // Read IDs if given and order if needed
    // if (colnames.includes('id')) {
    //     const ids = data.map((row: any) => parseInt(row[colnames.indexOf('id')]));
    //     if (order) {
    //         const sortOrder = sort(ids, 'asc');
    //         // data = data[sortOrder];
    //         data = sortOrder;
    //     }
    // }

    // Determine the elements
    let elements;
    if (colnames.includes('element')) {
        elements = data.map((row: any) => row[colnames.indexOf('element')]);
    } else if (colnames.includes('type')) {
        elements = data.map((row: any) => parseInt(row[colnames.indexOf('type')]));
        // if (specorder) {
        //     elements = elements.map((t: any) => specorder[t - 1]);
        // }
    } else {
        throw new Error('Cannot determine atom types from LAMMPS dump file');
    }

    const getQuantity = (labels: string[], quantity: string | null = null) => {
        try {
            const cols = labels.map(label => colnames.indexOf(label));
            if (quantity) {
                return convert(
                    data.map((row: any) => cols.map(col => parseFloat(row[col]))),
                    quantity,
                    units,
                    'ASE'
                );
            }
            return data.map((row: any) => cols.map(col => parseFloat(row[col])));
        } catch (e) {
            return null;
        }
    };

    // Positions
    let positions = null;
    let scaledPositions = null;
    if (colnames.includes('x')) {
        positions = getQuantity(['x', 'y', 'z'], 'distance');
    } else if (colnames.includes('xs')) {
        scaledPositions = getQuantity(['xs', 'ys', 'zs']);
    } else if (colnames.includes('xu')) {
        positions = getQuantity(['xu', 'yu', 'zu'], 'distance');
    } else if (colnames.includes('xsu')) {
        scaledPositions = getQuantity(['xsu', 'ysu', 'zsu']);
    } else {
        throw new Error('No atomic positions found in LAMMPS output');
    }

    // const velocities = getQuantity(['vx', 'vy', 'vz'], 'velocity');
    // const charges = getQuantity(['q'], 'charge');
    // const forces = getQuantity(['fx', 'fy', 'fz'], 'force');
    // const quaternions = getQuantity(['c_q[1]', 'c_q[2]', 'c_q[3]', 'c_q[4]']);

    // Convert cell
    cell = convert(cell, 'distance', units, 'ASE');
    celldisp = convert(celldisp, 'distance', units, 'ASE');
    // if (prismobj) {
    //     celldisp = prismobj.vectorToAse(celldisp);
    //     cell = prismobj.updateCell(cell);
    // }

    let outAtoms;
    // if (quaternions) {
    //     outAtoms = new Quaternions({
    //         symbols: elements,
    //         positions: positions,
    //         cell: cell,
    //         celldisp: celldisp,
    //         pbc: pbc,
    //         quaternions: quaternions,
    //     });
    // } else
    if (positions) {
        // if (prismobj) {
        //     positions = prismobj.vectorToAse(positions, true);
        // }
        outAtoms = new atomsobj({
            symbols: elements,
            positions: positions,
            pbc: pbc,
            celldisp: celldisp,
            cell: cell,
        });
    } else if (scaledPositions) {
        outAtoms = new atomsobj({
            symbols: elements,
            scaled_positions: scaledPositions,
            pbc: pbc,
            celldisp: celldisp,
            cell: cell,
        });
    }

    // if (velocities) {
    //     if (prismobj) {
    //         velocities = prismobj.vectorToAse(velocities);
    //     }
    //     outAtoms.setVelocities(velocities);
    // }
    // if (charges) {
    //     outAtoms.setInitialCharges(charges.map((charge: any) => charge[0]));
    // }
    // if (forces) {
    //     if (prismobj) {
    //         forces = prismobj.vectorToAse(forces);
    //     }
    //     const calculator = new SinglePointCalculator(outAtoms, 0.0, forces);
    //     outAtoms.calc = calculator;
    // }

    // colnames.forEach(colname => {
    //     if (
    //         (colname.startsWith('f_') || colname.startsWith('v_') || colname.startsWith('c_')) &&
    //         !colname.startsWith('c_q[')
    //     ) {
    //         outAtoms.newArray(colname, getQuantity([colname]), 'float');
    //     }
    // });

    return outAtoms;
}

function constructCell(diagdisp: any, offdiag: any) {
    const [xlo, xhi, ylo, yhi, zlo, zhi] = diagdisp;
    const [xy, xz, yz] = offdiag;

    const xhilo = xhi - xlo - Math.abs(xy) - Math.abs(xz);
    const yhilo = yhi - ylo - Math.abs(yz);
    const zhilo = zhi - zlo;
    const celldispx = xlo - Math.min(0, xy) - Math.min(0, xz);
    const celldispy = ylo - Math.min(0, yz);
    const celldispz = zlo;
    const cell = [
        [xhilo, 0, 0],
        [xy, yhilo, 0],
        [xz, yz, zhilo],
    ];
    const celldisp = [celldispx, celldispy, celldispz];

    return [cell, celldisp];
}

const SpaceReg = /\s+/g;

export function readLammpsDumpText(fileStr: string, indexEnd = -1): any[] {
    // Load all dumped timesteps into memory simultaneously
    // const lines: Deque<string> = new Deque(readFileSync(fileobj, 'utf-8').split('\n'));
    const lines = fileStr.split('\n');

    let nAtoms = 0;

    let images: any[] = [];

    // avoid references before assignment in case of incorrect file structure
    let cell: any = null,
        celldisp: any = null,
        pbc = [null, null, false];

    while (lines.length > nAtoms) {
        let line: string = lines.shift()!;

        if (line.includes('ITEM: TIMESTEP')) {
            nAtoms = 0;
            line = lines.shift()!;
            // !TODO: pyflakes complains about this line -> do something
            // const ntimestep: number = parseInt(line.split()[0]); // NOQA
        }

        if (line.includes('ITEM: NUMBER OF ATOMS')) {
            line = lines.shift()!;
            nAtoms = parseInt(line.split(SpaceReg)[0]);
        }

        if (line.includes('ITEM: BOX BOUNDS')) {
            // save labels behind "ITEM: BOX BOUNDS" in triclinic case
            // (>=lammps-7Jul09)
            const tilt_items: string[] = line.split(SpaceReg).slice(3);
            const celldatarows: string[] = [];
            for (let i = 0; i < 3; i++) {
                celldatarows.push(lines.shift()!);
            }
            const celldata: number[][] = celldatarows.map(row => row.split(SpaceReg).map(Number));

            const diagdisp: number[] = celldata.map(row => row.slice(0, 2)).flat();

            // determine cell tilt (triclinic case!)
            let offdiag: number[];
            if (celldata[0].length > 2) {
                // for >=lammps-7Jul09 use labels behind "ITEM: BOX BOUNDS"
                // to assign tilt (vector) elements ...
                let sort_index: number[] = [];
                ['xy', 'xz', 'yz'].forEach(label => {
                    sort_index.push(tilt_items.indexOf(label));
                });
                offdiag = sort_index.map(idx => celldata[idx][2]);
            } else {
                offdiag = [0.0, 0.0, 0.0];
            }

            [cell, celldisp] = constructCell(diagdisp, offdiag); // Assuming construct_cell function is defined

            // Handle pbc conditions
            let pbc_items: string[];
            if (tilt_items.length === 3) {
                pbc_items = tilt_items;
            } else if (tilt_items.length > 3) {
                pbc_items = tilt_items.slice(3, 6);
            } else {
                pbc_items = ['f', 'f', 'f'];
            }
            pbc = pbc_items.map(d => d.toLowerCase().includes('p'));
        }

        if (line.includes('ITEM: ATOMS')) {
            const colnames = line.split(SpaceReg).slice(2);
            const datarows = [];
            for (let i = 0; i < nAtoms; i++) {
                datarows.push(lines.shift());
            }
            const data = datarows.map(row => row?.split(SpaceReg)!);

            const outAtoms = lammpsDataToAseAtoms(data, colnames, cell, celldisp, Boolean(pbc[0]), Atoms);
            // const outAtoms = 0;
            images.push({
                atoms: outAtoms,
                matrix: cell,
            });
        }
    }

    return images;
}
