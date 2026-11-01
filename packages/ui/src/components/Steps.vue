<script setup lang="ts">
import type { MoeOption } from '../types'
import Icon from './Icon.vue'
defineProps<{ label: string; items: MoeOption[]; current: string }>()
</script>
<template><ol :aria-label="label" class="moe-steps"><li v-for="(item, index) in items" :key="item.value" :aria-current="current === item.value ? 'step' : undefined" :data-complete="index < items.findIndex(entry => entry.value === current)"><span class="moe-step-marker"><Icon v-if="index < items.findIndex(entry => entry.value === current)" name="check" class="size-4" /><template v-else>{{ index + 1 }}</template></span><span><span class="block text-sm font-medium">{{ item.label }}</span><span v-if="item.description" class="moe-description">{{ item.description }}</span></span></li></ol></template>
