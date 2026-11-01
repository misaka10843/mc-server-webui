<script setup lang="ts">
import { computed } from 'vue'
import { AvatarRoot, AvatarImage, AvatarFallback } from 'reka-ui'
import type { MoeColor, MoeSize } from '../types'
const props = withDefaults(defineProps<{ name: string; src?: string; size?: MoeSize; color?: MoeColor; shape?: 'circle' | 'square' }>(), { size: 'md', color: 'primary', shape: 'circle' })
const initials = computed(() => { const parts = props.name.trim().split(/\s+/); return parts.length > 1 ? `${parts[0]?.[0] ?? ''}${parts.at(-1)?.[0] ?? ''}`.toUpperCase() : Array.from(props.name.trim()).slice(0, 2).join('').toUpperCase() })
</script>
<template><AvatarRoot class="moe-avatar" :class="`moe-tone-${color}`" :data-size="size" :data-shape="shape" role="img" :aria-label="name"><AvatarImage v-if="src" :src="src" alt="" class="size-full object-cover" /><AvatarFallback aria-hidden="true">{{ initials || '?' }}</AvatarFallback></AvatarRoot></template>
