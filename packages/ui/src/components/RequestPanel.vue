<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Button from './Button.vue'
import CodeBlock from './CodeBlock.vue'
defineProps<{ title: string; hint: string; runLabel: string; clearLabel: string; cancelLabel: string; responseLabel: string; elapsedLabel: string; copyLabel: string; copiedLabel: string; errorLabel: string; busy?: boolean; disabled?: boolean; response?: string; status?: number; elapsed?: number }>()
defineEmits<{ run: []; clear: []; cancel: [] }>()
const ready = ref(false)
onMounted(() => { ready.value = true })
</script>
<template><section class="moe-request-panel"><header><h2>{{ title }}</h2><p class="text-sm text-muted">{{ hint }}</p></header><form class="grid gap-4" @submit.prevent="$emit('run')"><fieldset class="grid min-w-0 gap-4 border-0 p-0" :disabled="!ready || busy"><slot /></fieldset><div class="flex flex-wrap gap-3"><Button type="submit" :disabled="disabled || !ready" :loading="busy">{{ runLabel }}</Button><Button v-if="busy" variant="bordered" @click="$emit('cancel')">{{ cancelLabel }}</Button><Button variant="light" :disabled="!ready" @click="$emit('clear')">{{ clearLabel }}</Button></div></form><div v-if="status || response !== undefined" class="grid gap-3" aria-live="polite"><p class="text-sm"><strong v-if="status">HTTP {{ status }}</strong><span v-if="elapsed !== undefined" class="ml-4 text-muted">{{ elapsedLabel }} {{ elapsed }} ms</span></p><CodeBlock :title="responseLabel" :code="response ?? ''" :copy-label="copyLabel" :copied-label="copiedLabel" :error-label="errorLabel" /></div></section></template>
