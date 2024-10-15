import Konva from 'konva';
import { StateUnit } from './state-unit';

const padding = 40;

export const initialStageState = {
    width: 0,
    frame: 0,
    currentFrame: 0,
    stepPixel: 0,
    currentX: 0,
    onHover: false,
    hoverFrame: 0,
    hoverX: 0,
};

type ScaleRulerStageState = typeof initialStageState;

export class ScaleRulerStage extends StateUnit<ScaleRulerStageState> {
    stage!: Konva.Stage;

    layer = new Konva.Layer();

    wacthSet = new Set<(frame: number) => void>();

    state = initialStageState;

    addShortLine(x: number) {
        const y1 = 30;
        const y2 = y1 + 5.65;
        const line = new Konva.Line({
            points: [x, y1, x, y2],
            stroke: '#dbdcf0',
            strokeWidth: 1,
        });
        this.layer.add(line);
    }

    addMarkText(x: number, index: number) {
        const text = new Konva.Text({
            x: x - 50,
            y: 9,
            text: String(index),
            width: 100,
            align: 'center',
            fontSize: 10,
            lineHeight: 1.6,
            fontFamily: 'Roboto-Regular',
            fill: '#70749E',
        });
        this.layer.add(text);
    }

    addLongLine(x: number) {
        const y1 = 27.25;
        const y2 = y1 + 12;
        const line = new Konva.Line({
            points: [x, y1, x, y2],
            stroke: '#dbdcf0',
            strokeWidth: 1,
        });
        this.layer.add(line);
    }

    drawScaler() {
        this.layer.clear();
        this.layer.removeChildren();
        const { width, frame } = this.state;
        const largeScalerDis = 18;
        const mediumScalerDis = 12;
        const smallScalerDis = 8;
        const largeSize = Math.floor(width / largeScalerDis);
        const mediumSize = Math.floor(width / mediumScalerDis);
        const smallSize = Math.floor(width / smallScalerDis);
        const { zoom, interval } = getScalerZoom({
            frame,
            largeSize,
            mediumSize,
            smallSize,
        });
        const stepPixel = width / frame;
        this.setState({ stepPixel, currentX: this.state.currentFrame * stepPixel });
        for (let i = 0; i <= frame; i++) {
            if (i % zoom === 0) {
                const x = stepPixel * i + padding;
                if ((i / zoom) % interval === 0) {
                    this.addLongLine(x);
                    this.addMarkText(x, i);
                } else {
                    this.addShortLine(x);
                }
            }
        }
        this.layer.draw();
    }

    getFrameByX(x: number) {
        let frame = Math.round(x / this.state.stepPixel);
        if (frame < 0) {
            frame = 0;
        }
        if (frame > this.state.frame) {
            frame = this.state.frame;
        }
        return { frame, x: frame * this.state.stepPixel };
    }

    destroy() {
        this.stage?.destroy();
    }

    reset() {
        const width = this.container.clientWidth;
        this.stage.setAttr('width', width);
        this.state.width = width - padding * 2;
        this.drawScaler();
    }

    resetFrame(frame: number) {
        this.setState({ frame });
    }

    watch(fn: (frame: number) => void) {
        this.wacthSet.add(fn);
    }

    submitWatch(frame: number) {
        this.wacthSet.forEach(fn => fn(frame));
    }

    constructor(public container: HTMLDivElement, frame: number) {
        super();
        this.state.width = container.clientWidth - padding * 2;
        this.state.frame = frame;

        this.stage = new Konva.Stage({
            container,
            width: container.clientWidth,
            height: 38,
        });
        this.stage.add(this.layer);
        this.stage.on('mousemove', ({ evt }) => {
            const { offsetX, offsetY } = evt;
            if (offsetX >= 0 && offsetX <= this.container.clientWidth && offsetY < 26) {
                const { frame: hoverFrame } = this.getFrameByX(offsetX - padding);
                this.setState({
                    onHover: true,
                    hoverX: offsetX,
                    hoverFrame,
                });
            } else {
                this.setState({
                    onHover: false,
                });
            }
        });
        this.stage.on('mouseout', () => {
            this.setState({
                onHover: false,
            });
        });
        this.stage.on('click', ({ evt }) => {
            const { frame, x } = this.getFrameByX(evt.offsetX - padding);
            this.setState({
                currentX: x,
                currentFrame: frame,
            });
            this.submitWatch(frame);
        });
        this.stage.listening(true);

        this.drawScaler();
    }
}

function getScalerZoom(params: {
    frame: number;
    zoom?: number;
    largeSize: number;
    mediumSize: number;
    smallSize: number;
}): { zoom: number; interval: number } {
    const { frame, zoom = 1, largeSize, mediumSize, smallSize } = params;

    const frameSize = frame / zoom;
    if (zoom === 1) {
        if (largeSize > frameSize) {
            return { zoom, interval: 1 };
        }
        if (mediumSize > frameSize) {
            return { zoom, interval: 5 };
        }
        if (smallSize > frameSize) {
            return { zoom, interval: 10 };
        }
        return getScalerZoom({
            ...params,
            zoom: 5,
        });
    }
    if (String(zoom).startsWith('5')) {
        if (largeSize > frameSize) {
            return { zoom, interval: 2 };
        }
        if (mediumSize > frameSize) {
            return { zoom, interval: 4 };
        }
        if (smallSize > frameSize) {
            return { zoom, interval: 10 };
        }
        return getScalerZoom({
            ...params,
            zoom: zoom * 2,
        });
    }
    if (largeSize > frameSize) {
        return { zoom, interval: 2 };
    }
    if (mediumSize > frameSize) {
        return { zoom, interval: 5 };
    }
    if (smallSize > frameSize) {
        return { zoom, interval: 10 };
    }
    return getScalerZoom({
        ...params,
        zoom: zoom * 5,
    });
}
