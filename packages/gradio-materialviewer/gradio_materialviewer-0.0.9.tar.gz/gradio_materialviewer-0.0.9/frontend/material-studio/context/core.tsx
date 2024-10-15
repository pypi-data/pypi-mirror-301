import { LightPlugin, Format, RepresentationType, ThemeC, Granularity, MoleculeInfoParam } from 'dpmol';
import { Vec3 } from 'dpmol';
import { createContext, useCallback, useContext, useEffect, useRef } from 'react';
import { debounce } from 'lodash';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { OuterPromise, sleep } from '@@shared/utils/async';
import { MaterialCore } from '../core';
import { getPointsByVertex, getTypeColor, getVertexByVectors } from '../utils/utils';
import { Bulk } from '../utils/bulk';
import { ASEDataItem, Lattice } from '../model';
import { BehaviorSubject, Subject } from 'rxjs';

const useContextValue = () => {
    // core
    const lightPluginRef = useRef<LightPlugin>();
    const initPluginPromiseRef = useRef(OuterPromise<LightPlugin>());
    const coreRef = useRef<MaterialCore | null>();
    const uuidRef = useRef('');
    const dataSubjectRef = useRef(new BehaviorSubject<ASEDataItem[]>([]));
    const formatSubjectRef = useRef(new BehaviorSubject(''));

    // style
    const pluginRefreshSubjectRef = useRef(new Subject<void>());
    const reprTypeRef = useRef(RepresentationType.BallAndStick);
    const extraColorTableRef = useRef<{ [k: string]: number }>({});

    // subject
    const coreChangeSubjectRef = useRef(new Subject<MaterialCore | undefined>());
    const coreFileChangeSubjectRef = useRef(new Subject<MaterialCore | undefined>());
    const coreHistoryChangeSubjectRef = useRef(new Subject<MaterialCore | undefined>());

    // traj
    const isTrajSubjectRef = useRef(new BehaviorSubject(false));

    const initPlugin = useCallback((dom: HTMLElement) => {
        lightPluginRef.current = new LightPlugin();
        lightPluginRef.current.createCanvas(dom);
        lightPluginRef.current.managers.representation.showPolarHydrogenOnly = false;
        lightPluginRef.current.managers.selection.structure.setGranularity(Granularity.Atom);
        lightPluginRef.current.managers.editor.isLockCamera = true;

        Promise.resolve().then(() => {
            initPluginPromiseRef.current.outerResolve(lightPluginRef.current!);
        });

        const observer = new ResizeObserver(
            debounce(() => {
                lightPluginRef.current?.refresh({ fixCamera: true });
                pluginRefreshSubjectRef.current.next();
            }, 300)
        );
        observer.observe(dom);

        return function dispose() {
            observer.disconnect();
            lightPluginRef.current?.dispose?.();
        };
    }, []);

    const renderAtoms = useCallback(async (data: MoleculeInfoParam) => {
        const types = Array.from(new Set(data.elements)).filter(symbol => symbol.startsWith(`Type`));
        extraColorTableRef.current = {};
        types.forEach(type => {
            extraColorTableRef.current[type.toUpperCase()] = getTypeColor(Number(type.split(' ')?.[1]));
        });

        const [ref] = await lightPluginRef.current!.managers.representation.createMolecular({
            format: Format.Material,
            data,
            reprType: reprTypeRef.current,
            theme: {
                [ThemeC.ATOM]: {
                    color: {
                        name: 'material-element-symbol',
                        props: {
                            extraColorTable: extraColorTableRef.current,
                        },
                    },
                },
                // extraColorTable,
            },
            // 有多个frame的情况下自动变成trajectory而不是拆成多个structure
            // autoConvertToTrajectory: true,
        });

        uuidRef.current = ref;
        return ref;
    }, []);

    const renderCell = useCallback(async (lattice?: Lattice, surface?: Bulk) => {
        if (!lattice) {
            return;
        }

        if (!surface) {
            const vertex = getVertexByVectors(lattice.matrix!);
            const points = getPointsByVertex(vertex);

            return lightPluginRef.current!.managers.representation.createOther({
                data: points,
                type: RepresentationType.CustomLines,
                params: {
                    alpha: 1,
                },
            });
        }

        const vertex = getVertexByVectors(surface.getCell());
        const points = getPointsByVertex(vertex);
        const solidPoints = points.slice(0, 4);

        return lightPluginRef.current!.managers.representation.createOther({
            data: solidPoints,
            type: RepresentationType.CustomLines,
            params: {
                alpha: 1,
            },
        });
    }, []);

    const setAxes = useCallback((lattice?: Lattice, surface?: Bulk) => {
        const defaultParams = {
            vecA: Vec3.unitX,
            vecB: Vec3.unitY,
            vecC: Vec3.unitZ,
        };

        const params = (() => {
            if (!lattice) {
                return {};
            }
            const cell = surface?.getCell() || lattice.matrix;
            return {
                vecA: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[0] as [number, number, number])),
                vecB: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[1] as [number, number, number])),
                vecC: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[2] as [number, number, number])),
            };
        })();

        return lightPluginRef?.current?.canvas3d?.setProps({
            camera: {
                helper: {
                    axes: {
                        name: 'on',
                        params: {
                            ...defaultParams,
                            ...params,
                        },
                    },
                },
            },
        });
    }, []);

    const render = useCallback(
        async (
            core = coreRef.current,
            params?: {
                changeCore?: boolean;
                changeFile?: boolean;
                changeHistory?: boolean;
                autoLockCamera?: boolean;
            }
        ) => {
            params = Object.assign(
                {
                    changeCore: true,
                    changeFile: true,
                    changeHistory: true,
                    autoLockCamera: true,
                },
                params
            );
            await lightPluginRef.current!.clear();
            if (!core || !core.origin) {
                if (params.changeCore) {
                    coreChangeSubjectRef.current.next(core!);
                }
                return;
            }
            coreRef.current = core;
            const moleculeParam = core.getMoleculeParam();
            const lattice = core.origin.lattice;
            if (params.autoLockCamera) {
                lightPluginRef.current!.managers.editor.isLockCamera = true;
            }
            await renderAtoms(moleculeParam!);
            await renderCell(lattice, core.surface);
            await setAxes(lattice, core.surface);
            if (params.autoLockCamera) {
                await sleep(0);
                lightPluginRef.current!.managers.editor.isLockCamera = false;
            }
            if (params.changeCore) {
                coreChangeSubjectRef.current.next(core);
            }
            if (params.changeFile) {
                coreFileChangeSubjectRef.current.next(core);
            }
            if (params.changeHistory) {
                coreHistoryChangeSubjectRef.current.next(core);
            }
        },
        []
    );

    return {
        lightPluginRef,
        initPluginPromiseRef,
        uuidRef,
        coreRef,
        dataSubjectRef,
        formatSubjectRef,
        pluginRefreshSubjectRef,
        reprTypeRef,
        extraColorTableRef,
        coreChangeSubjectRef,
        coreFileChangeSubjectRef,
        coreHistoryChangeSubjectRef,
        isTrajSubjectRef,
        initPlugin,
        render,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DCoreProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DCore = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DCoreProvider');
    }
    return context;
};
