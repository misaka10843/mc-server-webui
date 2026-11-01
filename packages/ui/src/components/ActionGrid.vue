<script setup lang="ts">
import type { MoeNavItem } from '../types'
import Icon from './Icon.vue'
defineProps<{ items: MoeNavItem[] }>()
defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
</script>
<template><div class="moe-action-grid"><a v-for="item in items" :key="item.id" :href="item.href" class="moe-action-link moe-focus" @click="$emit('navigate', $event, item)"><Icon v-if="item.icon" :name="item.icon" class="shrink-0 text-primary" /><span>{{ item.label }}</span></a></div></template>
