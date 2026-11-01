<script setup lang="ts">
import type { MoeNavItem } from '../types'
import Icon from './Icon.vue'
defineProps<{ item: MoeNavItem; active?: boolean; compact?: boolean }>()
defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
</script>

<template>
  <component :is="item.disabled ? 'span' : 'a'" :href="item.disabled ? undefined : item.href" :aria-current="active ? 'page' : undefined" :aria-disabled="item.disabled || undefined" :title="compact ? item.label : undefined" class="moe-nav-item moe-focus" :data-active="active" :data-compact="compact" @click="!item.disabled && $emit('navigate', $event, item)">
    <slot name="icon"><Icon v-if="item.icon" :name="item.icon" class="size-4" /></slot>
    <span class="moe-nav-label" :class="{ 'sr-only': compact }">{{ item.label }}</span>
    <span v-if="item.badge && !compact" class="moe-nav-count">{{ item.badge }}</span>
  </component>
</template>
