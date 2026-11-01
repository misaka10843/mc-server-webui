<script setup lang="ts">
import Card from './Card.vue'
import CopyButton from './CopyButton.vue'
defineProps<{ title: string; description?: string; identifier: string; items: { key: string; label: string; value: string }[]; copyLabel: string; copiedLabel: string; errorLabel: string }>()
</script>
<template><Card padding="lg" class="moe-resource-summary"><div class="moe-resource-summary-heading"><div class="min-w-0"><div class="flex flex-wrap items-center gap-2"><h2 class="text-lg font-semibold break-words">{{ title }}</h2><slot name="badges" /></div><p v-if="description" class="mt-1 text-sm text-muted break-words">{{ description }}</p><div class="moe-resource-identifier"><code>{{ identifier }}</code><CopyButton :value="identifier" :label="copyLabel" :copied-label="copiedLabel" :error-label="errorLabel" /></div></div><div class="flex min-w-0 max-w-full flex-wrap gap-2"><slot name="actions" /></div></div><slot /><dl class="moe-resource-facts"><div v-for="item in items" :key="item.key"><dt>{{ item.label }}</dt><dd>{{ item.value }}</dd></div></dl></Card></template>
