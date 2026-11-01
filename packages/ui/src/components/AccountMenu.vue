<script setup lang="ts">
import type { MoeMenuItem } from '../types'
import Avatar from './Avatar.vue'
import Dropdown from './Dropdown.vue'
defineProps<{ label: string; name: string; email: string; src?: string; items: MoeMenuItem[] }>()
defineEmits<{ select: [item: MoeMenuItem] }>()
</script>
<template>
  <Dropdown :label="label" :heading="email" :items="items" @select="item => $emit('select', item)">
    <button type="button" class="moe-account-trigger moe-focus" :aria-label="label"><Avatar :name="name" :src="src" size="sm" /></button>
  </Dropdown>
</template>
