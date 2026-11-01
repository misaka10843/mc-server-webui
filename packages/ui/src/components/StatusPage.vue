<script setup lang="ts">
import type { MoeIllustrationName } from '../illustrations'
import Illustration from './Illustration.vue'
defineProps<{ code: string; title: string; description: string; illustration: MoeIllustrationName }>()
</script>
<template>
  <div class="moe-status-page">
    <header class="moe-status-header"><slot name="header" /></header>
    <main class="moe-status-content" tabindex="-1"><Illustration :name="illustration" size="lg" eager /><p class="moe-status-code">{{ code }}</p><h1>{{ title }}</h1><p class="moe-status-description">{{ description }}</p><div class="moe-status-actions"><slot /></div></main>
  </div>
</template>
