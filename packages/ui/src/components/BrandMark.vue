<script setup lang="ts">
import { ref } from 'vue'
import portrait from '../assets/illustrations/mascot-face-neutral.webp'
withDefaults(defineProps<{ size?: 'sm' | 'md' | 'lg' }>(), { size: 'md' })
const failed = ref(false)
</script>
<template><span class="moe-brand-mark" :data-size="size" aria-hidden="true"><img v-if="!failed" :src="portrait" alt="" width="192" height="192" decoding="async" @error="failed = true" /><span v-else>M</span></span></template>
