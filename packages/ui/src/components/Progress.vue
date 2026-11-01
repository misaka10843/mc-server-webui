<script setup lang="ts">
import { computed } from 'vue'
import { ProgressRoot, ProgressIndicator } from 'reka-ui'
import type { MoeColor } from '../types'
const props = withDefaults(defineProps<{ label: string; value?: number | null; max?: number; color?: MoeColor; showValue?: boolean }>(), { value: null, max: 100, color: 'primary' })
const percent = computed(() => props.value == null ? 0 : Math.min(100, Math.max(0, props.value / props.max * 100)))
</script>
<template><div class="grid gap-2"><div class="flex justify-between gap-4 text-sm"><span>{{ label }}</span><span v-if="showValue && value != null" class="tabular-nums text-muted">{{ Math.round(percent) }}%</span></div><ProgressRoot :model-value="value" :max="max" :aria-label="label" class="moe-progress" :class="`moe-tone-${color}`"><ProgressIndicator class="moe-progress-fill" :style="value == null ? undefined : { transform: `translateX(-${100 - percent}%)` }" /></ProgressRoot></div></template>
