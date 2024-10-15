import { ASEDataItem, AtomParams, LatticeParams, MaterialCleave, MaterialItem } from '../model';
import {
    ase2Material,
    bulk2Material,
    createOriginalMaterial,
    createSymmetryMaterial,
    getCleavageSurf,
    getParamsFromSymmetryMaterial,
    material2Ase,
    material2Bulk,
} from '../utils/utils';
import { Bulk } from '../utils/bulk';

export class SimpleMaterialCore {
    origin: MaterialItem;
    cleave?: MaterialCleave;

    toMaterialCore() {
        const core = new MaterialCore();
        core.setByOriginMaterial(this.origin);
        if (this.cleave) {
            core.setCleave(this.cleave);
        }
        return core;
    }

    constructor(
        origin: MaterialItem,
        params?: {
            cleave?: MaterialCleave;
        }
    ) {
        this.origin = JSON.parse(JSON.stringify(origin));
        if (params?.cleave) {
            this.cleave = JSON.parse(JSON.stringify(params.cleave));
        }
    }
}

export class MaterialCore {
    origin?: MaterialItem;
    symmetry?: MaterialItem;
    // expands?: MaterialItem[]

    prevOrigin?: MaterialItem;
    cleave?: MaterialCleave;
    surface?: Bulk;

    setByParams(params: { lattice?: LatticeParams; atoms: AtomParams[] }) {
        this.origin = createOriginalMaterial(params);
        this.symmetry = createSymmetryMaterial(this.origin);
    }

    setByOriginMaterial(origin: MaterialItem) {
        this.origin = origin;
        this.symmetry = createSymmetryMaterial(this.origin);
    }

    setByBulk(bulk: Bulk) {
        this.origin = bulk2Material(bulk);
        this.setByOriginMaterial(this.origin);
    }

    setByASE(ase: ASEDataItem) {
        this.origin = ase2Material(ase);
        this.setByOriginMaterial(this.origin);
    }

    setCleave(cleave: MaterialCleave) {
        this.cleave = cleave;
        this.surface = getCleavageSurf(cleave, this.origin!);
        this.prevOrigin = this.prevOrigin || this.origin;
        this.setByBulk(this.surface!);
    }

    convertOrigin(convert: (origin: MaterialItem) => MaterialItem) {
        if (!this.origin) {
            return;
        }
        const newOrigin = convert(this.origin);
        this.setByOriginMaterial(newOrigin);
    }

    getMoleculeParam() {
        if (!this.symmetry) {
            return;
        }
        return getParamsFromSymmetryMaterial(this.symmetry);
    }

    getBulk() {
        if (!this.origin) {
            return;
        }
        return material2Bulk(this.origin);
    }

    getAse() {
        if (!this.origin) {
            return;
        }
        return material2Ase(this.origin);
    }

    getSimple() {
        if (!this.origin) {
            return;
        }
        return new SimpleMaterialCore(this.origin, {
            cleave: this.cleave,
        });
    }

    constructor(ase?: ASEDataItem) {
        if (ase) {
            this.setByASE(ase);
        }
    }
}
