<script setup lang="ts">
import Icon from './Icon.vue'
defineProps<{ application: string; provider: string }>()
</script>
<template>
  <div class="moe-authorization-handshake">
    <span class="moe-authorization-app" :aria-label="application">{{ application.trim().slice(0, 1).toUpperCase() || '?' }}</span>
    <span class="moe-authorization-connector" aria-hidden="true" /><Icon name="arrow-right" /><span class="moe-authorization-connector" aria-hidden="true" />
    <span class="moe-authorization-app moe-authorization-provider" :aria-label="provider"><slot name="provider">M</slot></span>
  </div>
</template>
