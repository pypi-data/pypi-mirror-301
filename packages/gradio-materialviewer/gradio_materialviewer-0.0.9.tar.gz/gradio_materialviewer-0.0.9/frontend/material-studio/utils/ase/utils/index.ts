export function pbc2pbc(pbc: boolean[]): boolean[] {
    let newpbc: boolean[] = new Array<boolean>(3);

    for (let i = 0; i < 3; i++) {
        newpbc[i] = pbc[i];
    }

    return newpbc;
}
