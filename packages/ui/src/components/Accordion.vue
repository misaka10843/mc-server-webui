<script setup lang="ts">
import { AccordionRoot, AccordionItem, AccordionHeader, AccordionTrigger, AccordionContent } from 'reka-ui'
import type { MoeAccordionItem } from '../types'
import Icon from './Icon.vue'
defineProps<{ items: MoeAccordionItem[]; disabled?: boolean }>()
const model = defineModel<string>()
</script>
<template><AccordionRoot v-model="model" type="single" collapsible :disabled="disabled" class="moe-accordion"><AccordionItem v-for="item in items" :key="item.value" :value="item.value" :disabled="item.disabled" class="moe-accordion-item"><AccordionHeader><AccordionTrigger class="moe-accordion-trigger moe-focus"><span>{{ item.title }}</span><Icon name="chevron-down" /></AccordionTrigger></AccordionHeader><AccordionContent class="moe-accordion-content"><div class="px-4 pb-4 text-sm leading-7 text-muted"><slot :name="item.value" :item="item">{{ item.description }}</slot></div></AccordionContent></AccordionItem></AccordionRoot></template>
