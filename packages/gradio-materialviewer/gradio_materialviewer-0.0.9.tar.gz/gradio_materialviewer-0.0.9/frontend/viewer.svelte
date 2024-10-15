<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";
	import {
		Format,
		Granularity,
		LightPlugin,
		RepresentationType,
		ThemeC,
		VESTA_COLOR_TABLE,
		traverseAtoms,
		Vec3,
		AtomReprType,
	} from "dpmol";
	import { getParamsFromSymmetryMaterial, ase2Material, getVertexByVectors, getPointsByVertex, createSymmetryMaterial } from './material-studio/utils/utils'
    import { Lattice } from "./material-studio/model";
    import { Bulk } from "./material-studio/utils/bulk";
	import { debounce } from 'lodash';
    import TrajAnimation from "./traj-animation.svelte";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let materialFile = "";
	export let value = "";
	export let value_is_output = false;
	export let height;
	export let style;
	export let latticeInfoVisible;

	window.process = {
		env: {
			NODE_ENV: "production",
			LANG: "",
		},
	};

	let lightPlugin = new LightPlugin();

	const guid = () => {
		function S4() {
			// eslint-disable-next-line no-bitwise
			return (((1 + Math.random()) * 0x10000) | 0)
				.toString(16)
				.substring(1);
		}
		return `${S4() + S4()}-${S4()}-${S4()}-${S4()}-${S4()}${S4()}${S4()}`;
	};
	const key = guid();
	$: key;

	let el: HTMLTextAreaElement | HTMLInputElement;
	const container = true;

	function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			gradio.dispatch("submit");
		}
	}

	$: if (value === null) value = "";

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value, handle_change();

	let mousePosition = { x: -1000, y: -1000 };
	$: mousePosition;

	let tooltipText = "";
	$: tooltipText;

	let lattice;
	$: lattice;
	let isTraj = false;
	function hexToColorString(hex) {
		let hexString = hex.toString(16);

		while (hexString.length < 6) {
			hexString = "0" + hexString;
		}

		return "#" + hexString;
	}
	let atomList = [];

	const renderCell =async (lattice?: any, surface?: any) => {
        if (!lattice) {
            return;
        }

        if (!surface) {
            const vertex = getVertexByVectors(lattice.matrix!);
            const points = getPointsByVertex(vertex);

            return lightPlugin!.managers.representation.createOther({
                data: points,
                type: RepresentationType.CustomLines,
                params: {
                    alpha: 1,
                },
            });
        }

        const vertex = getVertexByVectors(surface.getCell());
        const points = getPointsByVertex(vertex);
        const solidPoints = points.slice(0, 4);

        return lightPlugin!.managers.representation.createOther({
            data: solidPoints,
            type: RepresentationType.CustomLines,
            params: {
                alpha: 1,
            },
        });
    };

	const setAxes = (lattice?: Lattice, surface?: Bulk) => {
        const defaultParams = {
            vecA: Vec3.unitX,
            vecB: Vec3.unitY,
            vecC: Vec3.unitZ,
        };

        const params = (() => {
            if (!lattice) {
                return {};
            }
            const cell = surface?.getCell() || lattice.matrix;
            return {
                vecA: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[0] as [number, number, number])),
                vecB: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[1] as [number, number, number])),
                vecC: Vec3.normalize(Vec3.zero(), Vec3.create.apply(null, cell[2] as [number, number, number])),
            };
        })();

        return lightPlugin?.canvas3d?.setProps({
            camera: {
                helper: {
                    axes: {
                        name: 'on',
                        params: {
                            ...defaultParams,
                            ...params,
                        },
                    },
                },
            },
        });
    };

	async function loadFile() {
		if (!lightPlugin.canvas3d) return;
		const data = getParamsFromSymmetryMaterial(
			createSymmetryMaterial(
				ase2Material(JSON.parse(materialFile)[0]),
			),
		);
		const [ref] = await lightPlugin.managers.representation.createMolecular(
			{
				format: Format.Material,
				reprType: AtomReprType.has(style) ? style : RepresentationType.BallAndStick,
				data: data as any,
				theme: {
					[ThemeC.ATOM]: {
						color: {
							name: "material-element-symbol",
						},
					},
				},
			},
		);
		const atomSet = new Set();
		const structure = await lightPlugin.managers.cell.getStructure(ref);
		if (!structure) return;
		traverseAtoms(structure, (atom) => {
			atomSet.add(atom.typeSymbol);
		});
		atomList = new Array(...atomSet.values());

		// 创建晶胞
		renderCell(data.lattice);
		// 更新axes
		setAxes(data.lattice);
		lattice = data.lattice;
	}
	function init(): void {
		lightPlugin.managers.representation.showPolarHydrogenOnly = false;
		// 修改光照及hover select颜色
		lightPlugin.createCanvas(
			document.getElementById(`material-viewer-canvas-${key}`)
		);
		lightPlugin.managers.selection.structure.setGranularity(
			Granularity.Atom,
		);
		lightPlugin.managers.events.setAllowSelect(false);
		lightPlugin.managers.highlight.info.subscribe((data) => {
			if (data.info?.granularity === Granularity.Atom) {
				const { atomName, x, y, z } = data.info;
				tooltipText = `${atomName} (${[x, y, z].map((i) => i.toFixed(3)).join(", ")})`;
			} else {
				tooltipText = "";
			}
		});

        let observer = new ResizeObserver(
            debounce(() => {
                lightPlugin.refresh({ fixCamera: true });
            }, 300)
        );
        observer.observe(document.getElementById(`material-viewer-canvas-${key}`));
		// @ts-ignore
		// eslint-disable-next-line no-underscore-dangle
		window.__material_viewer = lightPlugin;
		setTimeout(() => lightPlugin.refresh(), 50);
	}
	const interval = setInterval(() => {
		if (
			!!document.getElementById(`material-viewer-canvas-${key}`)
				?.clientHeight &&
			!lightPlugin.canvas3d
		) {
			clearInterval(interval);
			init();
			loadFile();
		}
	}, 500);

	function updateFile() {
		if (!lightPlugin.canvas3d) return;
		lightPlugin.clear();
		loadFile();
	}
	$: materialFile, updateFile();

	$: style, updateFile();
	const resize = () => {
		setTimeout(() => {
			lightPlugin.refresh({ fixCamera: true });
		}, 0);
	};
	$: height, resize();
