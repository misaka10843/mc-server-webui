<script setup lang="ts">
import type { MoeTreeEntry } from '../types'
import NavigationBranch from './NavigationBranch.vue'
defineProps<{ label: string; items: MoeTreeEntry[]; active?: string }>()
const expanded = defineModel<string[]>('expanded', { default: () => [] })
defineEmits<{ navigate: [event: MouseEvent, item: MoeTreeEntry] }>()
const toggle = (id: string, open: boolean) => { expanded.value = open ? [...new Set([...expanded.value, id])] : expanded.value.filter(value => value !== id) }
</script>
<template><nav :aria-label="label" class="moe-navigation-tree"><ul><NavigationBranch v-for="item in items" :key="item.id" :item="item" :active="active" :expanded="expanded" @toggle="toggle" @navigate="(event, item) => $emit('navigate', event, item)" /></ul></nav></template>
