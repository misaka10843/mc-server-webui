<script setup lang="ts">
import { ToastProvider, ToastViewport } from 'reka-ui'
withDefaults(defineProps<{ duration?: number; label?: string; viewportLabel?: string }>(), { duration: 5000, label: '通知', viewportLabel: '通知（F8）' })
</script>
<template><ToastProvider :duration="duration" :label="label" swipe-direction="right"><slot /><ToastViewport :label="viewportLabel" class="moe-toast-viewport" /></ToastProvider></template>
