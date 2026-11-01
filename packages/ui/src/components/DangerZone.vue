<script setup lang="ts">
import Card from './Card.vue'
defineProps<{ title: string; description: string }>()
</script>
<template><Card layout="form" :title="title" :description="description" class="moe-danger-zone"><slot /></Card></template>
