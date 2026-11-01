<script setup lang="ts">
import CopyButton from './CopyButton.vue'
defineProps<{ label: string; value: string; warning: string; copyLabel: string; copiedLabel: string; errorLabel: string }>()
</script>
<template><section class="grid gap-3" :aria-label="label"><p class="text-sm text-muted">{{ warning }}</p><div class="flex items-start justify-between gap-3 rounded-xl border border-line p-4"><pre class="min-w-0 whitespace-pre-wrap break-all text-sm">{{ value }}</pre><CopyButton :value="value" :label="copyLabel" :copied-label="copiedLabel" :error-label="errorLabel" /></div></section></template>
