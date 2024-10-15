import { useCallback } from 'react';
import { Vec3 } from 'dpmol';
import { useMaterial3DCore } from '../context/core';
import { createAtom, getElementLociInfo } from '../utils/utils';

export function useCreateAtomMode() {
    const { lightPluginRef, coreRef, render } = useMaterial3DCore();

    const enterCreateAtomMode = useCallback((element: string) => {
        const subscription = lightPluginRef.current?.canvas3d?.interaction.click.subscribe(ev => {
            if (!ev || !ev.page || !ev.current) {
                return;
            }
            const pos = lightPluginRef.current!.canvas3d?.getPosition(ev.page[0], ev.page[1]);
            if (!pos?.position) {
                return;
            }
            const { loci } = ev.current;
            if (loci.kind !== 'element-loci') {
                return addAtom(element, pos.position);
            }

            // TODO: position = selected.r + bond(selected => el)
            const info = getElementLociInfo(loci);
            if (!info) {
                return;
            }
            const offsetConstant = 0.5;
            const offset = {
                x: offsetConstant,
                y: offsetConstant,
                z: offsetConstant,
            };
            const position = Vec3.create(info.x + offset.x, info.y + offset.y, info.z + offset.z);
            addAtom(element, position);
        });
        return function exitCreateAtomMode() {
            subscription?.unsubscribe();
        };
    }, []);

    const addAtom = useCallback((element: string, xyz: Vec3) => {
        if (!coreRef.current?.origin) {
            return;
        }
        const { origin } = coreRef.current;
        const atom = createAtom(
            {
                element,
                xyz,
            },
            {
                order: origin.atoms.length,
            }
        );
        origin.atoms.push(atom);
        coreRef.current.setByOriginMaterial(origin);
        render(coreRef.current);
    }, []);

    return {
        enterCreateAtomMode,
    };
}
