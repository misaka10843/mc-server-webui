<script setup lang="ts">
import { useId } from 'vue'
import { CheckboxIndicator, CheckboxRoot } from 'reka-ui'
import type { MoeColor } from '../types'
const model = defineModel<boolean | 'indeterminate'>({ default: false })
withDefaults(defineProps<{ label: string; description?: string; disabled?: boolean; required?: boolean; name?: string; color?: MoeColor }>(), { color: 'primary' })
const id = useId()
</script>

<template>
  <label :for="id" class="moe-choice" :data-disabled="!!disabled">
    <CheckboxRoot :id="id" v-model="model" :disabled="disabled" :required="required" :name="name" :aria-labelledby="`${id}-label`" :aria-describedby="description ? `${id}-description` : undefined" class="moe-check moe-focus" :class="`moe-tone-${color}`">
      <CheckboxIndicator><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path :d="model === 'indeterminate' ? 'M3 8h10' : 'm3 8 3 3 7-7'" /></svg></CheckboxIndicator>
    </CheckboxRoot>
    <span class="grid gap-1"><span :id="`${id}-label`" class="moe-label">{{ label }}</span><span v-if="description" :id="`${id}-description`" class="moe-description">{{ description }}</span></span>
  </label>
</template>
