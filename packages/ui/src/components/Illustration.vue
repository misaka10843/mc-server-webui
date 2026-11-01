<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { illustrations, type MoeIllustrationName } from '../illustrations'
import Icon from './Icon.vue'
const props = withDefaults(defineProps<{ name: MoeIllustrationName; size?: 'sm' | 'md' | 'lg' | 'hero'; alt?: string; desktopOnly?: boolean; eager?: boolean }>(), { size: 'md', alt: '' })
const art = computed(() => illustrations[props.name])
const failed = ref(false)
const transparent = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
watch(() => props.name, () => { failed.value = false })
</script>
<template>
  <span class="moe-illustration" :data-size="size" :data-illustration="name" :data-desktop-only="desktopOnly || undefined" :data-failed="failed || undefined" :aria-hidden="alt ? undefined : true" :style="{ aspectRatio: `${art.width} / ${art.height}` }">
    <picture v-if="!failed"><source v-if="desktopOnly" media="(min-width: 1024px)" :srcset="art.src" /><img :src="desktopOnly ? transparent : art.src" :alt="alt" :width="art.width" :height="art.height" :loading="eager ? 'eager' : 'lazy'" decoding="async" @error="failed = true" /></picture>
    <span v-else class="moe-illustration-fallback" :role="alt ? 'img' : undefined" :aria-label="alt || undefined"><Icon name="inbox" class="size-8" /></span>
  </span>
</template>
