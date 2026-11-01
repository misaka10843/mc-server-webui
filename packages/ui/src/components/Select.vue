<script setup lang="ts">
import { useId } from 'vue'
import { SelectRoot, SelectTrigger, SelectValue, SelectPortal, SelectContent, SelectViewport, SelectItem, SelectItemText, SelectItemIndicator, SelectScrollUpButton, SelectScrollDownButton } from 'reka-ui'
import type { MoeOption, MoeSize } from '../types'
const model = defineModel<string>()
withDefaults(defineProps<{ label: string; options: MoeOption[]; placeholder?: string; description?: string; error?: string; disabled?: boolean; name?: string; required?: boolean; size?: MoeSize }>(), { placeholder: '请选择 · Select', size: 'md' })
const id = useId()
</script>

<template>
  <div class="moe-field">
    <label :id="`${id}-label`" :for="id" class="moe-label">{{ label }}</label>
    <SelectRoot v-model="model" :disabled="disabled" :name="name" :required="required">
      <SelectTrigger :id="id" class="moe-input moe-control moe-focus moe-disabled flex items-center justify-between gap-3 text-left" :data-size="size" :aria-labelledby="`${id}-label`" :aria-invalid="!!error" :aria-describedby="error ? `${id}-error` : description ? `${id}-description` : undefined">
        <SelectValue :placeholder="placeholder" /><svg class="moe-select-chevron shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
      </SelectTrigger>
      <SelectPortal><SelectContent position="popper" :side-offset="5" class="moe-popup moe-popover min-w-[var(--reka-select-trigger-width)] max-w-[calc(100vw-24px)]">
        <SelectScrollUpButton class="text-center text-xs" aria-hidden="true">⌃</SelectScrollUpButton>
        <SelectViewport class="max-h-64">
          <SelectItem v-for="option in options" :key="option.value" :value="option.value" :disabled="option.disabled" class="moe-select-item">
            <SelectItemText class="flex-1">{{ option.label }}</SelectItemText><SelectItemIndicator aria-hidden="true">✓</SelectItemIndicator>
          </SelectItem>
        </SelectViewport>
        <SelectScrollDownButton class="text-center text-xs" aria-hidden="true">⌄</SelectScrollDownButton>
      </SelectContent></SelectPortal>
    </SelectRoot>
    <p v-if="error" :id="`${id}-error`" role="alert" class="moe-description moe-error">{{ error }}</p>
    <p v-else-if="description" :id="`${id}-description`" class="moe-description">{{ description }}</p>
  </div>
</template>
