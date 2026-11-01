<script setup lang="ts">
import { useId } from 'vue'
import Icon from './Icon.vue'
withDefaults(defineProps<{ label: string; accept?: string; multiple?: boolean; disabled?: boolean; description?: string; error?: string; name?: string; chooseLabel?: string; clearLabel?: string }>(), { chooseLabel: '选择文件', clearLabel: '清除已选文件' })
const model = defineModel<File[]>({ default: () => [] })
const id = useId()
const change = (event: Event) => { const input = event.target; if (input instanceof HTMLInputElement) model.value = Array.from(input.files ?? []) }
const clear = () => { model.value = []; const input = document.getElementById(id); if (input instanceof HTMLInputElement) { input.value = ''; input.focus() } }
</script>
<template><div class="moe-field"><label :for="id" class="moe-label">{{ label }}</label><div class="moe-file-input" :data-disabled="disabled"><input :id="id" type="file" :accept="accept" :multiple="multiple" :disabled="disabled" :name="name" :aria-invalid="!!error" :aria-describedby="description || error ? `${id}-help` : undefined" class="moe-file-native" @change="change" /><span class="moe-file-choose" aria-hidden="true"><Icon name="plus" class="size-4" />{{ chooseLabel }}</span><span v-if="model.length" class="min-w-0 flex-1 truncate text-sm">{{ model.map(file => file.name).join('、') }}</span><button v-if="model.length" type="button" class="moe-file-clear moe-focus" :disabled="disabled" :aria-label="clearLabel" @click="clear"><Icon name="close" class="size-4" /></button></div><p v-if="description || error" :id="`${id}-help`" class="moe-description" :class="{ 'moe-error': error }" :role="error ? 'alert' : undefined">{{ error || description }}</p></div></template>
