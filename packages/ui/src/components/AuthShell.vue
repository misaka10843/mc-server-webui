<script setup lang="ts">
import { useId } from 'vue'
defineProps<{ skipLabel: string; brandLabel: string }>()
const mainId = useId()
</script>
<template>
  <div class="moe-auth-shell">
    <a :href="`#${mainId}`" class="moe-skip-link moe-focus">{{ skipLabel }}</a>
    <div class="moe-auth-column">
      <header class="moe-auth-header"><slot name="header" /></header>
      <div v-if="$slots['mobile-brand']" class="moe-auth-mobile-brand"><slot name="mobile-brand" /></div>
      <main :id="mainId" class="moe-auth-main" tabindex="-1"><slot /></main>
      <footer class="moe-auth-footer"><slot name="footer" /></footer>
    </div>
    <aside class="moe-auth-brand" :aria-label="brandLabel"><slot name="brand" /></aside>
  </div>
</template>
