<script setup lang="ts">
import { PopoverRoot, PopoverTrigger, PopoverPortal, PopoverContent, PopoverClose } from 'reka-ui'
import Button from './Button.vue'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; align?: 'start' | 'center' | 'end'; side?: 'top' | 'right' | 'bottom' | 'left'; closeLabel?: string }>(), { align: 'center', side: 'bottom', closeLabel: '关闭' })
const open = defineModel<boolean>('open', { default: false })
</script>
<template>
  <PopoverRoot v-model:open="open">
    <PopoverTrigger as-child><slot name="trigger" /></PopoverTrigger>
    <PopoverPortal>
      <PopoverContent :side="side" :align="align" :side-offset="8" class="moe-popup moe-popover w-80 max-w-[calc(100vw-24px)] p-4">
        <div class="mb-3 flex items-center justify-between gap-3">
          <p class="text-sm font-semibold">{{ label }}</p>
          <PopoverClose as-child><Button size="sm" icon-only variant="light" color="default" :aria-label="closeLabel"><Icon name="close" /></Button></PopoverClose>
        </div>
        <slot :close="() => open = false" />
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>
