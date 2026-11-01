<script setup lang="ts">
import { computed, useId } from 'vue'
import type { MoeTreeEntry } from '../types'
import HttpMethod from './HttpMethod.vue'
const props = defineProps<{ item: MoeTreeEntry; active?: string; expanded: string[] }>()
const emit = defineEmits<{ toggle: [id: string, open: boolean]; navigate: [event: MouseEvent, item: MoeTreeEntry] }>()
const id = useId()
const open = computed(() => props.expanded.includes(props.item.id))
</script>
<template><li class="moe-tree-branch"><template v-if="item.children"><button type="button" class="moe-tree-folder moe-focus" :aria-expanded="open" :aria-controls="id" @click="emit('toggle', item.id, !open)" @keydown.right.prevent="emit('toggle', item.id, true)" @keydown.left.prevent="emit('toggle', item.id, false)"><span class="moe-tree-chevron" :data-open="open" aria-hidden="true">›</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 7V5a1 1 0 0 1 1-1h6l2 3h8a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7Z" /></svg><span>{{ item.label }}</span><span class="ml-auto text-xs text-muted">{{ item.children.length }}</span></button><ul v-show="open" :id="id" class="moe-tree-children"><NavigationBranch v-for="child in item.children" :key="child.id" :item="child" :active="active" :expanded="expanded" @toggle="(id, value) => emit('toggle', id, value)" @navigate="(event, entry) => emit('navigate', event, entry)" /></ul></template><a v-else :href="item.href" class="moe-tree-link moe-focus" :aria-current="item.id === active ? 'page' : undefined" :title="item.description || item.label" @click="emit('navigate', $event, item)"><HttpMethod v-if="item.method" :method="item.method" /><span class="min-w-0"><span class="moe-tree-label">{{ item.label }}</span><span v-if="item.description" class="moe-tree-description">{{ item.description }}</span></span></a></li></template>
