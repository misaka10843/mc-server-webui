<script setup lang="ts">
import { computed } from 'vue'
import type { MoeColor, MoeSize, MoeVariant } from '../types'
const props = withDefaults(defineProps<{
  color?: MoeColor
  variant?: MoeVariant | 'primary' | 'secondary' | 'quiet'
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  size?: MoeSize | 'default' | 'icon'
  iconOnly?: boolean
}>(), { color: 'primary', variant: 'solid', type: 'button', size: 'md' })
const aliases: Record<string, MoeVariant> = { primary: 'solid', secondary: 'bordered', quiet: 'light' }
const resolvedVariant = computed(() => aliases[props.variant] ?? props.variant)
const resolvedSize = computed(() => props.size === 'default' || props.size === 'icon' ? 'md' : props.size)
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :aria-busy="loading || undefined"
    class="moe-button moe-control moe-focus moe-disabled"
    :class="`moe-tone-${color}`"
    :data-size="resolvedSize"
    :data-variant="resolvedVariant"
    :data-icon-only="iconOnly || size === 'icon'"
  >
    <span class="inline-flex items-center justify-center gap-2" :class="{ 'opacity-0': loading }"><slot /></span>
    <span v-if="loading" aria-hidden="true" class="absolute inset-0 flex items-center justify-center"><span class="moe-spinner" /></span>
  </button>
</template>
