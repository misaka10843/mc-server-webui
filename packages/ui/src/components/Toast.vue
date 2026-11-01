<script setup lang="ts">
import { ToastRoot, ToastTitle, ToastDescription, ToastClose } from 'reka-ui'
import type { MoeColor } from '../types'
import Button from './Button.vue'
import Icon from './Icon.vue'
withDefaults(defineProps<{ title: string; description?: string; color?: MoeColor; duration?: number; closeLabel?: string }>(), { color: 'info', closeLabel: '关闭通知' })
const open = defineModel<boolean>('open', { default: false })
</script>
<template><ToastRoot v-model:open="open" :duration="duration" class="moe-toast" :class="`moe-tone-${color}`"><div class="min-w-0 flex-1"><ToastTitle class="text-sm font-semibold">{{ title }}</ToastTitle><ToastDescription v-if="description" class="mt-1 text-sm leading-6 text-muted">{{ description }}</ToastDescription></div><ToastClose as-child><Button size="sm" icon-only variant="light" color="default" :aria-label="closeLabel"><Icon name="close" /></Button></ToastClose></ToastRoot></template>
