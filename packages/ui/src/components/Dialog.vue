<script setup lang="ts">
import { DialogClose, DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle, DialogTrigger } from 'reka-ui'
import Button from './Button.vue'
import Icon from './Icon.vue'
import { useId } from 'vue'

withDefaults(defineProps<{ title: string; description?: string; closeLabel: string; showCloseAction?: boolean; size?: 'sm' | 'md' | 'lg' }>(), { showCloseAction: true, size: 'md' })
const open = defineModel<boolean>('open', { default: false })
const emit = defineEmits<{ openAutoFocus: [event: Event] }>()
const descriptionId = useId()
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogTrigger v-if="$slots.trigger" as-child><slot name="trigger" /></DialogTrigger>
    <DialogPortal>
      <DialogOverlay class="moe-dialog-overlay fixed inset-0 z-40 bg-overlay" />
      <DialogContent class="moe-popup moe-dialog fixed top-1/2 left-1/2 z-50 grid max-h-[calc(100svh-2rem)] -translate-x-1/2 -translate-y-1/2 gap-4 overflow-y-auto p-6 focus:outline-none" :data-size="size" :aria-describedby="description ? descriptionId : undefined" @open-auto-focus="emit('openAutoFocus', $event)">
        <div class="moe-dialog-heading"><DialogTitle class="text-xl font-bold">{{ title }}</DialogTitle><DialogClose as-child><Button icon-only size="sm" variant="light" color="default" :aria-label="closeLabel"><Icon name="close" /></Button></DialogClose></div>
        <DialogDescription v-if="description" :id="descriptionId" class="text-sm leading-6 text-muted">{{ description }}</DialogDescription>
        <slot />
        <slot name="footer" :close="() => open = false" />
        <DialogClose v-if="showCloseAction" class="min-h-11 justify-self-end rounded-lg px-3 text-sm font-medium text-primary focus-visible:outline-2 focus-visible:outline-focus">{{ closeLabel }}</DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