</script>

<div class="material-viewer-container" style={`height: ${height}px;`}>
	<div
		id={`material-viewer-canvas-${key}`}
		style={"width: 100%;height: 100%;min-height: 240px;"}
		on:mousemove={(e) => {
			mousePosition = {
				x: e.offsetX,
				y: e.offsetY,
			};
		}}
	></div>
	{#if !!tooltipText}
		<div
			class="tooltip"
			style={`top: ${mousePosition.y - 45}px;left: ${mousePosition.x - 8}px;`}
		>
			<div class={"tooltip-inner"}>{tooltipText}</div>
		</div>
	{/if}
	{#if latticeInfoVisible && !!lattice}
		<div class="lattice-content">
			<h6 style="font-weight: 600;">Lattice</h6>
			<div class="lattice-params">
				<div class="lattice-params-half">
					{#each ['a', 'b', 'c'] as key}
						<div class="lattice-params-item">
							<span class="text-color-tertiary" style="margin-right: 8px;">{key}</span>
							<span>{lattice[key].toFixed(3)}(Å)</span>
						</div>
					{/each}
				</div>
				<div class="lattice-params-half">
					{#each ['α', 'β', 'γ'] as key, idx}
						<div class="lattice-params-item">
							<span class="text-color-tertiary" style="margin-right: 8px;">{key}</span>
							<span>{lattice[['alpha', 'beta', 'gamma'][idx]].toFixed(3)}°</span>
						</div>
					{/each}
				</div>
			</div>

			<div class={'row'} style="justify-content: space-between;margin-top: 8px;">
				<span class={`text-color-tertiary mr-16`}>Volume</span>
				<span>{lattice.volume.toFixed(3)}(Å3)</span>
			</div>
			<div class={'row'} style="justify-content: space-between;">
				<span class={`text-color-tertiary mr-16`}>Space Group</span>
				<span>
					{lattice.spacegroup.symbol}({lattice.spacegroup.no})
				</span>
			</div>
		</div>
	{/if}
	<div class={"atom-model-legend-container"}>
		{#each atomList as atom}
			<div class={"atom-model-legend-item"}>
				<div
					style={`background-color: ${hexToColorString(VESTA_COLOR_TABLE[atom.toUpperCase()])}`}
					class={"atom-model-legend-item-ball"}
				/>
				{atom}
			</div>
		{/each}
	</div>
	<div class="material-viewer-toolbar">
		<button
			class="material-viewer-toolbar-btn"
			on:click={() => lightPlugin.managers.camera.zoomIn()}
		>
			<svg
				width="1em"
				height="1em"
				viewBox="0 0 16 16"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M8.02 3.334l-.012 9.333M3.336 8h9.333"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
		<button
			class="material-viewer-toolbar-btn"
			on:click={() => lightPlugin.managers.camera.zoomOut()}
		>
			<svg
				width="1em"
				height="1em"
				viewBox="0 0 16 16"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M3.336 8h9.333"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
		<button
			class="material-viewer-toolbar-btn"
			on:click={() => lightPlugin.managers.camera.reset()}
		>
			<svg
				width="1em"
				height="1em"
				viewBox="0 0 16 16"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M8.0026 14.6673C11.6845 14.6673 14.6693 11.6825 14.6693 8.00065C14.6693 4.31875 11.6845 1.33398 8.0026 1.33398C4.32071 1.33398 1.33594 4.31875 1.33594 8.00065C1.33594 11.6825 4.32071 14.6673 8.0026 14.6673Z"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M8 12.334V14.6673"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M12 8H14.6667"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M1.33594 8H3.66927"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M8 3.66732V1.33398"
					stroke="#A2A5C4"
					stroke-width="1.3"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<circle cx="8" cy="8" r="1" stroke="#A2A5C4" />
			</svg>
		</button>
	</div>
	{#if isTraj}
		<TrajAnimation />
	{/if}
</div>

<style>
	label {
		display: block;
		width: 100%;
	}

	.tooltip {
		position: absolute;
	}

	.tooltip-inner {
		pointer-events: none;
		position: relative;
		left: -50%;
		padding: 8px 12px;
		font-size: 16px;
		color: #fff;
		background-color: rgba(0,0,0,0.8);
		border-radius: 4px;
	}

	.tooltip-inner::after {
		position: absolute;
		bottom: -3px;
		left: 50%;
		width: 6px;
		height: 6px;
		background-color: #020c1a;
		content: " ";
		transform: rotate(45deg);
		transform-origin: center center;
	}

	.atom-model-legend-container {
		position: absolute;
		top: 12px;
		right: 12px;
		display: flex;
		max-width: 200px;
		flex-wrap: wrap;
		gap: 8px 16px;
	}

	.atom-model-legend-item {
		display: flex;
		align-items: center;
		color: black;
		font-size: 14px;
	}

	.atom-model-legend-item-ball {
		margin-right: 8px;
		width: 14px;
		height: 14px;
		border-radius: 50%;
	}

	.material-viewer-container {
		width: 100%;
		height: 100%;
		position: relative;
		min-height: 240px;
	}

	.material-viewer-toolbar {
		position: absolute;
		right: 12px;
		top: 50%;
		transform: translateY(-50%);
		display: flex;
		flex-direction: column;
		color: #000000;

		background: #ffffff;
		box-shadow:
			0 6px 10px rgba(183, 192, 231, 0.1),
			0 8px 12px 1px rgba(170, 181, 223, 0.05);
		border-radius: 4px;
		padding: 4px;
		margin-bottom: 8px;
	}
	.material-viewer-toolbar-btn {
		cursor: pointer;
		font-size: 16px;
		height: 16px;
		width: 16px;
		margin-bottom: 4px;
	}
	.material-viewer-toolbar-btn:hover {
		cursor: pointer;
		color: #555878;
	}

	.lattice-content {
		position: absolute;
		top: 48px;
		right: 12px;
		z-index: 11;
		color: #000000;
	}

	.lattice-params {
		display: flex;
		justify-content: space-between;
	}

	.lattice-params-item {
		margin-top: 8px;
		width: 784x;
		line-height: 16px;
	}
	.text-color-tertiary {
		color: #70749e;
	}
    .row {
        display: flex;
        flex-flow: row wrap;
    }
	input {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	.container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	}
	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}
</style>
