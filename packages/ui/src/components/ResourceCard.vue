<script setup lang="ts">
defineProps<{ title: string; description?: string; identifier: string; href: string; linkLabel: string }>()
defineEmits<{ navigate: [event: MouseEvent] }>()
</script>
<template><a :href="href" :aria-label="linkLabel" class="moe-resource-card moe-focus" @click="$emit('navigate', $event)"><div class="flex items-start justify-between gap-3"><h2 class="min-w-0 text-base font-semibold break-words">{{ title }}</h2><div class="flex shrink-0 flex-wrap gap-2"><slot name="badges" /></div></div><p v-if="description" class="mt-2 line-clamp-2 text-sm text-muted">{{ description }}</p><code class="mt-3 block truncate text-xs text-muted">{{ identifier }}</code><div class="moe-resource-card-footer"><slot /></div></a></template>
