<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { StatusTracker } from "@gradio/statustracker";
	import { tick } from "svelte";
	import Viewer from './viewer.svelte'

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let materialFile = "";
	export let label = "Textbox";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let placeholder = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let interactive: boolean;
	export let rtl = false;
	export let height;
	export let style;
	export let latticeInfoVisible;

	window.process = {
		env: {
			NODE_ENV: "production",
			LANG: "",
		},
	};

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
	// function hexToColorString(hex) {
	// 	let hexString = hex.toString(16);
		
	// 	while (hexString.length < 6) {
	// 		hexString = '0' + hexString;
	// 	}

	// 	return '#' + hexString;
	// }
	// let atomList = [];
	// async function loadFile() {
	// 	if (!lightPlugin.canvas3d) return;
	// 	const [ref] =
	// 		await lightPlugin.managers.representation.createMolecular({
	// 			format: Format.Material,
	// 			reprType: RepresentationType.BallAndStick,
	// 			data: aseToMaterial(JSON.parse(materialFile)),
	// 			theme: {
	// 				[ThemeC.ATOM]: {
	// 					color: {
	// 						name: 'material-element-symbol',
	// 					}
	// 				}
	// 			}
	// 		});
	// 	const atomSet = new Set();
	// 	await LightPlugin.Utils.traverseAtoms(ref, atom => {
	// 		atomSet.add(atom.typeSymbol);
	// 	});
	// 	atomList = new Array(...atomSet.values())
		
	// 	// 创建晶胞
	// 	lightPlugin.managers.representation.createOther({
	// 		data: lightPlugin.managers.cell.getUnitCellData(ref),
	// 		type: RepresentationType.UnitCell,
	// 	});
	// 	// 更新axes(不传ref即为恢复axes)
	// 	lightPlugin.managers.camera.updateAxes(ref);
	// }
	// const aseToMaterial = (aseData: any) => {
	// 	const { angle, atoms, length } = aseData[0];
	// 	const [a, b, c] = length;
	// 	const [alpha, beta, gamma] = angle;
	// 	const res = {
	// 		elements: [],
	// 		xyzs: [],
	// 		lattice: {
	// 			a,
	// 			b,
	// 			c,
	// 			alpha,
	// 			beta,
	// 			gamma,
	// 		},
	// 	};
	// 	atoms.forEach((atom) => {
	// 		const { cart_coord, formula } = atom;
	// 		res.elements.push(formula);
	// 		res.xyzs.push(cart_coord);
	// 	});
	// 	return res;
	// };

	// function init(): void {
	// 	lightPlugin.managers.representation.showPolarHydrogenOnly = false;
	// 	// 修改光照及hover select颜色
	// 	lightPlugin.createCanvas(
	// 		document.getElementById("material-viewer-canvas"),
	// 		{
	// 			renderer: {
	// 				ambientIntensity: 0.4,
	// 				backgroundColor: Color(0xf2f5fa),
	// 			},
	// 		},
	// 	);
	// 	lightPlugin.managers.selection.structure.setGranularity(
	// 		Granularity.Atom,
	// 	);
	// 	lightPlugin.managers.events.setAllowSelect(false);
	// 	lightPlugin.managers.highlight.info.subscribe(
	// 		(data) => {
	// 			if (data.info?.granularity === Granularity.Atom) {
	// 				const { atomName, x, y, z } = data.info;
	// 				tooltipText = `${atomName} (${[x, y, z].map((i) => i.toFixed(3)).join(", ")})`;
	// 			} else {
	// 				tooltipText = "";
	// 			}
	// 		},
	// 	);
	// 	// @ts-ignore
	// 	// eslint-disable-next-line no-underscore-dangle
	// 	window.__material_viewer = lightPlugin;
	// 	setTimeout(() => lightPlugin.refresh(), 50);
	// }
	// const interval = setInterval(() => {
	// 	if (
	// 		document.getElementById("material-viewer-canvas") &&
	// 		!lightPlugin.canvas3d
	// 	) {
	// 		clearInterval(interval);
	// 		init();
	// 		loadFile();
	// 	}
	// }, 1000);

	// function updateFile() {
	// 	lightPlugin.clear();
	// 	loadFile();
	// }
	// $: materialFile, updateFile()

	// const resize = () => {
	// 	setTimeout(() => {
	// 		lightPlugin.refresh({ fixCamera: true });
	// 	}, 0)
	// }
	// $: height, resize()
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
{#if loading_status}
	<StatusTracker
		autoscroll={gradio.autoscroll}
		i18n={gradio.i18n}
		{...loading_status}
		on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
	/>
{/if}
{#if visible}
<div class="material-viewer-index-container" style={`height: ${height}px;`}>
	<Viewer
		gradio={gradio}
		materialFile={materialFile}
		value={value}
		{value_is_output}
		{height}
		{style}
		{latticeInfoVisible}
	/>
</div>
{/if}
</Block>

<style>
	label {
		display: block;
		width: 100%;
	}
	.material-viewer-index-container {
        width: 100%;
        height: 100%;
        position: relative;
        min-height: 240px;
	}
	#material-viewer-canvas {
		width: 100%;
		height: 100%;
		min-height: 240px;
	}

	.tooltip {
		position: absolute;
	}

	.tooltip-inner {
		position: relative;
		left: -50%;
		padding: 2px 4px;
		font-size: 12px;
		color: #fff;
		background-color: #020c1a;
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
	}

	.atom-model-legend-item-ball {
		margin-right: 8px;
		width: 8px;
		height: 8px;
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
        box-shadow: 0 6px 10px rgba(183, 192, 231, .1), 0 8px 12px 1px rgba(170, 181, 223, .05);
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
        color: #555878
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
