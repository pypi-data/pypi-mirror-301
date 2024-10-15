export class StateUnit<T> {
    state!: T;

    setState: (state: Partial<T>) => void = state => {
        state = [...this.beforeSetState].reduce((s, fnB) => fnB(s), state);
        this.state = {
            ...this.state,
            ...state,
        };
        this.onSetState.forEach(fn => fn(this.state));
    };

    staticSetState: (state: Partial<T>) => void = state => {
        this.state = {
            ...this.state,
            ...state,
        };
    };

    beforeSetState = new Set<(state: Partial<T>) => Partial<T>>();

    onSetState = new Set<(state: T) => void>();

    subscribeBeforeSetState = (fn: (state: Partial<T>) => Partial<T>) => {
        this.beforeSetState.add(fn);
        const unsubscribe = () => this.beforeSetState.delete(fn);
        return unsubscribe;
    };

    subscribe = (fn: (state: T) => void) => {
        this.onSetState.add(fn);
        const unsubscribe = () => this.onSetState.delete(fn);
        return unsubscribe;
    };

    forceUpdate() {
        this.setState({});
    }
}
