<script setup lang="ts">
import Avatar from './Avatar.vue'
defineProps<{ name: string; description?: string; src?: string }>()
</script>
<template><div class="moe-user-chip"><Avatar :name="name" :src="src" /><div class="min-w-0"><p class="truncate text-sm font-medium">{{ name }}</p><p v-if="description" class="truncate text-xs text-muted">{{ description }}</p></div><slot /></div></template>
