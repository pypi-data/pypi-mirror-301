import { useCallback } from 'react';
import { RepresentationType } from 'dpmol';
import { useMaterial3DCore } from '../context/core';
import { MeasureType } from '../model';

const MeasureReprTypeMap = {
    [MeasureType.Distance]: RepresentationType.Distance,
    [MeasureType.Angle]: RepresentationType.Angle,
    [MeasureType.Dihedral]: RepresentationType.Dihedral,
};

const MeasureCountMap = {
    [MeasureType.Distance]: 2,
    [MeasureType.Angle]: 3,
    [MeasureType.Dihedral]: 4,
};

export function useMeasureMode() {
    const { lightPluginRef } = useMaterial3DCore();

    const enterMeasureMode = useCallback((type: MeasureType) => {
        lightPluginRef.current?.managers.events.setAllowSelect(true);
        const reprType = MeasureReprTypeMap[type];
        const count = MeasureCountMap[type];
        const subscription = lightPluginRef.current?.managers.selection.event.changed.subscribe(async () => {
            const prev = lightPluginRef.current?.managers.selection.structure.prev!;

            if (prev.length === count) {
                await lightPluginRef.current?.managers.representation.createMeasurement({
                    items: prev,
                    type: reprType,
                });
                lightPluginRef.current?.managers.selection.clear();
            }
        });
        return function exitMeasureMode() {
            lightPluginRef.current?.managers.events.setAllowSelect(false);
            subscription?.unsubscribe();
        };
    }, []);

    return {
        enterMeasureMode,
    };
}
