import { createContext, useCallback, useContext, useRef } from 'react';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { useMaterial3DCore } from './core';
import { BehaviorSubject, Subject } from 'rxjs';
import { SimpleMaterialCore } from '../core';

interface HistoryRecord {
    core: SimpleMaterialCore;
    snapshot: any;
}

const defaultProperty = {
    length: 0,
    current: -1,
};

const useContextValue = () => {
    const { lightPluginRef, coreHistoryChangeSubjectRef, coreRef, render } = useMaterial3DCore();
    const historyStackRef = useRef<HistoryRecord[]>([]);
    const historyPropertySubjectRef = useRef(new BehaviorSubject(defaultProperty));

    const record = useCallback(async () => {
        const core = coreRef.current?.getSimple();
        const snapshot = await lightPluginRef.current?.managers.snapshot.getSnapshot();
        if (!core || !snapshot) {
            return;
        }
        const property = historyPropertySubjectRef.current.value;
        const current = property.current + 1;
        historyStackRef.current[current] = {
            core,
            snapshot,
        };
        historyPropertySubjectRef.current.next({
            current,
            length: current + 1,
        });
    }, []);

    const startRecording = useCallback(() => {
        const subscription = coreHistoryChangeSubjectRef.current.subscribe(() => {
            record();
        });

        return function stop() {
            subscription.unsubscribe();
        };
    }, []);

    const clearHistory = useCallback(() => {
        historyStackRef.current = [];
        historyPropertySubjectRef.current.next(defaultProperty);
    }, []);

    const goto = useCallback(async (index: number) => {
        const record = historyStackRef.current[index];
        if (!record) {
            return;
        }
        const property = historyPropertySubjectRef.current.value;
        historyPropertySubjectRef.current.next({
            ...property,
            current: index,
        });
        await lightPluginRef.current?.managers.snapshot.setSnapshot(record.snapshot);
        render(record.core.toMaterialCore(), {
            changeHistory: false,
        });
    }, []);

    const prev = useCallback(() => {
        const property = historyPropertySubjectRef.current.value;
        goto(property.current - 1);
    }, []);

    const next = useCallback(() => {
        const property = historyPropertySubjectRef.current.value;
        goto(property.current + 1);
    }, []);

    return {
        historyPropertySubjectRef,
        startRecording,
        clearHistory,
        goto,
        prev,
        next,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DHistoryProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DHistory = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DHistoryProvider');
    }
    return context;
};
