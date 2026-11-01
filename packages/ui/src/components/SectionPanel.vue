<script setup lang="ts">
import Card from './Card.vue'
defineProps<{ title: string; description?: string }>()
</script>
<template><section class="moe-section-panel"><header class="moe-section-panel-heading"><div class="min-w-0"><h2 class="text-lg font-semibold">{{ title }}</h2><p v-if="description" class="mt-1 text-sm text-muted">{{ description }}</p></div><div v-if="$slots.actions" class="flex shrink-0 flex-wrap gap-2"><slot name="actions" /></div></header><Card padding="lg"><slot /></Card></section></template>
