import { useCallback, useRef, useState } from 'react';
import { useMaterial3DCore } from '../context/core';
import { getElementLociInfo } from '../utils/utils';
import { Loci } from 'dpmol';

export function useHoverAtom() {
    const { lightPluginRef } = useMaterial3DCore();
    const [hoverAtom, setHoverAtom] = useState<
        | {
              element: string;
              x: number;
              y: number;
              z: number;
              page?: number[];
          }
        | undefined
    >();

    const subscribeHoverEvent = useCallback(() => {
        if (!lightPluginRef.current) {
            return () => {};
        }
        lightPluginRef.current.canvas3d?.controls.setLockCameraState(true);
        lightPluginRef.current?.managers.highlight.hoverLoci?.loci;
        // @ts-ignore
        const subscription = lightPluginRef.current.canvas3d?.interaction.hover.subscribe(ev => {
            const { loci } = ev.current;
            if (loci?.kind === 'element-loci') {
                const info = getElementLociInfo(loci);
                setHoverAtom({
                    ...info!,
                    page: ev.page,
                });
                return;
            }
            setHoverAtom(undefined);
        });

        return function unsubscribe() {
            subscription?.unsubscribe();
        };
    }, []);

    return {
        hoverAtom,
        subscribeHoverEvent,
    };
}
