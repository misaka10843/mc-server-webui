<script setup lang="ts">
import { DialogRoot, DialogTrigger, DialogPortal, DialogOverlay, DialogContent, DialogTitle, DialogDescription, DialogClose } from 'reka-ui'
import Button from './Button.vue'
import Icon from './Icon.vue'
import { useId } from 'vue'
withDefaults(defineProps<{ title: string; description?: string; side?: 'left' | 'right'; closeLabel?: string }>(), { side: 'right', closeLabel: '关闭抽屉' })
const open = defineModel<boolean>('open', { default: false })
const descriptionId = useId()
</script>
<template><DialogRoot v-model:open="open"><DialogTrigger as-child><slot name="trigger" /></DialogTrigger><DialogPortal><DialogOverlay class="moe-dialog-overlay fixed inset-0 z-40 bg-overlay" /><DialogContent class="moe-drawer" :class="`moe-drawer-${side}`" :aria-describedby="description ? descriptionId : undefined"><div class="moe-drawer-heading"><DialogTitle class="font-semibold">{{ title }}</DialogTitle><DialogClose as-child><Button icon-only variant="light" color="default" :aria-label="closeLabel"><Icon name="close" /></Button></DialogClose></div><DialogDescription v-if="description" :id="descriptionId" class="text-sm leading-6 text-muted">{{ description }}</DialogDescription><div class="min-h-0 flex-1 overflow-y-auto"><slot :close="() => open = false" /></div><div v-if="$slots.footer" class="border-t border-line pt-4"><slot name="footer" :close="() => open = false" /></div></DialogContent></DialogPortal></DialogRoot></template>
