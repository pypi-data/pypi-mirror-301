import { Point } from './point';

export class Line {
    p1: Point;

    p2: Point;

    constructor(p1: Point, p2: Point) {
        this.p1 = p1;
        this.p2 = p2;
    }

    distanceToPoint(point: Point) {
        const m = (this.p2.y - this.p1.y) / (this.p2.x - this.p1.x);
        // y offset
        const b = this.p1.y - m * this.p1.x;
        const d = [];
        // distance to the linear equation
        // eslint-disable-next-line no-restricted-properties
        d.push(Math.abs(point.y - m * point.x - b) / Math.sqrt(Math.pow(m, 2) + 1));
        // distance to p1
        // eslint-disable-next-line no-restricted-properties
        d.push(Math.sqrt(Math.pow(point.x - this.p1.x, 2) + Math.pow(point.y - this.p1.y, 2)));
        // distance to p2
        // eslint-disable-next-line no-restricted-properties
        d.push(Math.sqrt(Math.pow(point.x - this.p2.x, 2) + Math.pow(point.y - this.p2.y, 2)));
        // return the smallest distance
        return d.sort(function (a, b) {
            return a - b; // causes an array to be sorted numerically and ascending
        })[0];
    }
}
