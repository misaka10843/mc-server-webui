<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
defineProps<{ value: string; label: string; copiedLabel: string; errorLabel: string }>()
const state = ref<'idle' | 'copied' | 'error'>('idle')
let timer: ReturnType<typeof setTimeout> | undefined
const copy = async (value: string) => {
  try { await navigator.clipboard.writeText(value); state.value = 'copied' }
  catch { state.value = 'error' }
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => { state.value = 'idle' }, 2500)
}
onBeforeUnmount(() => { if (timer) clearTimeout(timer) })
</script>
<template><span class="moe-copy-control"><Button size="sm" variant="light" color="default" @click="copy(value)">{{ state === 'copied' ? copiedLabel : label }}<Icon :name="state === 'copied' ? 'check' : 'copy'" class="size-3.5" /></Button><span :class="state === 'error' ? 'text-xs text-danger' : 'sr-only'" role="status">{{ state === 'error' ? errorLabel : state === 'copied' ? copiedLabel : '' }}</span></span></template>
