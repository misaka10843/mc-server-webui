<script setup lang="ts">
import { useId } from 'vue'
import { RadioGroupRoot, RadioGroupItem, RadioGroupIndicator } from 'reka-ui'
import type { MoeColor, MoeOption } from '../types'
const model = defineModel<string>()
withDefaults(defineProps<{ label: string; options: MoeOption[]; disabled?: boolean; name?: string; color?: MoeColor; orientation?: 'horizontal' | 'vertical' }>(), { color: 'primary', orientation: 'vertical' })
const id = useId()
</script>

<template>
  <div class="moe-field">
    <span :id="`${id}-label`" class="moe-label">{{ label }}</span>
    <RadioGroupRoot v-model="model" :aria-labelledby="`${id}-label`" :disabled="disabled" :name="name" :orientation="orientation" class="flex gap-x-6 gap-y-1" :class="orientation === 'vertical' ? 'flex-col' : 'flex-wrap'">
      <label v-for="(option, index) in options" :key="option.value" :for="`${id}-${index}`" class="moe-choice" :data-disabled="!!(disabled || option.disabled)">
        <RadioGroupItem :id="`${id}-${index}`" :value="option.value" :disabled="option.disabled" :aria-labelledby="`${id}-${index}-label`" :aria-describedby="option.description ? `${id}-${index}-description` : undefined" class="moe-radio moe-focus" :class="`moe-tone-${color}`"><RadioGroupIndicator class="moe-radio-indicator" /></RadioGroupItem>
        <span class="grid gap-1"><span :id="`${id}-${index}-label`" class="moe-label">{{ option.label }}</span><span v-if="option.description" :id="`${id}-${index}-description`" class="moe-description">{{ option.description }}</span></span>
      </label>
    </RadioGroupRoot>
  </div>
</template>
