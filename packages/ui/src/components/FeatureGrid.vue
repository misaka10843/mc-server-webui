<script setup lang="ts">
import type { MoeIconName } from '../types'
import Card from './Card.vue'
import Icon from './Icon.vue'
defineProps<{ items: { id: string; title: string; description: string; icon: MoeIconName }[] }>()
</script>
<template><div class="moe-feature-grid"><Card v-for="item in items" :key="item.id" padding="lg"><Icon :name="item.icon" class="text-primary" /><h2 class="mt-4 text-base font-semibold">{{ item.title }}</h2><p class="mt-2 text-sm leading-7 text-muted">{{ item.description }}</p></Card></div></template>
