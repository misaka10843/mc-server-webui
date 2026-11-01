<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
const props = defineProps<{ value: string; label: string; errorLabel: string }>()
const source = ref('')
const failed = ref(false)
let active = false
let generation = 0
const render = async () => {
  const current = ++generation
  source.value = ''; failed.value = false
  if (!active || !props.value) return
  try {
    const { toDataURL } = await import('qrcode')
    if (!active || current !== generation) return
    const result = await toDataURL(props.value, { width: 256, margin: 4, errorCorrectionLevel: 'M', color: { dark: '#000000', light: '#ffffff' } })
    if (active && current === generation) source.value = result
  } catch { if (active && current === generation) failed.value = true }
}
watch(() => props.value, render)
onMounted(() => { active = true; void render() })
onBeforeUnmount(() => { active = false; generation++; source.value = '' })
</script>
<template><div class="grid justify-items-center gap-2"><img v-if="source" :src="source" :alt="label" width="256" height="256" class="max-w-full rounded-xl" draggable="false"><p v-else-if="failed" role="alert" class="text-sm text-danger">{{ errorLabel }}</p></div></template>
