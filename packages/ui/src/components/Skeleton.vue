<script setup lang="ts">
withDefaults(defineProps<{ shape?: 'line' | 'avatar' | 'block' }>(), { shape: 'line' })
</script>
<template><div aria-hidden="true" class="moe-skeleton" :class="{ 'h-4 w-full': shape === 'line', 'size-11 rounded-full': shape === 'avatar', 'h-28 w-full': shape === 'block' }" /></template>
