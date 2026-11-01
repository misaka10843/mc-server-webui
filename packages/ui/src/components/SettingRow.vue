<script setup lang="ts">
import type { MoeIconName } from '../types'
import Icon from './Icon.vue'
defineProps<{ title: string; description?: string; icon?: MoeIconName; inset?: boolean }>()
</script>
<template><div class="moe-setting-row" :data-inset="inset"><div v-if="icon" class="moe-setting-icon"><Icon :name="icon" /></div><div class="moe-setting-content"><h3 class="text-sm font-medium"><slot name="title">{{ title }}</slot></h3><p v-if="description" class="mt-1 text-xs leading-6 text-muted">{{ description }}</p><div v-if="$slots.default" class="mt-2"><slot /></div></div><div v-if="$slots.actions" class="moe-setting-actions"><slot name="actions" /></div></div></template>
