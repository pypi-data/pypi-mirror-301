import { useCallback, useMemo, useState } from 'react';
import { LatticeValue } from '../model';

interface OnConvertValue {
    (changed: LatticeValue): LatticeValue;
}

interface CrystalSystem {
    convert: OnConvertValue;
    disabled: {
        a: boolean;
        b: boolean;
        c: boolean;
        alpha: boolean;
        beta: boolean;
        gamma: boolean;
    };
    initialValues: Partial<LatticeValue>;
    description: string;
}

type CrystalSystemParams = {
    convert?: OnConvertValue;
    disabled: Partial<CrystalSystem['disabled']>;
} & Omit<CrystalSystem, 'disabled' | 'convert'>;

export function getCrystalOrder(no: number) {
    if (no < 3) {
        return 0;
    }
    if (no < 16) {
        return 1;
    }
    if (no < 75) {
        return 2;
    }
    if (no < 143) {
        return 3;
    }
    if (no < 168) {
        return 4;
    }
    if (no < 195) {
        return 5;
    }
    return 6;
}

function createCrystalSystem(params: CrystalSystemParams) {
    const disabled: CrystalSystem['disabled'] = Object.assign(
        {
            a: false,
            b: false,
            c: false,
            alpha: false,
            beta: false,
            gamma: false,
        },
        params.disabled
    );

    return {
        ...params,
        disabled,
        convert: params.convert || ((n: number) => n),
    } as CrystalSystem;
}

// 三斜晶系 α≠β≠γ≠90°，a≠b≠c
const TriclinicSystem = createCrystalSystem({
    disabled: {},
    initialValues: {},
    description: `α≠β≠γ≠90°，a≠b≠c`,
});
// 单斜晶系 α=γ=90°，β≠90°，a≠b≠c
const MonoclinicSystem = createCrystalSystem({
    disabled: {
        alpha: true,
        gamma: true,
    },
    initialValues: {
        alpha: 90,
        gamma: 90,
    },
    description: `α=γ=90°，β≠90°，a≠b≠c`,
});
// orthorhombic system
// 正交/斜方晶系 α=β=γ=90°，a≠b≠c
const OrthorhombicSystem = createCrystalSystem({
    disabled: {
        alpha: true,
        beta: true,
        gamma: true,
    },
    initialValues: {
        alpha: 90,
        beta: 90,
        gamma: 90,
    },
    description: `α=β=γ=90°，a≠b≠c`,
});
// tetragonal system
// 四方/正方晶系 α=β=γ=90°，a=b≠c
const TetragonalSystem = createCrystalSystem({
    disabled: {
        b: true,
        alpha: true,
        beta: true,
        gamma: true,
    },
    initialValues: {
        alpha: 90,
        beta: 90,
        gamma: 90,
    },
    convert: v => ({ ...v, b: v.a }),
    description: `α=β=γ=90°，a=b≠c`,
});
// trigonal system
// 三方晶系 α=β=γ≠90°，a=b=c
// TODO: 疑惑，ms的三方晶系都在使用六方晶系参数
const TrigonalSystem = createCrystalSystem({
    disabled: {
        b: true,
        c: true,
        beta: true,
        gamma: true,
    },
    initialValues: {},
    convert: v => ({ ...v, b: v.a, c: v.a, beta: v.alpha, gamma: v.alpha }),
    description: `α=β=γ≠90°，a=b=c`,
});
// hexagonal system
// 六方晶系 α=β=90°，γ=120°，a=b≠c
const HexagonalSystem = createCrystalSystem({
    disabled: {
        b: true,
        alpha: true,
        beta: true,
        gamma: true,
    },
    initialValues: {
        alpha: 90,
        beta: 90,
        gamma: 120,
    },
    convert: v => ({ ...v, b: v.a }),
    description: `α=β=90°，γ=120°，a=b≠c`,
});
// cubic system
// 立方/等轴晶系 α=β=γ=90°，a=b=c
const CubicSystem = createCrystalSystem({
    disabled: {
        b: true,
        c: true,
        alpha: true,
        beta: true,
        gamma: true,
    },
    initialValues: {
        alpha: 90,
        beta: 90,
        gamma: 90,
    },
    convert: v => ({ ...v, b: v.a, c: v.a }),
    description: `α=β=γ=90°，a=b=c`,
});

