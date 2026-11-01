<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ label: string; missingLabel: string; partialLabel: string; points: { day: string; value?: number; partial?: boolean }[] }>()
const maximum = computed(() => Math.max(1, ...props.points.map(point => point.value ?? 0)))
const barStyle = (point: typeof props.points[number]) => ({
  height: point.value === undefined ? '100%' : `${Math.max(1, point.value / maximum.value * 100)}%`,
  background: point.value === undefined ? 'repeating-linear-gradient(135deg, transparent, transparent 4px, var(--moe-line) 4px, var(--moe-line) 5px)' : 'var(--moe-primary)',
  opacity: point.partial ? 0.55 : 1,
})
</script>
<template><figure class="grid gap-4" :aria-label="label"><figcaption class="font-semibold">{{ label }}</figcaption><div class="flex h-52 items-end gap-1 border-b border-line" role="img" :aria-label="label"><div v-for="point in points" :key="point.day" class="flex h-full min-w-0 flex-1 items-end" :title="`${point.day}: ${point.value ?? missingLabel}${point.partial ? ` · ${partialLabel}` : ''}`"><div class="w-full rounded-t-sm" :style="barStyle(point)" /></div></div><div class="flex justify-between text-xs text-muted"><span>{{ points[0]?.day }}</span><span>{{ maximum }}</span><span>{{ points.at(-1)?.day }}</span></div><details class="text-sm"><summary class="cursor-pointer">{{ label }}</summary><table class="w-full text-left"><tbody><tr v-for="point in points" :key="point.day"><th class="py-1 font-normal">{{ point.day }}</th><td>{{ point.value ?? missingLabel }} {{ point.partial ? `(${partialLabel})` : '' }}</td></tr></tbody></table></details></figure></template>
