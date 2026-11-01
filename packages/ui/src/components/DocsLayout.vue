<script setup lang="ts">
import type { MoeNavGroup, MoeNavItem } from '../types'
import NavItem from './NavItem.vue'
defineProps<{ label: string; groups: MoeNavGroup[]; active?: string }>()
defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
</script>
<template><div class="moe-docs-layout"><details v-if="$slots.navigation" class="moe-docs-mobile-navigation"><summary class="moe-focus">{{ label }}</summary><slot name="navigation" /></details><aside class="moe-docs-sidebar"><slot name="navigation"><nav :aria-label="label"><div v-for="group in groups" :key="group.label" class="grid gap-1"><p class="moe-console-section">{{ group.label }}</p><NavItem v-for="item in group.items" :key="item.id" :item="item" :active="item.id === active" @navigate="(event, entry) => $emit('navigate', event, entry)" /></div></nav></slot></aside><div class="moe-docs-content"><div v-if="$slots.actions" class="moe-docs-actions"><slot name="actions" /></div><slot /></div></div></template>
