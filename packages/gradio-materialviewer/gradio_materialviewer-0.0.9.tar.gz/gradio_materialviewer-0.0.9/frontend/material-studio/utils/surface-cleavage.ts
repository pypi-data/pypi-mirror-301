import {
    MathCollection,
    add,
    cross,
    divide,
    dot,
    dotMultiply,
    floor,
    gcd,
    inv,
    matrix,
    mod,
    multiply,
    norm,
    prod,
    sqrt,
    subtract,
} from 'mathjs';
import { Bulk } from './bulk';

function isZero(x: number): boolean {
    return Math.abs(x) < 1e-6;
}

function ext_gcd(a: number, b: number): [number, number] {
    if (b === 0) return [1, 0];
    else if (a % b === 0) return [0, 1];
    else {
        const [x, y] = ext_gcd(b, a % b);
        return [y, x - y * Math.floor(a / b)];
    }
}

function negativeZeroConvert(value: number): number {
    return Object.is(value, -0) ? 0 : value;
}

export function getSurfaceVector(
    a1: [number, number, number],
    a2: [number, number, number],
    a3: [number, number, number],
    h: number,
    k: number,
    l: number
) {
    const h0 = isZero(h);
    const k0 = isZero(k);
    const l0 = isZero(l);

    let c1: [number, number, number] = [0, 0, 0];
    let c2: [number, number, number] = [0, 0, 0];
    let c3: [number, number, number] = [0, 0, 0];
    if ((h0 && k0) || (h0 && l0) || (k0 && l0)) {
        if (!h0) {
            c1 = [0, 1, 0];
            c2 = [0, 0, 1];
            c3 = [1, 0, 0];
        }
        if (!k0) {
            c1 = [0, 0, 1];
            c2 = [1, 0, 0];
            c3 = [0, 1, 0];
        }
        if (!l0) {
            c1 = [1, 0, 0];
            c2 = [0, 1, 0];
            c3 = [0, 0, 1];
        }
    } else {
        let [p, q] = ext_gcd(k, l);
        //k1 = np.dot(p * (k * a1 - h * a2) + q * (l * a1 - h * a3),l * a2 - k * a3)
        const vec1 = subtract(multiply(k, a1), multiply(h, a2));
        const vec2 = subtract(multiply(l, a1), multiply(h, a3));
        const vec3 = subtract(multiply(l, a2), multiply(k, a3));
        // @ts-ignore
        const k1 = dot(add(multiply(p, vec1), multiply(q, vec2)) as MathCollection, vec3 as MathCollection);

        //k2 = np.dot(l * (k * a1 - h * a2) - k * (l * a1 - h * a3), l * a2 - k * a3)
        // @ts-ignore
        const k2 = dot(subtract(multiply(l, vec1), multiply(k, vec2)) as MathCollection, vec3 as MathCollection);

        if (Math.abs(k2) > 1e-10) {
            const i = -Math.trunc(Math.round(k1 / k2));
            [p, q] = [p + i * l, q - i * k];
        }
        const [a, b] = ext_gcd(p * k + q * l, h);

        c1 = [p * k + q * l, -p * h, -q * h];
        const lk_gcd = gcd(l, k);
        c2 = [0, Math.floor(l / lk_gcd), Math.floor(-k / lk_gcd)];
        c3 = [b, a * p, a * q];

        c1 = c1.map(negativeZeroConvert) as [number, number, number];
        c2 = c2.map(negativeZeroConvert) as [number, number, number];
        c3 = c3.map(negativeZeroConvert) as [number, number, number];
    }
    return [
        // 新晶矢系数
        [c1, c2, c3],
        // 新晶矢笛卡尔坐标
        multiply(matrix([c1, c2, c3]), matrix([a1, a2, a3])).valueOf() as number[][],
    ];
}

export function buildBulk(bulk: Bulk, basis: number[][], layers: number, periodic: boolean) {
    const surf = bulk.copy();
    let newFractionalCoordinates = multiply(surf.getFractionalCoordinates(), inv(basis));
    newFractionalCoordinates = add(newFractionalCoordinates, 1e-10).valueOf() as number[][];
    newFractionalCoordinates = subtract(newFractionalCoordinates, floor(newFractionalCoordinates));
    surf.setFractionalCoordinates(newFractionalCoordinates);

    surf.setCell(multiply(basis, surf.getCell()).valueOf() as number[][], true);
    surf.makeSuperCell(1, 1, layers);

    let [a1, a2, a3] = surf.getCell();
    const _tmp_value = cross(a1, a2);
    const _tmp_value_norm = norm(_tmp_value);
    a3 = divide(dotMultiply(_tmp_value, dot(a3, _tmp_value)), prod(_tmp_value_norm, _tmp_value_norm)).valueOf() as [
        number,
        number,
        number
    ];

    surf.setCell([a1, a2, a3], false);
    const a1_new = [norm(a1).valueOf() as number, 0, 0];
    let _tmp: number = divide(dot(a1, a2), norm(a1)).valueOf() as number;
    let _tmp_a2_norm = norm(a2);
    const a2_new = [
        _tmp,
        sqrt(subtract(prod(_tmp_a2_norm, _tmp_a2_norm), _tmp * _tmp).valueOf() as number).valueOf() as number,
        0,
    ];
    const a3_new = [0, 0, norm(a3).valueOf() as number];
    surf.setCell([a1_new, a2_new, a3_new], true);
    surf.setPBC([true, true, periodic]);

    // Move atoms into the unit cell
    let fractionalCoordinates = surf.getFractionalCoordinates();
    fractionalCoordinates = mod(fractionalCoordinates, 1);
    surf.setFractionalCoordinates(fractionalCoordinates);

    return surf;
}
