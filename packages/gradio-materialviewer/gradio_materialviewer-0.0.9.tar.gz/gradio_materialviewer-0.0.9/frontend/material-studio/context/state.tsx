import { createContext, useCallback, useContext } from 'react';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { useMaterial3DCore } from './core';
import { getElementColor } from '../utils/utils';
import { Ligand } from '../model';

const useContextValue = () => {
    const { lightPluginRef, coreRef, extraColorTableRef } = useMaterial3DCore();

    const getLigands = useCallback(async (biology = false) => {
        const elements = new Set<string>();
        const ligands: Array<Ligand> = [];
        coreRef.current?.origin?.atoms.forEach(atom => {
            elements.add(atom.element);
        });
        elements.forEach(element => {
            ligands.push({
                element,
                color: getElementColor(element, {
                    biology,
                    extraColorTable: extraColorTableRef.current,
                }),
            });
        });
        return ligands;
    }, []);

    const getLattice = useCallback(() => {
        const lattice = coreRef.current?.origin?.lattice;
        if (!lattice) {
            return;
        }
        return lattice;
    }, []);

    const getCameraState = useCallback(() => {
        return lightPluginRef?.current?.canvas3d?.camera?.state;
    }, []);

    const setCameraMode = useCallback((mode: 'perspective' | 'orthographic') => {
        return lightPluginRef?.current?.canvas3d?.setProps({
            camera: {
                mode,
            },
        });
    }, []);

    return {
        getLigands,
        getCameraState,
        setCameraMode,
        getLattice,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DStateProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DState = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DStateProvider');
    }
    return context;
};
