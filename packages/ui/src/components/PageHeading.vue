<script setup lang="ts">
withDefaults(defineProps<{ title: string; description?: string; eyebrow?: string; headingLevel?: 'h1' | 'h2' | 'h3' }>(), { headingLevel: 'h1' })
</script>
<template><div class="moe-page-heading"><div class="flex min-w-0 items-start gap-3"><slot name="leading" /><div class="min-w-0"><p v-if="eyebrow" class="moe-auth-eyebrow mb-2">{{ eyebrow }}</p><component :is="headingLevel" class="break-words text-2xl font-semibold tracking-tight">{{ title }}</component><p v-if="description" class="mt-3 text-sm leading-7 text-muted">{{ description }}</p></div></div><div v-if="$slots.actions" class="flex shrink-0 flex-wrap gap-2"><slot name="actions" /></div></div></template>
