<script setup lang="ts">
import { useId } from 'vue'
import { PinInputRoot, PinInputInput } from 'reka-ui'
withDefaults(defineProps<{ label: string; length?: number; description?: string; error?: string; disabled?: boolean; mask?: boolean; name?: string; digitLabel?: (index: number) => string }>(), { length: 6, digitLabel: (index: number) => `第 ${index + 1} 位` })
const model = defineModel<(number | undefined)[]>({ default: () => [] })
defineEmits<{ complete: [value: (number | undefined)[]] }>()
const id = useId()
</script>
<template><div class="moe-field"><span :id="`${id}-label`" class="moe-label">{{ label }}</span><PinInputRoot v-model="model" :name="name" :disabled="disabled" :mask="mask" type="number" otp :aria-labelledby="`${id}-label`" :aria-describedby="error || description ? `${id}-help` : undefined" class="moe-pin" @complete="$emit('complete', $event)"><PinInputInput v-for="(_, index) in length" :key="index" :index="index" :aria-label="`${label} ${digitLabel(index)}`" :aria-invalid="!!error" class="moe-pin-digit moe-focus moe-disabled" /></PinInputRoot><p v-if="error || description" :id="`${id}-help`" class="moe-description" :class="{ 'moe-error': error }" :role="error ? 'alert' : undefined">{{ error || description }}</p></div></template>
