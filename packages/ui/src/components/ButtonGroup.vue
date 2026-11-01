<script setup lang="ts">
defineProps<{ label: string }>()
</script>
<template><div role="group" :aria-label="label" class="moe-button-group"><slot /></div></template>
