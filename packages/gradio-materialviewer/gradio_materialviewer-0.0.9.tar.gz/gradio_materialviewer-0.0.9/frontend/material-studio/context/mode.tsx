import { createContext, useCallback, useContext, useRef } from 'react';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { BehaviorSubject } from 'rxjs';
import { MaterialMode, MeasureType } from '../model';
import { useCreateAtomMode } from '../hooks/useCreateAtomMode';
import { useSelectionMode } from '../hooks/useSelectionMode';
import { useMeasureMode } from '../hooks/useMeasureMode';

const useContextValue = () => {
    const { enterSelectionMode, selectedAtomsSubjectRef } = useSelectionMode();
    const { enterCreateAtomMode } = useCreateAtomMode();
    const { enterMeasureMode } = useMeasureMode();

    const modeSubjectRef = useRef(new BehaviorSubject<MaterialMode | undefined>(undefined));
    const exitPrevModeRef = useRef<() => void>();

    const setMode = useCallback(
        (
            mode: MaterialMode,
            params?: {
                element?: string;
                measureType?: MeasureType;
            }
        ) => {
            exitPrevModeRef.current?.();

            switch (mode) {
                case MaterialMode.CreateAtom:
                    exitPrevModeRef.current = enterCreateAtomMode(params?.element!);
                    break;
                case MaterialMode.Selection:
                    exitPrevModeRef.current = enterSelectionMode();
                    break;
                case MaterialMode.Measure:
                    exitPrevModeRef.current = enterMeasureMode(params?.measureType!);
                    break;
            }

            modeSubjectRef.current.next(mode);
        },
        []
    );

    return {
        setMode,
        modeSubjectRef,
        selectedAtomsSubjectRef,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DModeProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DMode = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DModeProvider');
    }
    return context;
};
