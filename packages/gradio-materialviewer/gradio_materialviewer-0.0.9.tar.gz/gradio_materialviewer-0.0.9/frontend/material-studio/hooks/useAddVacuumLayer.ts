import { useCallback } from 'react';
import { multiply } from 'mathjs';
import { useMaterial3DCore } from '../context';
import { MaterialCore } from '../core';
import { MaterialItem } from '../model';
import { cellToCellpar } from '../utils/cell';
import { createLatticeByParams, createAtom } from '../utils/utils';

export function useAddVacuumLayer() {
    const { coreRef, render } = useMaterial3DCore();

    const addVacuumLayer = useCallback((values: { c: number }) => {
        const origin = coreRef.current?.origin;
        if (!origin || !origin.lattice) {
            return;
        }
        const { matrix: prevMatrix, spacegroup } = origin.lattice;
        const vecZ = prevMatrix[2];
        const matrix = [prevMatrix[0], prevMatrix[1], [vecZ[0], vecZ[1], vecZ[2] + values.c]];
        const cellpar = cellToCellpar(matrix);
        const [a, b, c, alpha, beta, gamma] = cellpar;
        const lattice = createLatticeByParams({
            a,
            b,
            c,
            alpha,
            beta,
            gamma,
            matrix,
            spacegroup,
        });
        const atoms = origin.atoms.map(atom => {
            return createAtom({
                ...atom,
                abc: multiply(atom.xyz, lattice.invertMatrix) as number[],
            });
        });
        const material: MaterialItem = {
            expand: [1, 1, 1],
            atoms,
            lattice,
        };
        const core = new MaterialCore();
        core.setByOriginMaterial(material);
        render(core);
    }, []);

    return {
        addVacuumLayer,
    };
}
