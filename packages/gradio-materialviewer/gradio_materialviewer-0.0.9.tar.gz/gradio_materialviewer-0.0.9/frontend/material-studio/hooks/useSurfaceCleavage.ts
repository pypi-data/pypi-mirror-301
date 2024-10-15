import { useCallback, useRef } from 'react';
import { RepresentationType } from 'dpmol';
import { Color } from 'dpmol';
import { useMaterial3DCore } from '../context/core';
import { MaterialCleaveParams } from '../model';
import { getCleavageSurf, getPointsByVertex, getVertexByVectors } from '../utils/utils';
import { MaterialCore } from '../core';

export function useSurfaceCleavage() {
    const { lightPluginRef, coreRef, render } = useMaterial3DCore();

    const prevRefsRef = useRef<string[]>([]);

    const clearCleavageCell = useCallback(() => {
        return lightPluginRef.current?.managers.cell.remove(prevRefsRef.current.map(ref => ({ ref })));
    }, []);

    const render3DCleavageCell = useCallback(async (params: MaterialCleaveParams) => {
        const surf = getCleavageSurf(params, coreRef.current?.origin!);
        if (!surf) {
            return;
        }
        await clearCleavageCell();
        const cell = surf.getCell();
        const vertex = getVertexByVectors(cell);
        const points = getPointsByVertex(vertex);
        const solidPoints = points.slice(0, 4);
        const dashedPoints = points.slice(4);
        const ref1 = await lightPluginRef.current!.managers.representation.createOther({
            data: solidPoints,
            type: RepresentationType.CustomLines,
            params: {
                linesColor: Color(0x1677ff),
                alpha: 1,
            },
        });
        const ref2 = await lightPluginRef.current!.managers.representation.createOther({
            data: dashedPoints,
            type: RepresentationType.CustomLines,
            params: {
                linesColor: Color(0x1677ff),
                // alpha: 0.2,
                isDash: true,
                dashLength: 0.5,
            },
        });

        prevRefsRef.current = [ref1!, ref2!];
    }, []);

    const render2DCleavageCell = useCallback(async (params: MaterialCleaveParams, mark = true) => {
        if (!coreRef.current?.prevOrigin) {
            return;
        }
        await clearCleavageCell();
        const core = new MaterialCore();
        core.setByOriginMaterial(coreRef.current?.prevOrigin);
        coreRef.current = core;
        core.setCleave(params);
        render(core, {
            changeCore: false,
            changeFile: false,
            changeHistory: false,
        });
    }, []);

    const renderCleavageCell = useCallback(async (params: MaterialCleaveParams, mark = true) => {
        if (coreRef.current?.prevOrigin) {
            return render2DCleavageCell(params, mark);
        }
        return render3DCleavageCell(params);
    }, []);

    return {
        getCleavageSurf,
        renderCleavageCell,
        clearCleavageCell,
    };
}
