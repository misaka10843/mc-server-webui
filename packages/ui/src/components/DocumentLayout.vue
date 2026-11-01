<script setup lang="ts">
defineProps<{ label: string; items: { id: string; label: string }[] }>()
</script>
<template><div class="moe-document-layout"><details class="moe-document-mobile-outline"><summary class="moe-focus">{{ label }}</summary><nav :aria-label="label"><a v-for="item in items" :key="item.id" class="moe-outline-link moe-focus" :href="`#${item.id}`">{{ item.label }}</a></nav></details><article class="moe-document min-w-0"><slot /></article><aside class="moe-document-outline"><nav :aria-label="label"><p class="mb-3 text-sm font-semibold">{{ label }}</p><a v-for="item in items" :key="item.id" class="moe-outline-link moe-focus" :href="`#${item.id}`">{{ item.label }}</a></nav><slot name="aside" /></aside></div></template>
