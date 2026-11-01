<script setup lang="ts">
import { TabsRoot, TabsList, TabsTrigger, TabsContent, TabsIndicator } from 'reka-ui'
import type { MoeOption } from '../types'
const model = defineModel<string>()
withDefaults(defineProps<{ label: string; items: MoeOption[]; activationMode?: 'automatic' | 'manual'; variant?: 'segmented' | 'underline'; fullWidth?: boolean }>(), { activationMode: 'automatic', variant: 'segmented' })
</script>

<template>
  <TabsRoot v-model="model" :default-value="items.find(item => !item.disabled)?.value" :activation-mode="activationMode" class="moe-tabs" :data-variant="variant" :data-full-width="fullWidth">
    <TabsList :aria-label="label" class="moe-tabs-list">
      <TabsIndicator class="moe-tabs-indicator" aria-hidden="true" />
      <TabsTrigger v-for="item in items" :key="item.value" :value="item.value" :disabled="item.disabled" class="moe-tab moe-focus moe-disabled">{{ item.label }}</TabsTrigger>
    </TabsList>
    <TabsContent v-for="item in items" :key="item.value" :value="item.value" class="moe-tabs-content moe-focus py-5 text-sm leading-7 text-foreground"><slot :name="item.value" :item="item"><slot :item="item">{{ item.description }}</slot></slot></TabsContent>
  </TabsRoot>
</template>
