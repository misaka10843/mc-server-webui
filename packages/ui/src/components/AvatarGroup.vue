<script setup lang="ts">
import { computed } from 'vue'
import type { MoeSize } from '../types'
import Avatar from './Avatar.vue'
const props = withDefaults(defineProps<{ label: string; items: { id: string; name: string; src?: string }[]; max?: number; size?: MoeSize; moreLabel?: (count: number) => string }>(), { max: 4, size: 'md', moreLabel: (count: number) => `另有 ${count} 位成员` })
const visible = computed(() => props.items.slice(0, Math.max(0, props.max)))
const hidden = computed(() => props.items.length - visible.value.length)
</script>
<template><div role="group" :aria-label="label" class="moe-avatar-group"><Avatar v-for="person in visible" :key="person.id" :name="person.name" :src="person.src" :size="size" /><span v-if="hidden > 0" class="moe-avatar moe-tone-default" :data-size="size" role="img" :aria-label="moreLabel(hidden)">+{{ hidden }}</span></div></template>
