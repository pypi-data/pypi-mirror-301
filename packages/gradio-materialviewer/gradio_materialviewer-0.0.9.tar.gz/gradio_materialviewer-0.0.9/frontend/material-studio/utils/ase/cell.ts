import { sqrt, sin, cos, pi, dot, cross, norm, matrix, transpose, multiply, divide, abs, acos } from 'mathjs';

function unitVector(x: number[]): number[] {
    const y = x.map(n => n as number); // Ensure elements are numbers
    return divide(y, norm(y)) as number[];
}

export function cellparToCell(
    cellpar: number | number[],
    abNormal: number[] = [0, 0, 1],
    aDirection?: number[]
): number[][] {
    if (!aDirection) {
        const crossProduct = cross(abNormal, [1, 0, 0]) as number[];
        if ((norm(crossProduct) as number) < 1e-5) {
            aDirection = [0, 0, 1];
        } else {
            aDirection = [1, 0, 0];
        }
    }

    const ad = aDirection;
    const Z = unitVector(abNormal);
    const X = unitVector(ad.map((v, i) => v - dot(ad, Z) * Z[i]));
    const Y = cross(Z, X) as number[];

    let alpha = 90,
        beta = 90,
        gamma = 90;
    let a, b, c;

    if (typeof cellpar === 'number') {
        a = b = c = cellpar;
    } else if (cellpar.length === 1) {
        a = b = c = cellpar[0];
    } else if (cellpar.length === 3) {
        [a, b, c] = cellpar;
    } else {
        [a, b, c, alpha, beta, gamma] = cellpar;
    }

    const eps = 2 * Number.EPSILON; // around 1.4e-14

    let cosAlpha = abs(alpha - 90) < eps ? 0 : cos((alpha * pi) / 180);
    let cosBeta = abs(beta - 90) < eps ? 0 : cos((beta * pi) / 180);
    let cosGamma, sinGamma;

    if (abs(gamma - 90) < eps) {
        cosGamma = 0;
        sinGamma = 1;
    } else if (abs(gamma + 90) < eps) {
        cosGamma = 0;
        sinGamma = -1;
    } else {
        cosGamma = cos((gamma * pi) / 180);
        sinGamma = sin((gamma * pi) / 180);
    }

    const va = [a, 0, 0];
    const vb = [b * cosGamma, b * sinGamma, 0];
    const cx = cosBeta;
    const cy = (cosAlpha - cosBeta * cosGamma) / sinGamma;
    const czSqr = 1 - cx * cx - cy * cy;
    if (czSqr < 0) throw new Error('cz_sqr is negative, which is not possible');
    const cz = sqrt(czSqr) as number;

    const vc = [c * cx, c * cy, c * cz];

    const abc = matrix([va, vb, vc]);
    const T = matrix([X, Y, Z]);
    const cell = multiply(abc, transpose(T));

    return cell.toArray() as number[][];
}

export function cellToCellpar(cell: number[][], radians: boolean = false): number[] {
    /**
     * Returns the cell parameters [a, b, c, alpha, beta, gamma].
     *
     * Angles are in degrees unless radians=True is used.
     */

    const lengths = cell.map(v => norm(v));
    const angles = [];

    for (let i = 0; i < 3; i++) {
        const j = (i + 2) % 3;
        const k = (i + 1) % 3;
        const ll = multiply(lengths[j], lengths[k]) as number;
        let angle;

        if (ll > 1e-16) {
            const x = dot(cell[j], cell[k]) / ll;
            angle = (180.0 / pi) * (acos(x) as number);
        } else {
            angle = 90.0;
        }
        angles.push(angle);
    }

    if (radians) {
        for (let i = 0; i < angles.length; i++) {
            angles[i] = (angles[i] * pi) / 180;
        }
    }

    return [...(lengths as number[]), ...angles];
}
