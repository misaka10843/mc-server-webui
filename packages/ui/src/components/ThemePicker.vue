<script setup lang="ts">
import { computed } from 'vue'
import Dropdown from './Dropdown.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
import type { MoeMenuItem } from '../types'
const props = defineProps<{ label: string; lightLabel: string; darkLabel: string; systemLabel: string }>()
const model = defineModel<'light' | 'dark' | 'system'>({ default: 'light' })
const items = computed<MoeMenuItem[]>(() => [{ id: 'light', label: props.lightLabel, icon: model.value === 'light' ? 'check' : 'sun' }, { id: 'dark', label: props.darkLabel, icon: model.value === 'dark' ? 'check' : 'moon' }, { id: 'system', label: props.systemLabel, icon: model.value === 'system' ? 'check' : 'settings' }])
const select = (item: MoeMenuItem) => { if (item.id === 'light' || item.id === 'dark' || item.id === 'system') model.value = item.id }
</script>
<template><Dropdown :label="label" :items="items" @select="select"><Button variant="light" color="default" icon-only :aria-label="label"><Icon :name="model === 'dark' ? 'moon' : model === 'system' ? 'settings' : 'sun'" /></Button></Dropdown></template>
