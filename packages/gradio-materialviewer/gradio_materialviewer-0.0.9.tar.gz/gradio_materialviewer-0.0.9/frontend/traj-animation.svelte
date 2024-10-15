<svelte:options accessors={true} />

<script lang="ts">
    import { onMount } from "svelte";
    import { ScaleRulerStage } from "./stage";
    import Slider from '@smui/slider';
    import { NumberInput } from 'flowbite-svelte';
    import './index.less';
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
    let containerRef;
    let stageRef;
    let trajStep = 0;
    let isPlaying = false;

    onMount(() => {
        stageRef = new ScaleRulerStage(containerRef!, 20);
        console.log(stageRef, containerRef)
    });
</script>

<div class="material-viewer-traj">
    <div>
        <div class="row" style="font-size: 14px;align-items: center;">
            <!-- Prev -->
            <svg width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 13.263"><rect transform="rotate(180 14 13.263)" x="26.526" y="14" width="1.474" height="11.789" rx=".737" fill="currentColor"/><rect x="28.263" y="13.263" width="2" height="16" rx="1" transform="rotate(180 14.5 12.763)" fill="currentColor"/><path d="M2.67 7.109a.553.553 0 0 1 0-.957l8.845-5.12a.553.553 0 0 1 .83.478v10.241a.553.553 0 0 1-.83.478L2.671 7.11Z" fill-rule="evenodd" fill="currentColor"/></svg>
            {#if isPlaying}
                <!-- Pause -->
                <svg width="1em" height="1em" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 12v24m16-24v24" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {/if}
            {#if !isPlaying}
                <!-- Play -->
                <svg width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 48 48"><path stroke-linejoin="round" stroke-width="4" stroke="currentColor" fill="currentColor" d="m20 12 12 12-12 12V12Z"/></svg>
            {/if}
            <!-- Next -->
            <svg width="1em" height="1em" viewBox="0 0 14 13.263" fill="none" xmlns="http://www.w3.org/2000/svg"><rect fill="currentColor" rx=".737" height="11.789" width="1.474" y=".737" x="12.526"/><rect fill="currentColor" transform="translate(-1 1)" rx="1" height="16" width="2" x="14.263"/><path fill="currentColor" fill-rule="evenodd" d="M11.332 6.153a.553.553 0 0 1 0 .957l-8.844 5.12a.553.553 0 0 1-.83-.478V1.51c0-.426.461-.692.83-.478l8.844 5.12Z"/></svg>
            <NumberInput style="margin-left: 20px" bind:value={trajStep} step={1} min={0} max={20} />
        </div>
    </div>
    <div bind:this={containerRef} class="material-viewer-traj-axis" />
    <div class="material-viewer-traj-slider">
        <Slider min={0} max={20} step={1} style="flex: 1;" bind:value={trajStep} />
    </div>
</div>

<style>
    .row {
        display: flex;
        flex-flow: row wrap;
    }
    .material-viewer-traj {
        position: absolute;
        width: 100%;
        bottom: 24px;
        color: black; 
    }
    .material-viewer-traj-axis {
        position: relative;
        bottom: -24px;
    }
    .material-viewer-traj-slider {
        width: calc(100% - 28px);
        display: flex;
        margin: 0 14px;
    }
</style>
