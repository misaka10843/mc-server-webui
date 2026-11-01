<script setup lang="ts">
import { ref } from 'vue'
import type { MoeSize } from '../types'
import Input from './Input.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
defineOptions({ inheritAttrs: false })
withDefaults(defineProps<{ label: string; description?: string; error?: string; disabled?: boolean; size?: MoeSize; showLabel?: string; hideLabel?: string }>(), { size: 'md', showLabel: '显示密码', hideLabel: '隐藏密码' })
const model = defineModel<string>({ default: '' })
const visible = ref(false)
</script>
<template><Input v-model="model" v-bind="$attrs" :label="label" :description="description" :error="error" :disabled="disabled" :size="size" :type="visible ? 'text' : 'password'"><template #trailing><Button :size="size" icon-only variant="light" color="default" :disabled="disabled" :aria-label="visible ? hideLabel : showLabel" :aria-pressed="visible" @click="visible = !visible"><Icon :name="visible ? 'eye-off' : 'eye'" /></Button></template></Input></template>
