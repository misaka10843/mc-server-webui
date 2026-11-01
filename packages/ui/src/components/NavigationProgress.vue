<script setup lang="ts">
import { computed } from 'vue'
const props = withDefaults(defineProps<{ active: boolean; value?: number; label: string; error?: boolean }>(), { value: 0, error: false })
const fraction = computed(() => Number.isFinite(props.value) ? Math.min(100, Math.max(0, props.value)) / 100 : 0)
</script>
<template><div v-show="active" class="moe-navigation-progress" :data-error="error" role="progressbar" :aria-label="label"><span :style="{ transform: `scaleX(${fraction})` }" /></div></template>
