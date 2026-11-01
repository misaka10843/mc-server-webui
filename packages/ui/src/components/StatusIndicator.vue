<script setup lang="ts">
withDefaults(defineProps<{ label: string; state?: 'positive' | 'negative' | 'pending'; announce?: boolean }>(), { state: 'pending' })
</script>
<template><span class="moe-status-indicator" :data-state="state" :role="announce ? 'status' : undefined"><span aria-hidden="true" />{{ label }}</span></template>
