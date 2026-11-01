<script setup lang="ts">
import { useId } from 'vue'
import { ComboboxRoot, ComboboxAnchor, ComboboxInput, ComboboxTrigger, ComboboxPortal, ComboboxContent, ComboboxViewport, ComboboxItem, ComboboxItemIndicator, ComboboxEmpty } from 'reka-ui'
import type { MoeOption } from '../types'
import Icon from './Icon.vue'
const props = withDefaults(defineProps<{ label: string; options: MoeOption[]; placeholder?: string; emptyText?: string; disabled?: boolean; description?: string; error?: string; name?: string }>(), { placeholder: '搜索并选择', emptyText: '没有匹配的选项' })
const model = defineModel<string>()
const id = useId()
const displayValue = (value: unknown) => props.options.find(option => option.value === value)?.label ?? ''
</script>
<template>
  <div class="moe-field">
    <label :for="id" class="moe-label">{{ label }}</label>
    <ComboboxRoot v-model="model" :disabled="disabled" :name="name">
      <ComboboxAnchor class="moe-combobox-anchor"><ComboboxInput :id="id" :display-value="displayValue" :placeholder="placeholder" :aria-invalid="!!error" :aria-describedby="description || error ? `${id}-help` : undefined" class="moe-input moe-control moe-focus moe-disabled pr-12" /><ComboboxTrigger class="moe-combobox-trigger moe-focus" :disabled="disabled" :aria-label="label"><Icon name="chevron-down" /></ComboboxTrigger></ComboboxAnchor>
      <ComboboxPortal><ComboboxContent position="popper" :side-offset="6" class="moe-popup moe-popover min-w-[var(--reka-combobox-trigger-width)] max-w-[calc(100vw-24px)]"><ComboboxViewport class="max-h-64 overflow-y-auto"><ComboboxEmpty class="p-4 text-sm text-muted">{{ emptyText }}</ComboboxEmpty><ComboboxItem v-for="option in options" :key="option.value" :value="option.value" :text-value="option.label" :disabled="option.disabled" class="moe-select-item"><span class="flex-1">{{ option.label }}</span><ComboboxItemIndicator><Icon name="check" class="size-4" /></ComboboxItemIndicator></ComboboxItem></ComboboxViewport></ComboboxContent></ComboboxPortal>
    </ComboboxRoot>
    <p v-if="description || error" :id="`${id}-help`" class="moe-description" :class="{ 'moe-error': error }" :role="error ? 'alert' : undefined">{{ error || description }}</p>
  </div>
</template>
