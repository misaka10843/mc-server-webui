<script setup lang="ts">
import type { MoeColor } from '../types'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; color?: MoeColor; removable?: boolean; disabled?: boolean; removeLabel?: string }>(), { color: 'primary' })
defineEmits<{ remove: [] }>()
</script>
<template><span class="moe-tag" :class="`moe-tone-${color}`"><span>{{ label }}</span><button v-if="removable" type="button" class="moe-tag-remove moe-focus" :disabled="disabled" :aria-label="removeLabel ?? `移除 ${label}`" @click="$emit('remove')"><Icon name="close" class="size-3.5" /></button></span></template>
