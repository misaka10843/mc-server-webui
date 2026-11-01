<script setup lang="ts">
defineProps<{ label: string }>()
</script>
<template><span role="status" class="inline-flex items-center gap-2 text-sm text-muted"><span class="moe-spinner" aria-hidden="true" /><span>{{ label }}</span></span></template>
