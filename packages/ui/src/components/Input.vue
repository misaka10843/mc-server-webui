<script setup lang="ts">
import { computed, useAttrs, useId } from 'vue'
import type { MoeSize } from '../types'
defineOptions({ inheritAttrs: false })

const model = defineModel<string>({ default: '' })
const props = withDefaults(defineProps<{
  label: string
  id?: string
  type?: 'text' | 'email' | 'password' | 'search' | 'tel' | 'url' | 'date' | 'datetime-local'
  error?: string
  description?: string
  autocomplete?: string
  disabled?: boolean
  size?: MoeSize
}>(), { type: 'text', size: 'md' })
const generatedId = useId()
const inputId = props.id ?? generatedId
const attrs = useAttrs()
const describedBy = computed(() => [
  typeof attrs['aria-describedby'] === 'string' ? attrs['aria-describedby'] : undefined,
  props.description ? `${inputId}-description` : undefined,
  props.error ? `${inputId}-error` : undefined,
].filter(Boolean).join(' ') || undefined)
</script>

<template>
  <div class="moe-field">
    <label :for="inputId" class="moe-label">{{ label }}</label>
    <div class="relative min-w-0">
    <input
      v-bind="$attrs"
      :id="inputId"
      v-model="model"
      :type="type"
      :autocomplete="autocomplete"
      :disabled="disabled"
      :aria-invalid="!!error"
      :aria-describedby="describedBy"
      class="moe-input moe-control moe-focus moe-disabled"
      :data-size="size"
      :style="$slots.trailing ? { paddingRight: '48px' } : undefined"
    >
      <div v-if="$slots.trailing" class="absolute inset-y-0 right-0 flex items-center"><slot name="trailing" :size="size" /></div>
    </div>
    <p v-if="description" :id="`${inputId}-description`" class="moe-description">{{ description }}</p>
    <p v-if="error" :id="`${inputId}-error`" role="alert" class="moe-description moe-error">{{ error }}</p>
  </div>
</template>
