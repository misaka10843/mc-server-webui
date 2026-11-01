<script setup lang="ts">
import { computed } from 'vue'
import { SelectRoot, SelectTrigger, SelectValue, SelectPortal, SelectContent, SelectViewport, SelectItem, SelectItemText, SelectItemIndicator } from 'reka-ui'
import Icon from './Icon.vue'
import type { MoeOption } from '../types'
const model = defineModel<string>()
const props = defineProps<{ label: string; options: readonly (MoeOption & { shortLabel?: string })[]; disabled?: boolean }>()
const current = computed(() => props.options.find(option => option.value === model.value))
</script>
<template>
  <SelectRoot v-model="model" :disabled="disabled">
    <SelectTrigger class="moe-language-picker moe-control moe-focus moe-disabled" :aria-label="label" :title="current?.label" data-size="md">
      <Icon name="languages" /><SelectValue :placeholder="label">{{ current?.shortLabel ?? current?.label }}</SelectValue><Icon name="chevron-down" class="moe-select-chevron" />
    </SelectTrigger>
    <SelectPortal><SelectContent class="moe-popup moe-popover moe-language-menu" position="popper" align="end" :side-offset="8"><SelectViewport>
      <SelectItem v-for="option in options" :key="option.value" :value="option.value" :disabled="option.disabled" class="moe-select-item" :lang="option.value">
        <SelectItemText class="flex-1">{{ option.label }}</SelectItemText><SelectItemIndicator aria-hidden="true"><Icon name="check" /></SelectItemIndicator>
      </SelectItem>
    </SelectViewport></SelectContent></SelectPortal>
  </SelectRoot>
</template>
