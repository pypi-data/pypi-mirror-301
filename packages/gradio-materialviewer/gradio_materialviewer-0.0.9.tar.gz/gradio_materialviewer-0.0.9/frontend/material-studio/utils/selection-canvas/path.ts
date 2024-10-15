import { Point } from './models/point';
import { Line } from './models/line';

export const simplifyPath = (points: Point[], tolerance: number) => {
    const douglasPeucker = (points: Point[], tolerance: number) => {
        if (points.length <= 2) {
            return [points[0]];
        }
        let returnPoints: Point[] = [];
        // make line from start to end
        const line = new Line(points[0], points[points.length - 1]);
        // find the largest distance from intermediate poitns to this line
        let maxDistance = 0;
        let maxDistanceIndex = 0;
        let p;
        for (let i = 1; i <= points.length - 2; i++) {
            const distance = line.distanceToPoint(points[i]);
            if (distance > maxDistance) {
                maxDistance = distance;
                maxDistanceIndex = i;
            }
        }
        // check if the max distance is greater than our tollerance allows
        if (maxDistance >= tolerance) {
            p = points[maxDistanceIndex];
            line.distanceToPoint(p);
            // include this point in the output
            returnPoints = returnPoints.concat(douglasPeucker(points.slice(0, maxDistanceIndex + 1), tolerance));
            // returnPoints.push( points[maxDistanceIndex] );
            returnPoints = returnPoints.concat(
                douglasPeucker(points.slice(maxDistanceIndex, points.length), tolerance)
            );
        } else {
            // ditching this point
            p = points[maxDistanceIndex];
            line.distanceToPoint(p);
            returnPoints = [points[0]];
        }
        return returnPoints;
    };
    const arr = douglasPeucker(points, tolerance);
    // always have to push the very last point on so it doesn't get left off
    arr.push(points[points.length - 1]);
    return arr;
};

// 判断点是否在多边形内
const INF = 10000;
// Given three collinear points p, q, r,
// the function checks if point q lies
// on line segment 'pr'
const onSegment = (p: Point, q: Point, r: Point) => {
    if (
        q.x <= Math.max(p.x, r.x) &&
        q.x >= Math.min(p.x, r.x) &&
        q.y <= Math.max(p.y, r.y) &&
        q.y >= Math.min(p.y, r.y)
    ) {
        return true;
    }
    return false;
};

// To find orientation of ordered triplet (p, q, r).
// The function returns following values
// 0 --> p, q and r are collinear
// 1 --> Clockwise
// 2 --> Counterclockwise
const orientation = (p: Point, q: Point, r: Point) => {
    const val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);

    if (val === 0) {
        return 0; // collinear
    }
    return val > 0 ? 1 : 2; // clock or counterclock wise
};

// The function that returns true if
// line segment 'p1q1' and 'p2q2' intersect.
const doIntersect = (p1: Point, q1: Point, p2: Point, q2: Point) => {
    // Find the four orientations needed for
    // general and special cases
    const o1 = orientation(p1, q1, p2);
    const o2 = orientation(p1, q1, q2);
    const o3 = orientation(p2, q2, p1);
    const o4 = orientation(p2, q2, q1);

    // General case
    if (o1 !== o2 && o3 !== o4) {
        return true;
    }

    // Special Cases
    // p1, q1 and p2 are collinear and
    // p2 lies on segment p1q1
    if (o1 === 0 && onSegment(p1, p2, q1)) {
        return true;
    }

    // p1, q1 and p2 are collinear and
    // q2 lies on segment p1q1
    if (o2 === 0 && onSegment(p1, q2, q1)) {
        return true;
    }

    // p2, q2 and p1 are collinear and
    // p1 lies on segment p2q2
    if (o3 === 0 && onSegment(p2, p1, q2)) {
        return true;
    }

    // p2, q2 and q1 are collinear and
    // q1 lies on segment p2q2
    if (o4 === 0 && onSegment(p2, q1, q2)) {
        return true;
    }

    // Doesn't fall in any of the above cases
    return false;
};

// Returns true if the point p lies
// inside the polygon[] with n vertices
export const isInside = (polygon: Point[], n: number, p: Point) => {
    // There must be at least 3 vertices in polygon[]
    if (n < 3) {
        return false;
    }

    // Create a point for line segment from p to infinite
    const extreme = new Point(INF, p.y);

    // Count intersections of the above line
    // with sides of polygon
    let count = 0;
    let i = 0;
    do {
        const next = (i + 1) % n;

        // Check if the line segment from 'p' to
        // 'extreme' intersects with the line
        // segment from 'polygon[i]' to 'polygon[next]'
        if (doIntersect(polygon[i], polygon[next], p, extreme)) {
            // If the point 'p' is collinear with line
            // segment 'i-next', then check if it lies
            // on segment. If it lies, return true, otherwise false
            if (orientation(polygon[i], p, polygon[next]) === 0) {
                return onSegment(polygon[i], p, polygon[next]);
            }

            count++;
        }
        i = next;
    } while (i !== 0);

    // Return true if count is odd, false otherwise
    return count % 2 === 1; // Same as (count%2 == 1)
};
