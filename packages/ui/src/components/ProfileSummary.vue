<script setup lang="ts">
import Avatar from './Avatar.vue'
import Card from './Card.vue'
defineProps<{ name: string; email: string; description?: string; src?: string }>()
</script>
<template><Card><div class="moe-profile-identity"><Avatar :name="name" :src="src" size="lg" /><h2 class="text-lg font-semibold">{{ name }}</h2><p class="text-sm text-muted break-all">{{ email }}</p><slot /></div><p v-if="description" class="moe-profile-caption">{{ description }}</p></Card></template>
