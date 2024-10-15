import { useCallback, useRef } from 'react';
import {
    MolecularReprType,
    ReprLabelToType,
    transformLociToElementLoci,
    Loci,
    getStructureUniqueId,
    getElementIdsByLoci,
    PickingId,
} from 'dpmol';
import { BehaviorSubject } from 'rxjs';
import KeyboardJS from 'keyboardjs';
import { isInside, simplifyPath } from '../utils/selection-canvas/path';
import { Point } from '../utils/selection-canvas/models/point';
import { Atom } from '../model';
import { useMaterial3DCore } from '../context';
import { delMaterialAtoms, isMac } from '../utils/utils';

export function useSelectionMode() {
    const { lightPluginRef, coreRef, isTrajSubjectRef, render } = useMaterial3DCore();

    const selectedAtomsSubjectRef = useRef(new BehaviorSubject<Array<Atom>>([]));
    const selectionCanvasRef = useRef<HTMLCanvasElement>();

    const enterSelectionMode = useCallback(() => {
        lightPluginRef.current?.managers.events.setAllowSelect(true);
        const subscription = lightPluginRef.current?.managers.selection.event.changed.subscribe(() => {
            const items = lightPluginRef.current?.managers.selection.structure.getSelectionCellItems();
            const ids = items?.[0]?.elementIds || [];
            const atoms = coreRef.current?.symmetry?.atoms;
            if (!atoms) {
                return;
            }
            const selected = atoms.filter((atom, idx) => ids.includes(idx));
            selectedAtomsSubjectRef.current.next(selected);
        });
        const unbind = bindQuickSelectEvent();

        return function exitSelectionMode() {
            selectedAtomsSubjectRef.current.next([]);
            unbind();
            removeSelectionCanvas();
            lightPluginRef.current?.managers.events.setAllowSelect(false);
            subscription?.unsubscribe();
        };
    }, []);

    const removeSelectionCanvas = useCallback(() => {
        // console.log(`removeSelectionCanvas`);
        if (!selectionCanvasRef.current) {
            return;
        }
        lightPluginRef.current?.layout?.root?.removeChild(selectionCanvasRef.current);
        selectionCanvasRef.current = undefined;
    }, []);

    const selectByPickingIds = useCallback((pickingIds: PickingId[]) => {
        const plugin = lightPluginRef.current;

        if (!plugin) {
            return;
        }
        const lociList: any[] = [];
        const structureSelection: Map<string, Set<number>> = new Map();
        pickingIds.forEach(pickingId => {
            const reprLoci = plugin!.canvas3d!.getLoci(pickingId);
            if (reprLoci.loci.kind === 'empty-loci') return;
            const reprType = ReprLabelToType[reprLoci.repr?.label ?? ''];
            if (!MolecularReprType.has(reprType)) {
                plugin.managers.selection.shape.event.change.next({
                    current: reprLoci,
                    button: 2,
                } as any);
            } else {
                const loci = transformLociToElementLoci(reprLoci.loci);
                if (loci) {
                    const elementLoci = transformLociToElementLoci(
                        Loci.normalize(loci, plugin.managers.selection.structure.lociGranularity, true)
                    ) as any;
                    const key = getStructureUniqueId(elementLoci.structure);
                    const elementIds = getElementIdsByLoci(elementLoci);
                    if (key && elementIds?.length) {
                        if (!structureSelection.has(key)) {
                            structureSelection.set(key, new Set([...elementIds]));
                        } else {
                            elementIds.forEach(elementId => {
                                structureSelection.get(key)?.add(elementId);
                            });
                        }
                    }
                    lociList.push(reprLoci);
                }
            }
        });
        plugin.cells.forEach((cell, ref) => {
            if (cell?.model.structure && structureSelection.has(getStructureUniqueId(cell?.model.structure))) {
                const key = getStructureUniqueId(cell?.model.structure);
                const elementIds = Array.from(structureSelection.get(key)?.values() ?? []);
                plugin.managers.selection.structure.add({
                    item: { ref, elementIds },
                });
            }
        });
    }, []);

    const appendSelectionCanvas = useCallback(() => {
        const plugin = lightPluginRef.current;
        const root = plugin?.layout?.root;
        // console.log(`appendSelectionCanvas`);

        if (!plugin || !root || selectionCanvasRef.current) {
            return;
        }
        let points: [number, number][] = [];
        const width = root.clientWidth;
        const height = root.clientHeight;
        const zoom = plugin.canvas3d?.camera.zoom!;
        const canvas = (selectionCanvasRef.current = document.createElement('canvas'));
        canvas.setAttribute(
            'style',
            `position: absolute; top: 0; left: 0; z-index: 100; -webkit-user-select: none; -webkit-tap-highlight-color: rgba(0,0,0,0); -webkit-touch-callout: none; touch-action: manipulation;`
        );
        canvas.setAttribute('width', String(width));
        canvas.setAttribute('height', String(height));
        const ctx = canvas.getContext('2d');
        canvas.addEventListener('mousedown', e => {
            const { offsetX: x, offsetY: y } = e;
            // console.log(x, y, 'mousedown');
            ctx!.beginPath();
            ctx!.moveTo(x, y);
            // ctx!.strokeStyle = 'yellow';
            ctx!.lineWidth = 2;
            points.push([x, y]);
            e.stopPropagation();
            e.stopImmediatePropagation();
        });
        canvas.addEventListener('mousemove', e => {
            if (!points.length) return;
            const { offsetX: x, offsetY: y } = e;
            // console.log(x, y, 'mousemove');
            const isExchangeX = points[0][0] > x;
            const isExchangeY = points[0][1] > y;
            ctx!.closePath();
            ctx!.clearRect(0, 0, ctx?.canvas.width!, ctx?.canvas.height!);
            ctx!.strokeRect(
                isExchangeX ? x : points[0][0],
                isExchangeY ? y : points[0][1],
                (x - points[0][0]) * (isExchangeX ? -1 : 1),
                (y - points[0][1]) * (isExchangeY ? -1 : 1)
            );
            points[1] = [x, y];
            // ctx!.lineTo(x, y);
            // ctx!.stroke();
            // points.push([x, y]);
            e.stopPropagation();
            e.stopImmediatePropagation();
        });
        canvas.addEventListener('mouseup', e => {
            removeSelectionCanvas();
            if (!(points[0]?.length >= 2) || !(points[1]?.length >= 2)) return;
            ctx!.stroke();
            ctx!.closePath();
            ctx!.clearRect(0, 0, width, height);
            // console.log(points.length, 'length');
            e.stopPropagation();
            e.stopImmediatePropagation();
            // XXX 直接使用第一个位置的节点算不出结构，所以偏移了1px
            const simple = simplifyPath(
                [
                    new Point(points[0][0], points[0][1]),
                    new Point(points[0][0], points[1][1]),
                    new Point(points[1][0], points[1][1]),
                    new Point(points[1][0], points[0][1]),
                    new Point(points[0][0] - 1, points[0][1] - 1),
                ],
                20
            );
            const start = { ...simple[0] };
            const rect = [start.x, start.y, start.x, start.y];

            simple.forEach((point: Point, index) => {
                if (index === 0) {
                    ctx!.moveTo(start.x, start.y);
                    ctx!.lineWidth = 2;
                } else {
                    ctx!.lineTo(point.x, point.y);
                }
                if (point.x < rect[0]) rect[0] = point.x;
                if (point.y < rect[1]) rect[1] = point.y;
                if (point.x > rect[2]) rect[2] = point.x;
                if (point.y > rect[3]) rect[3] = point.y;
            });

            const innerPoints: Point[] = [];
            const gap = Math.max(Math.floor(zoom / 15), 1);
            const pickingIdObj: { [key: string]: PickingId } = {};
            for (let x = rect[0]; x < rect[2]; x += gap) {
                for (let y = rect[1]; y < rect[3]; y += gap) {
                    // console.log(i, j);
                    if (isInside(simple, simple.length, new Point(x, y))) {
                        innerPoints.push(new Point(x, y));
                        // ctx!.fillStyle = 'green'
                        // ctx!.fillRect(i - 2, j - 2, 4, 4)
                        const pickingId = plugin!.canvas3d!.identify(x, y)?.id;
                        if (pickingId) {
                            const key = `${pickingId.objectId}-${pickingId.instanceId}-${pickingId.groupId}`;
                            if (!pickingIdObj[key]) {
                                pickingIdObj[key] = pickingId;
                            }
                        }
                    }
                }
            }
            selectByPickingIds(Object.values(pickingIdObj));
            points = [];
            // start.x = -1
            // start.y = -1
        });
        root.appendChild(canvas);
    }, []);

    const bindQuickSelectEvent = useCallback(() => {
        const ctrlKey = isMac ? 'command' : 'ctrl';
        const delKey = isMac ? 'backspace' : 'delete';
        const deleteAtom = () => {
            const selected = selectedAtomsSubjectRef.current.value;
            if (!selected.length || isTrajSubjectRef.current.value) {
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
        };
        KeyboardJS.bind(delKey, deleteAtom);
        KeyboardJS.bind(ctrlKey, appendSelectionCanvas, removeSelectionCanvas);

        return function unbind() {
            KeyboardJS.unbind(delKey, deleteAtom);
            KeyboardJS.unbind(ctrlKey, appendSelectionCanvas, removeSelectionCanvas);
        };
    }, []);

    return {
        enterSelectionMode,
        selectedAtomsSubjectRef,
    };
}
