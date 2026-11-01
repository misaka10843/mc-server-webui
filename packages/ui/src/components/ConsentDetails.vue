<script setup lang="ts">
defineProps<{ title: string; items: { key: string; label: string; value: string; field?: string }[] }>()
</script>
<template>
  <section class="moe-consent-details">
    <h2>{{ title }}</h2>
    <dl><div v-for="item in items" :key="item.key"><dt>{{ item.label }}<span v-if="item.field">{{ item.field }}</span></dt><dd>{{ item.value }}</dd></div></dl>
  </section>
</template>
