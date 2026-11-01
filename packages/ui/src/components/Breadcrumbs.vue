<script setup lang="ts">
import type { MoeBreadcrumbItem } from '../types'
import Icon from './Icon.vue'
withDefaults(defineProps<{ items: MoeBreadcrumbItem[]; label?: string }>(), { label: '当前位置' })
</script>
<template><nav :aria-label="label"><ol class="moe-breadcrumbs"><li v-for="(item, index) in items" :key="`${index}-${item.label}`"><Icon v-if="index > 0" name="chevron-right" class="size-3 shrink-0 text-muted" /><a v-if="item.href && index < items.length - 1" :href="item.href" class="moe-focus">{{ item.label }}</a><span v-else :aria-current="index === items.length - 1 ? 'page' : undefined">{{ item.label }}</span></li></ol></nav></template>
