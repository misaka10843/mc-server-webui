<script setup lang="ts">
import HttpMethod from './HttpMethod.vue'
defineProps<{ label: string; items: { id: string; method: string; path: string; title: string; href: string }[]; emptyLabel: string }>()
defineEmits<{ navigate: [event: MouseEvent, item: { id: string; href: string }] }>()
</script>
<template><ul class="moe-endpoint-list" :aria-label="label"><li v-for="item in items" :key="item.id"><a :href="item.href" class="moe-endpoint-link moe-focus" @click="$emit('navigate', $event, item)"><HttpMethod :method="item.method" /><span class="min-w-0"><code class="moe-endpoint-path">{{ item.path }}</code><span class="moe-endpoint-title">{{ item.title }}</span></span><span aria-hidden="true" class="text-muted">›</span></a></li><li v-if="!items.length" class="p-6 text-sm text-muted">{{ emptyLabel }}</li></ul></template>
