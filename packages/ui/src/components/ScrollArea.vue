<script setup lang="ts">
import { ScrollAreaRoot, ScrollAreaViewport, ScrollAreaScrollbar, ScrollAreaThumb, ScrollAreaCorner } from 'reka-ui'
withDefaults(defineProps<{ label: string; height?: string }>(), { height: '240px' })
</script>
<template><ScrollAreaRoot type="auto" class="moe-scroll-area" :style="{ height }"><ScrollAreaViewport class="size-full rounded-[inherit] moe-focus" role="region" :aria-label="label" tabindex="0"><slot /></ScrollAreaViewport><ScrollAreaScrollbar orientation="vertical" class="moe-scrollbar"><ScrollAreaThumb class="moe-scroll-thumb" /></ScrollAreaScrollbar><ScrollAreaScrollbar orientation="horizontal" class="moe-scrollbar"><ScrollAreaThumb class="moe-scroll-thumb" /></ScrollAreaScrollbar><ScrollAreaCorner /></ScrollAreaRoot></template>
