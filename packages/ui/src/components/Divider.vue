<script setup lang="ts">
import { Separator } from 'reka-ui'
withDefaults(defineProps<{ orientation?: 'horizontal' | 'vertical'; decorative?: boolean }>(), { orientation: 'horizontal', decorative: true })
</script>
<template><Separator :orientation="orientation" :decorative="decorative" class="moe-divider" /></template>
