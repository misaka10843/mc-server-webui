<script setup lang="ts">
import CopyButton from './CopyButton.vue'
defineProps<{ title: string; code: string; copyLabel: string; copiedLabel: string; errorLabel: string }>()
</script>
<template><section class="moe-code-block"><header><span>{{ title }}</span><CopyButton :value="code" :label="copyLabel" :copied-label="copiedLabel" :error-label="errorLabel" /></header><pre tabindex="0"><code>{{ code }}</code></pre></section></template>
