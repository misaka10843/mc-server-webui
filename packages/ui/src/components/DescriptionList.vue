<script setup lang="ts">
defineProps<{ items: { key: string; label: string; value: string }[] }>()
</script>
<template><dl class="moe-description-list"><div v-for="item in items" :key="item.key"><dt>{{ item.label }}</dt><dd><slot :name="item.key" :item="item">{{ item.value }}</slot></dd></div></dl></template>