const CrystalSystemList = [
    TriclinicSystem,
    MonoclinicSystem,
    OrthorhombicSystem,
    TetragonalSystem,
    TrigonalSystem,
    HexagonalSystem,
    CubicSystem,
];

const SpaceGroupList = [
    { no: 1, symbol: 'P1' },
    { no: 2, symbol: 'P-1' },
    { no: 3, symbol: 'P121' },
    { no: 4, symbol: 'P1211' },
    { no: 5, symbol: 'C121' },
    { no: 6, symbol: 'P1m1' },
    { no: 7, symbol: 'P1c1' },
    { no: 8, symbol: 'C1m1' },
    { no: 9, symbol: 'C1c1' },
    { no: 10, symbol: 'P12/m1' },
    { no: 11, symbol: 'P121/m1' },
    { no: 12, symbol: 'C12/m1' },
    { no: 13, symbol: 'P12/c1' },
    { no: 14, symbol: 'P121/c1' },
    { no: 15, symbol: 'C12/c1' },
    { no: 16, symbol: 'P222' },
    { no: 17, symbol: 'P2221' },
    { no: 18, symbol: 'P21212' },
    { no: 19, symbol: 'P212121' },
    { no: 20, symbol: 'C2221' },
    { no: 21, symbol: 'C222' },
    { no: 22, symbol: 'F222' },
    { no: 23, symbol: 'I222' },
    { no: 24, symbol: 'I212121' },
    { no: 25, symbol: 'Pmm2' },
    { no: 26, symbol: 'Pmc21' },
    { no: 27, symbol: 'Pcc2' },
    { no: 28, symbol: 'Pma2' },
    { no: 29, symbol: 'Pca21' },
    { no: 30, symbol: 'Pnc2' },
    { no: 31, symbol: 'Pmn21' },
    { no: 32, symbol: 'Pba2' },
    { no: 33, symbol: 'Pna21' },
    { no: 34, symbol: 'Pnn2' },
    { no: 35, symbol: 'Cmm2' },
    { no: 36, symbol: 'Cmc21' },
    { no: 37, symbol: 'Ccc2' },
    { no: 38, symbol: 'Amm2' },
    { no: 39, symbol: 'Abm2' },
    { no: 40, symbol: 'Ama2' },
    { no: 41, symbol: 'Aba2' },
    { no: 42, symbol: 'Fmm2' },
    { no: 43, symbol: 'Fdd2' },
    { no: 44, symbol: 'Imm2' },
    { no: 45, symbol: 'Iba2' },
    { no: 46, symbol: 'Ima2' },
    { no: 47, symbol: 'Pmmm' },
    { no: 48, symbol: 'Pnnn' },
    { no: 49, symbol: 'Pccm' },
    { no: 50, symbol: 'Pban' },
    { no: 51, symbol: 'Pmma' },
    { no: 52, symbol: 'Pnna' },
    { no: 53, symbol: 'Pmna' },
    { no: 54, symbol: 'Pcca' },
    { no: 55, symbol: 'Pbam' },
    { no: 56, symbol: 'Pccn' },
    { no: 57, symbol: 'Pbcm' },
    { no: 58, symbol: 'Pnnm' },
    { no: 59, symbol: 'Pmmn' },
    { no: 60, symbol: 'Pbcn' },
    { no: 61, symbol: 'Pbca' },
    { no: 62, symbol: 'Pnma' },
    { no: 63, symbol: 'Cmcm' },
    { no: 64, symbol: 'Cmca' },
    { no: 65, symbol: 'Cmmm' },
    { no: 66, symbol: 'Cccm' },
    { no: 67, symbol: 'Cmma' },
    { no: 68, symbol: 'Ccca' },
    { no: 69, symbol: 'Fmmm' },
    { no: 70, symbol: 'Fddd' },
    { no: 71, symbol: 'Immm' },
    { no: 72, symbol: 'Ibam' },
    { no: 73, symbol: 'Ibca' },
    { no: 74, symbol: 'Imma' },
    { no: 75, symbol: 'P4' },
    { no: 76, symbol: 'P41' },
    { no: 77, symbol: 'P42' },
    { no: 78, symbol: 'P43' },
    { no: 79, symbol: 'I4' },
    { no: 80, symbol: 'I41' },
    { no: 81, symbol: 'P-4' },
    { no: 82, symbol: 'I-4' },
    { no: 83, symbol: 'P4/m' },
    { no: 84, symbol: 'P42/m' },
    { no: 85, symbol: 'P4/n' },
    { no: 86, symbol: 'P42/n' },
    { no: 87, symbol: 'I4/m' },
    { no: 88, symbol: 'I41/a' },
    { no: 89, symbol: 'P422' },
    { no: 90, symbol: 'P4212' },
    { no: 91, symbol: 'P4122' },
    { no: 92, symbol: 'P41212' },
    { no: 93, symbol: 'P4222' },
    { no: 94, symbol: 'P42212' },
    { no: 95, symbol: 'P4322' },
    { no: 96, symbol: 'P43212' },
    { no: 97, symbol: 'I422' },
    { no: 98, symbol: 'I4122' },
    { no: 99, symbol: 'P4mm' },
    { no: 100, symbol: 'P4bm' },
    { no: 101, symbol: 'P42cm' },
    { no: 102, symbol: 'P42nm' },
    { no: 103, symbol: 'P4cc' },
    { no: 104, symbol: 'P4nc' },
    { no: 105, symbol: 'P42mc' },
    { no: 106, symbol: 'P42bc' },
    { no: 107, symbol: 'I4mm' },
    { no: 108, symbol: 'I4cm' },
    { no: 109, symbol: 'I41md' },
    { no: 110, symbol: 'I41cd' },
    { no: 111, symbol: 'P-42m' },
    { no: 112, symbol: 'P-42c' },
    { no: 113, symbol: 'P-421m' },
    { no: 114, symbol: 'P-421c' },
    { no: 115, symbol: 'P-4m2' },
    { no: 116, symbol: 'P-4c2' },
    { no: 117, symbol: 'P-4b2' },
    { no: 118, symbol: 'P-4n2' },
    { no: 119, symbol: 'I-4m2' },
    { no: 120, symbol: 'I-4c2' },
    { no: 121, symbol: 'I-42m' },
    { no: 122, symbol: 'I-42d' },
    { no: 123, symbol: 'P4/mmm' },
    { no: 124, symbol: 'P4/mcc' },
    { no: 125, symbol: 'P4/nbm' },
    { no: 126, symbol: 'P4/nnc' },
    { no: 127, symbol: 'P4/mbm' },
    { no: 128, symbol: 'P4/mnc' },
    { no: 129, symbol: 'P4/nmm' },
    { no: 130, symbol: 'P4/ncc' },
    { no: 131, symbol: 'P42/mmc' },
    { no: 132, symbol: 'P42/mcm' },
    { no: 133, symbol: 'P42/nbc' },
    { no: 134, symbol: 'P42/nnm' },
    { no: 135, symbol: 'P42/mbc' },
    { no: 136, symbol: 'P42/mnm' },
    { no: 137, symbol: 'P42/nmc' },
    { no: 138, symbol: 'P42/ncm' },
    { no: 139, symbol: 'I4/mmm' },
    { no: 140, symbol: 'I4/mcm' },
    { no: 141, symbol: 'I41/amd' },
    { no: 142, symbol: 'I41/acd' },
    { no: 143, symbol: 'P3' },
    { no: 144, symbol: 'P31' },
    { no: 145, symbol: 'P32' },
    { no: 146, symbol: 'R3' },
    { no: 147, symbol: 'P-3' },
    { no: 148, symbol: 'R-3' },
    { no: 149, symbol: 'P312' },
    { no: 150, symbol: 'P321' },
    { no: 151, symbol: 'P3112' },
    { no: 152, symbol: 'P3121' },
    { no: 153, symbol: 'P3212' },
    { no: 154, symbol: 'P3221' },
    { no: 155, symbol: 'R32' },
    { no: 156, symbol: 'P3m1' },
    { no: 157, symbol: 'P31m' },
    { no: 158, symbol: 'P3c1' },
    { no: 159, symbol: 'P31c' },
    { no: 160, symbol: 'R3m' },
    { no: 161, symbol: 'R3c' },
    { no: 162, symbol: 'P-31m' },
    { no: 163, symbol: 'P-31c' },
    { no: 164, symbol: 'P-3m1' },
    { no: 165, symbol: 'P-3c1' },
    { no: 166, symbol: 'R-3m' },
    { no: 167, symbol: 'R-3c' },
    { no: 168, symbol: 'P6' },
    { no: 169, symbol: 'P61' },
    { no: 170, symbol: 'P65' },
    { no: 171, symbol: 'P62' },
    { no: 172, symbol: 'P64' },
    { no: 173, symbol: 'P63' },
    { no: 174, symbol: 'P-6' },
    { no: 175, symbol: 'P6/m' },
    { no: 176, symbol: 'P63/m' },
    { no: 177, symbol: 'P622' },
    { no: 178, symbol: 'P6122' },
    { no: 179, symbol: 'P6522' },
    { no: 180, symbol: 'P6222' },
    { no: 181, symbol: 'P6422' },
    { no: 182, symbol: 'P6322' },
    { no: 183, symbol: 'P6mm' },
    { no: 184, symbol: 'P6cc' },
    { no: 185, symbol: 'P63cm' },
    { no: 186, symbol: 'P63mc' },
    { no: 187, symbol: 'P-6m2' },
    { no: 188, symbol: 'P-6c2' },
    { no: 189, symbol: 'P-62m' },
    { no: 190, symbol: 'P-62c' },
    { no: 191, symbol: 'P6/mmm' },
    { no: 192, symbol: 'P6/mcc' },
    { no: 193, symbol: 'P63/mcm' },
    { no: 194, symbol: 'P63/mmc' },
    { no: 195, symbol: 'P23' },
    { no: 196, symbol: 'F23' },
    { no: 197, symbol: 'I23' },
    { no: 198, symbol: 'P213' },
    { no: 199, symbol: 'I213' },
    { no: 200, symbol: 'Pm-3' },
    { no: 201, symbol: 'Pn-3' },
    { no: 202, symbol: 'Fm-3' },
    { no: 203, symbol: 'Fd-3' },
    { no: 204, symbol: 'Im-3' },
    { no: 205, symbol: 'Pa-3' },
    { no: 206, symbol: 'Ia-3' },
    { no: 207, symbol: 'P432' },
    { no: 208, symbol: 'P4232' },
    { no: 209, symbol: 'F432' },
    { no: 210, symbol: 'F4132' },
    { no: 211, symbol: 'I432' },
    { no: 212, symbol: 'P4332' },
    { no: 213, symbol: 'P4132' },
    { no: 214, symbol: 'I4132' },
    { no: 215, symbol: 'P-43m' },
    { no: 216, symbol: 'F-43m' },
    { no: 217, symbol: 'I-43m' },
    { no: 218, symbol: 'P-43n' },
    { no: 219, symbol: 'F-43c' },
    { no: 220, symbol: 'I-43d' },
    { no: 221, symbol: 'Pm-3m' },
    { no: 222, symbol: 'Pn-3n' },
    { no: 223, symbol: 'Pm-3n' },
    { no: 224, symbol: 'Pn-3m' },
    { no: 225, symbol: 'Fm-3m' },
    { no: 226, symbol: 'Fm-3c' },
    { no: 227, symbol: 'Fd-3m' },
    { no: 228, symbol: 'Fd-3c' },
    { no: 229, symbol: 'Im-3m' },
    { no: 230, symbol: 'Ia-3d' },
];

export function getSpaceGroupByNo(no: number) {
    return SpaceGroupList[no - 1];
}

export function useSpaceGroup(defaultNo?: number) {
    const [crystalSystem, setCrystalSystem] = useState(
        CrystalSystemList[getCrystalOrder(defaultNo || 0)] || TriclinicSystem
    );
    const spaceGroupOptions = useMemo(() => {
        return SpaceGroupList.map(({ symbol, no }) => ({
            label: symbol,
            value: no,
        }));
    }, []);

    const setCrystalSystemByNo = useCallback((no: number) => {
        const order = getCrystalOrder(no);
        const system = CrystalSystemList[order] || TriclinicSystem;
        setCrystalSystem(system);
        return system;
    }, []);

    return { crystalSystem, spaceGroupOptions, setCrystalSystemByNo };
}
