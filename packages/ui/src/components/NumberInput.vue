<script setup lang="ts">
import { useId } from 'vue'
import { NumberFieldRoot, NumberFieldInput, NumberFieldIncrement, NumberFieldDecrement } from 'reka-ui'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; min?: number; max?: number; step?: number; disabled?: boolean; description?: string; error?: string; name?: string; locale?: string; increaseLabel?: string; decreaseLabel?: string }>(), { step: 1, locale: 'zh-CN', increaseLabel: '增加', decreaseLabel: '减少' })
const model = defineModel<number>()
const id = useId()
</script>
<template><div class="moe-field"><label :for="id" class="moe-label">{{ label }}</label><NumberFieldRoot v-model="model" :min="min" :max="max" :step="step" :disabled="disabled" :name="name" :locale="locale" disable-wheel-change class="moe-number"><NumberFieldDecrement class="moe-number-step moe-focus" :aria-label="decreaseLabel"><span aria-hidden="true">−</span></NumberFieldDecrement><NumberFieldInput :id="id" :aria-invalid="!!error" :aria-describedby="description || error ? `${id}-help` : undefined" class="moe-number-input moe-focus" /><NumberFieldIncrement class="moe-number-step moe-focus" :aria-label="increaseLabel"><Icon name="plus" class="size-4" /></NumberFieldIncrement></NumberFieldRoot><p v-if="description || error" :id="`${id}-help`" class="moe-description" :class="{ 'moe-error': error }" :role="error ? 'alert' : undefined">{{ error || description }}</p></div></template>
