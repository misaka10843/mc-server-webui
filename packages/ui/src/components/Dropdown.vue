<script setup lang="ts">
import { DropdownMenuRoot, DropdownMenuTrigger, DropdownMenuPortal, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuLabel } from 'reka-ui'
import type { MoeMenuItem } from '../types'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; items: MoeMenuItem[]; heading?: string; align?: 'start' | 'center' | 'end' }>(), { align: 'end' })
const open = defineModel<boolean>('open', { default: false })
defineEmits<{ select: [item: MoeMenuItem] }>()
</script>
<template><DropdownMenuRoot v-model:open="open"><DropdownMenuTrigger as-child><slot /></DropdownMenuTrigger><DropdownMenuPortal><DropdownMenuContent :aria-label="label" :align="align" :side-offset="8" class="moe-popup moe-popover moe-dropdown"><DropdownMenuLabel v-if="heading" class="moe-menu-heading">{{ heading }}</DropdownMenuLabel><template v-for="(item, index) in items" :key="item.id"><DropdownMenuSeparator v-if="item.separatorBefore && index > 0" class="moe-menu-separator" /><DropdownMenuItem :disabled="item.disabled" class="moe-menu-item" :data-danger="item.danger" @select="$emit('select', item)"><Icon v-if="item.icon" :name="item.icon" /><span class="min-w-0 flex-1"><span class="block">{{ item.label }}</span><span v-if="item.description" class="moe-description block">{{ item.description }}</span></span><kbd v-if="item.shortcut" class="moe-menu-shortcut">{{ item.shortcut }}</kbd></DropdownMenuItem></template></DropdownMenuContent></DropdownMenuPortal></DropdownMenuRoot></template>
