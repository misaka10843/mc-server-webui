<script setup lang="ts">
import type { MoeColor } from '../types'
withDefaults(defineProps<{ title: string; color?: MoeColor; announce?: boolean }>(), { color: 'info', announce: false })
</script>
<template><div class="moe-alert" :class="`moe-tone-${color}`" :role="announce ? 'alert' : undefined"><p class="text-sm font-medium" style="color: var(--moe-ink)">{{ title }}</p><div v-if="$slots.default" class="mt-1 text-sm leading-6 text-foreground"><slot /></div><div v-if="$slots.actions" class="mt-3 flex flex-wrap gap-2"><slot name="actions" /></div></div></template>
