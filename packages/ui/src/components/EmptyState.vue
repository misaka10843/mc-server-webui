<script setup lang="ts">
import type { MoeIconName } from '../types'
import Icon from './Icon.vue'
import Illustration from './Illustration.vue'
import type { MoeIllustrationName } from '../illustrations'
withDefaults(defineProps<{ title: string; description?: string; icon?: MoeIconName; illustration?: MoeIllustrationName; illustrationSize?: 'sm' | 'md' | 'lg' }>(), { icon: 'inbox', illustrationSize: 'md' })
</script>
<template><div class="moe-empty"><Illustration v-if="illustration" :name="illustration" :size="illustrationSize" /><div v-else class="moe-empty-icon"><slot name="icon"><Icon :name="icon" class="size-7" /></slot></div><h3 class="font-semibold text-foreground">{{ title }}</h3><p v-if="description" class="max-w-sm text-sm leading-6 text-muted">{{ description }}</p><div v-if="$slots.default" class="mt-2 flex flex-wrap justify-center gap-2"><slot /></div></div></template>
