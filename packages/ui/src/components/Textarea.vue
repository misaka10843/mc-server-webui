<script setup lang="ts">
import { useId } from 'vue'
import type { MoeSize } from '../types'
defineOptions({ inheritAttrs: false })
const model = defineModel<string>({ default: '' })
withDefaults(defineProps<{ label: string; description?: string; error?: string; disabled?: boolean; rows?: number; size?: MoeSize }>(), { rows: 4, size: 'md' })
const id = useId()
</script>

<template>
  <div class="moe-field">
    <label :for="id" class="moe-label">{{ label }}</label>
    <textarea :id="id" v-model="model" v-bind="$attrs" :rows="rows" :disabled="disabled" :aria-invalid="!!error" :aria-describedby="error ? `${id}-error` : description ? `${id}-description` : undefined" class="moe-input moe-control moe-focus moe-disabled resize-y leading-6" :data-size="size" />
    <p v-if="error" :id="`${id}-error`" role="alert" class="moe-description moe-error">{{ error }}</p>
    <p v-else-if="description" :id="`${id}-description`" class="moe-description">{{ description }}</p>
  </div>
</template>
