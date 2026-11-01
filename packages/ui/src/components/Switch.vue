<script setup lang="ts">
import { useId } from 'vue'
import { SwitchRoot, SwitchThumb } from 'reka-ui'
import type { MoeColor } from '../types'
const model = defineModel<boolean>({ default: false })
withDefaults(defineProps<{ label: string; description?: string; disabled?: boolean; name?: string; color?: MoeColor }>(), { color: 'primary' })
const id = useId()
</script>

<template>
  <label :for="id" class="moe-choice" :data-disabled="!!disabled">
    <SwitchRoot :id="id" v-model="model" :disabled="disabled" :name="name" :aria-labelledby="`${id}-label`" :aria-describedby="description ? `${id}-description` : undefined" class="moe-switch moe-focus" :class="`moe-tone-${color}`"><SwitchThumb class="moe-switch-thumb" /></SwitchRoot>
    <span class="grid gap-1"><span :id="`${id}-label`" class="moe-label">{{ label }}</span><span v-if="description" :id="`${id}-description`" class="moe-description">{{ description }}</span></span>
  </label>
</template>
