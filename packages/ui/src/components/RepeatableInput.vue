<script setup lang="ts">
import Input from './Input.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
const model = defineModel<string[]>({ required: true })
withDefaults(defineProps<{ label: string; addLabel: string; removeLabel: string; disabled?: boolean; required?: boolean; max?: number; description?: string }>(), { max: 10, required: true })
const update = (index: number, value: string) => { model.value = model.value.map((item, position) => position === index ? value : item) }
const remove = (index: number) => { model.value = model.value.filter((_, position) => position !== index) }
</script>
<template><fieldset class="moe-repeatable-input" :disabled="disabled"><legend class="moe-label mb-2">{{ label }}</legend><div v-for="(value, index) in model" :key="index" class="moe-repeatable-row"><Input :model-value="value" :label="`${label} ${index + 1}`" :disabled="disabled" :required="required" :maxlength="2048" @update:model-value="update(index, $event)" /><Button v-if="model.length > 1" icon-only size="sm" variant="light" color="danger" :aria-label="`${removeLabel} ${index + 1}`" :disabled="disabled" @click="remove(index)"><Icon name="close" /></Button></div><Button variant="light" size="sm" :disabled="disabled || model.length >= max" @click="model = [...model, '']"><Icon name="plus" />{{ addLabel }}</Button><p v-if="description" class="moe-description">{{ description }}</p></fieldset></template>
