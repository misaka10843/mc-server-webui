<script setup lang="ts">
import type { MoeNavGroup, MoeNavItem } from '../types'
import NavItem from './NavItem.vue'
defineProps<{ label: string; groups: MoeNavGroup[]; active?: string }>()
defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
</script>

<template>
  <div class="moe-console-layout">
    <aside class="moe-console-sidebar">
      <div class="moe-console-sidebar-inner">
        <nav :aria-label="label" class="grid gap-6">
          <div v-for="group in groups" :key="group.label">
            <p class="moe-console-section">{{ group.label }}</p>
            <div class="grid gap-1"><NavItem v-for="item in group.items" :key="item.id" :item="item" :active="item.id === active" @navigate="(event, entry) => $emit('navigate', event, entry)" /></div>
          </div>
        </nav>
        <slot name="account" />
      </div>
    </aside>
    <div class="moe-console-content"><slot /></div>
  </div>
</template>
