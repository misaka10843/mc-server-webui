<script setup lang="ts">
import { useId } from 'vue'
import { SliderRoot, SliderTrack, SliderRange, SliderThumb } from 'reka-ui'
withDefaults(defineProps<{ label: string; min?: number; max?: number; step?: number; disabled?: boolean; name?: string; showValue?: boolean }>(), { min: 0, max: 100, step: 1 })
const model = defineModel<number[]>({ default: () => [50] })
const id = useId()
</script>
<template><div class="moe-field"><div class="flex justify-between gap-4"><span :id="id" class="moe-label">{{ label }}</span><span v-if="showValue" class="text-sm tabular-nums text-muted">{{ model.join(' – ') }}</span></div><SliderRoot v-model="model" :min="min" :max="max" :step="step" :disabled="disabled" :name="name" class="moe-slider"><SliderTrack class="moe-slider-track"><SliderRange class="moe-slider-range" /></SliderTrack><SliderThumb v-for="(_, index) in model" :key="index" class="moe-slider-thumb moe-focus" :aria-label="model.length > 1 ? `${label} ${index + 1}` : label" /></SliderRoot></div></template>
