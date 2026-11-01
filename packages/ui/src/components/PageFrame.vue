<script setup lang="ts">
import { useId } from 'vue'
withDefaults(defineProps<{ skipLabel: string; density?: 'default' | 'compact' | 'landing' }>(), { density: 'default' })
const mainId = useId()
</script>
<template>
  <div class="moe-page-frame" :data-density="density" :data-rail="!!$slots.sidebar">
    <a :href="`#${mainId}`" class="moe-skip-link moe-focus">{{ skipLabel }}</a>
    <div v-if="$slots.sidebar" class="moe-page-rail"><slot name="sidebar" /></div>
    <div class="moe-page-body">
    <div class="moe-page-header"><div class="moe-page-header-inner"><slot name="header" /></div></div>
    <main :id="mainId" class="moe-page-main" tabindex="-1"><slot /></main>
    <footer v-if="$slots.footer" class="moe-page-footer"><slot name="footer" /></footer>
    </div>
  </div>
</template>
