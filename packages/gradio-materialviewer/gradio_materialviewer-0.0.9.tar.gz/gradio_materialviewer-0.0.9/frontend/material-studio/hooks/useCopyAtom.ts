import { useCallback, useRef } from 'react';
import KeyboardJS, { KeyEvent } from 'keyboardjs';
import { copyText } from '@utils/string';
import { useMaterial3DCore, useMaterial3DMode } from '../context';
import { addMaterialAtoms, delMaterialAtoms, isMac } from '../utils/utils';
import { Atom } from '../model';

const ctrlKey = isMac ? 'command' : 'ctrl';

function atoms2text(atoms: Atom[]) {
    return JSON.stringify({
        atoms: atoms.map(item => ({
            element: item.element,
            xyz: item.xyz,
        })),
    });
}

export function useCopyAtom() {
    const { coreRef, lightPluginRef, uuidRef, render } = useMaterial3DCore();
    const { selectedAtomsSubjectRef } = useMaterial3DMode();

    const ctrlCEvent = useCallback((ev?: KeyEvent) => {
        const selected = selectedAtomsSubjectRef.current.value;
        if (!selected.length) {
            return;
        }
        copyText(atoms2text(selected));
    }, []);

    const ctrlXEvent = useCallback(() => {
        const selected = selectedAtomsSubjectRef.current.value;
        if (!selected.length) {
            return;
        }

        const core = coreRef.current;
        const origin = core?.origin;
        if (!core || !origin) {
            return;
        }
        const selectedIds = selected.map(atom => atom.order!);
        core.setByOriginMaterial(delMaterialAtoms(origin, selectedIds));
        render(core);
        copyText(atoms2text(selected));
    }, []);

    const ctrlVDown = useCallback(async (ev?: KeyEvent) => {
        const text = await navigator.clipboard.readText();
        try {
            const json = JSON.parse(text);
            if (Array.isArray(json?.atoms)) {
                const params = json?.atoms?.filter((p: Atom) => {
                    if (typeof p.element !== 'string') {
                        return false;
                    }
                    if (!p.xyz || !Array.isArray(p.xyz) || p.xyz.length < 3) {
                        return false;
                    }
                    return p.xyz.every(n => typeof n === 'number');
                }) as Atom[];
                if (!params.length) {
                    return;
                }
                const core = coreRef.current;
                const origin = core?.origin;
                if (!core || !origin) {
                    return;
                }
                const elementIds: number[] = [];
                const start = origin.atoms.length;
                params.forEach((p, i) => {
                    elementIds.push(start + i);
                });
                core.setByOriginMaterial(addMaterialAtoms(origin, params));
                await render(core);
                lightPluginRef.current?.managers.selection.structure.add(
                    {
                        item: {
                            ref: uuidRef.current,
                            elementIds,
                        },
                    },
                    false
                );
            }
        } catch (e) {}
    }, []);

    const bindCopyEvent = useCallback(() => {
        KeyboardJS.bind(`${ctrlKey} + c`, ctrlCEvent);
        KeyboardJS.bind(`${ctrlKey} + x`, ctrlXEvent);
        KeyboardJS.bind(`${ctrlKey} + v`, ctrlVDown);

        return function unbind() {
            KeyboardJS.unbind(`${ctrlKey} + c`, ctrlCEvent);
            KeyboardJS.unbind(`${ctrlKey} + x`, ctrlXEvent);
            KeyboardJS.unbind(`${ctrlKey} + v`, ctrlVDown);
        };
    }, []);

    return {
        bindCopyEvent,
    };
}
