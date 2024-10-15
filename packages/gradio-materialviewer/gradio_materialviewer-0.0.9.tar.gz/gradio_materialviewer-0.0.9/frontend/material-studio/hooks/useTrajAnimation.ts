import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useInterval } from 'react-use';

import { useMaterial3DCore } from '../context';
import { MaterialCore } from '../core';

export function useTrajAnimation() {
    const { render, dataSubjectRef } = useMaterial3DCore();

    const [delay, setDelay] = useState(200);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentIndex, setCurrentIndex] = useState(0);
    const currentIndexRef = useRef(currentIndex);
    currentIndexRef.current = currentIndex;
    const [frameLength, setFrameLength] = useState(dataSubjectRef.current.value.length);
    const maxFrameIndex = useMemo(() => frameLength - 1, [frameLength]);

    useInterval(
        () => {
            nextFrame();
        },
        isPlaying ? delay : null
    );

    const reset = useCallback(() => {
        setIsPlaying(false);
        setCurrentIndex(0);
        setFrameLength(dataSubjectRef.current.value.length);
    }, []);

    const setFrame = useCallback((n: number) => {
        let current = n;
        const max = dataSubjectRef.current.value.length - 1;
        if (current >= max) {
            current = max;
            setIsPlaying(false);
        }
        if (current < 0) {
            current = 0;
        }
        setCurrentIndex(current);
        const data = dataSubjectRef.current.value[current];
        const core = new MaterialCore();
        core.setByASE(data);
        render(core, {
            changeFile: false,
            changeHistory: false,
        });
    }, []);

    const nextFrame = useCallback(() => {
        setFrame(++currentIndexRef.current);
    }, []);

    const prevFrame = useCallback(() => {
        setFrame(--currentIndexRef.current);
    }, []);

    const play = useCallback(() => {
        const max = dataSubjectRef.current.value.length - 1;
        if (currentIndexRef.current >= max) {
            setFrame(0);
        }
        setIsPlaying(true);
    }, []);

    const pause = useCallback(() => {
        setIsPlaying(false);
    }, []);

    useEffect(() => {
        const subscription = dataSubjectRef.current.subscribe(() => {
            reset();
        });

        return () => {
            subscription.unsubscribe();
        };
    }, []);

    return {
        delay,
        setDelay,
        isPlaying,
        currentIndex,
        frameLength,
        maxFrameIndex,
        setFrame,
        nextFrame,
        prevFrame,
        play,
        pause,
        stop: reset,
    };
}
