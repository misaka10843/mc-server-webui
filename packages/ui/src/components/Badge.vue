<script setup lang="ts">
import type { MoeColor } from '../types'
withDefaults(defineProps<{ color?: MoeColor; variant?: 'flat' | 'solid' | 'bordered' }>(), { color: 'default', variant: 'flat' })
</script>
<template><span class="moe-badge" :class="`moe-tone-${color}`" :data-variant="variant"><slot /></span></template>
