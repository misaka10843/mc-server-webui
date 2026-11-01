<script setup lang="ts">
import Input from './Input.vue'
defineOptions({ inheritAttrs: false })
defineProps<{ label: string; min?: string; max?: string; disabled?: boolean; description?: string; error?: string; name?: string }>()
const model = defineModel<string>({ default: '' })
</script>
<template><Input v-model="model" v-bind="$attrs" type="date" :label="label" :min="min" :max="max" :disabled="disabled" :description="description" :error="error" :name="name" /></template>
