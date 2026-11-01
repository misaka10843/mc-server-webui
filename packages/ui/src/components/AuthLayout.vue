<script setup lang="ts">
defineProps<{ illustration?: string; illustrationAlt?: string; caption?: string; title?: string; description?: string }>()
</script>
<template>
  <div class="moe-auth-layout" :data-illustrated="!!illustration">
    <section class="moe-auth-form"><slot /></section>
    <aside v-if="illustration" class="moe-auth-art">
      <div class="moe-auth-illustration"><img :src="illustration" :alt="illustrationAlt ?? ''" width="1086" height="1448" loading="lazy" decoding="async" /></div>
      <div v-if="title || caption || description" class="moe-auth-art-caption"><p v-if="caption" class="moe-auth-eyebrow">{{ caption }}</p><h2 v-if="title" class="text-xl font-semibold">{{ title }}</h2><p v-if="description" class="text-sm leading-7 text-muted">{{ description }}</p></div>
    </aside>
  </div>
</template>
