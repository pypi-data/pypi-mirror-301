import { createContext, useCallback, useContext, useRef } from 'react';
import Cookies from 'js-cookie';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { useAppContext } from '@context';
import { getExtByName, getNameByPath } from '@@shared/model/workspace/node/util';
import { exportASE2CloudDiskReq, exportASE2FileReq, getASEByCloudDiskReq, getASEByFileReq } from '@@api';
import { downloadFileFromBlob } from '@@shared/utils/util';
import { APP_CONFIG } from '@config';
import { useMaterial3DCore } from './core';
import { MaterialCore } from '../core';
import { ASEDataItem, MaterialFormat } from '../model';
import { readLammpsDumpText } from '../utils/ase/io/lammpsrun';

// async function readFileText(file: File): Promise<string> {
//     return new Promise(resolve => {
//         const reader = new FileReader();
//         reader.onload = (ev: ProgressEvent<FileReader>) => {
//             const result = ev?.target?.result || '';
//             resolve(result as string);
//         };
//         reader.readAsText(file);
//     });
// }

const EmptyAseData = {
    atoms: [],
};

const useContextValue = () => {
    const { coreRef, render, isTrajSubjectRef, dataSubjectRef, formatSubjectRef, lightPluginRef } = useMaterial3DCore();
    const { userInfo } = useAppContext();

    const canISave = useCallback(() => {
        return !!coreRef.current?.origin?.atoms?.length;
    }, []);

    const setAndRenderData = useCallback(async (data: ASEDataItem[] = [], format: MaterialFormat) => {
        dataSubjectRef.current.next(data);
        isTrajSubjectRef.current.next(data.length > 1);
        const core = new MaterialCore();
        core.setByASE(data[0] || EmptyAseData);

        const representation = lightPluginRef.current?.managers.representation;
        if (representation) {
            representation.hideBond = format === 'dump';
        }
        await render(core, {
            changeFile: false,
            autoLockCamera: false,
        });
        formatSubjectRef.current.next(format);
    }, []);

    // const readData = useCallback(async (fileContent: string, format: MaterialFormat) => {
    //     const res = await getASEByFileReq({
    //         fileContent,
    //         format,
    //     });

    //     setAndRenderData(res.data);
    // }, []);

    // const readFile = useCallback(async (file: File) => {
    //     const fileContent = await readFileText(file);
    //     const ext = getExtByName(file.name);
    //     await readData(fileContent, ext as MaterialFormat);
    // }, []);

    const readCloudDisk = useCallback(async (params: { projectId?: number; userId?: number; path: string }) => {
        const name = getNameByPath(params.path);
        const format = getExtByName(name);
        const searchParams = new URLSearchParams();
        searchParams.set('projectId', String(params.projectId || 0));
        searchParams.set('userId', String(params.userId || userInfo?.userId));
        searchParams.set('token', Cookies.get(APP_CONFIG.COOKIE_NAME)!);
        const fileUrl = `${APP_CONFIG.HOST}/bohrapi/v1/file/download/${params.path}?${searchParams.toString()}`;
        const res = await (format === 'dump'
            ? dump()
            : getASEByCloudDiskReq({
                  fileUrl,
                  format,
              }));

        async function dump() {
            const fileContent = await (await fetch(fileUrl)).text();
            const ase = readLammpsDumpText(fileContent);

            return {
                data: ase,
            };
        }
        setAndRenderData(res.data, format as MaterialFormat);
    }, []);

    const download = useCallback(async (name: string) => {
        if (!canISave()) {
            return;
        }

        const format = getExtByName(name);
        const fileContent = (() => {
            if (isTrajSubjectRef.current) {
                return dataSubjectRef.current.value!;
            }

            const ase = coreRef.current?.getAse();
            return ase ? [ase] : undefined;
        })();

        if (!fileContent) {
            return;
        }

        const res = await exportASE2FileReq({
            fileContent,
            format,
        });

        downloadFileFromBlob(res.data, 'text/plain', name);
    }, []);

    const saveToCloudDisk = useCallback(async (params: { projectId?: number; path: string }) => {
        if (!canISave()) {
            return;
        }
        const { projectId, path } = params;
        const ase = coreRef.current?.getAse();
        const name = path.slice(path.lastIndexOf('/') + 1);
        const format = getExtByName(name);
        if (!ase) {
            return;
        }
        return exportASE2CloudDiskReq({
            fileContent: [ase],
            projectId: projectId || 0,
            path,
            format,
        });
    }, []);

    return {
        // readData,
        // readFile,
        readCloudDisk,
        download,
        saveToCloudDisk,
        canISave,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DIOProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DIO = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DIOProvider');
    }
    return context;
};
