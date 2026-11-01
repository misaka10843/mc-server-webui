<script setup lang="ts">
import { useId } from 'vue'
import type { MoeNavGroup, MoeNavItem } from '../types'
import NavItem from './NavItem.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; groups: MoeNavGroup[]; active?: string; collapsible?: boolean; collapseLabel?: string; expandLabel?: string; title?: string; footerText?: string; layout?: 'panel' | 'rail' }>(), { collapseLabel: '收起侧栏', expandLabel: '展开侧栏', layout: 'panel' })
const collapsed = defineModel<boolean>('collapsed', { default: false })
defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
const id = useId()
</script>

<template>
  <aside class="moe-sidebar" :data-collapsed="collapsed" :data-layout="layout">
    <div v-if="$slots.header || title || collapsible" class="moe-sidebar-heading"><span v-if="layout === 'rail'" class="moe-sidebar-brand" aria-hidden="true"><slot name="brand-icon">M</slot></span><div v-if="!collapsed" class="min-w-0 flex-1"><slot name="header">{{ title }}</slot></div><Button v-if="collapsible && layout === 'panel'" icon-only variant="light" color="default" :aria-label="collapsed ? expandLabel : collapseLabel" :aria-expanded="!collapsed" :aria-controls="id" @click="collapsed = !collapsed"><Icon :name="collapsed ? 'chevron-right' : 'chevron-left'" /></Button></div>
    <nav :id="id" :aria-label="label" class="moe-sidebar-groups"><div v-for="group in groups" :key="group.label" class="grid gap-1"><p class="moe-sidebar-group" :class="{ 'sr-only': collapsed }">{{ group.label }}</p><NavItem v-for="item in group.items" :key="item.id" :item="item" :active="active === item.id" :compact="collapsed" @navigate="(event, entry) => $emit('navigate', event, entry)" /></div></nav>
    <div v-if="$slots.footer || footerText" class="moe-sidebar-footer"><slot name="footer" :collapsed="collapsed"><p v-if="!collapsed" class="px-2 text-xs text-muted">{{ footerText }}</p></slot></div>
    <Button v-if="collapsible && layout === 'rail'" class="moe-sidebar-collapse" icon-only variant="light" color="default" :aria-label="collapsed ? expandLabel : collapseLabel" :aria-expanded="!collapsed" :aria-controls="id" @click="collapsed = !collapsed"><Icon :name="collapsed ? 'chevron-right' : 'chevron-left'" /></Button>
  </aside>
</template>
