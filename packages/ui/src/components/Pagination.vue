<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { PaginationRoot, PaginationList, PaginationListItem, PaginationEllipsis, PaginationPrev, PaginationNext } from 'reka-ui'
import Icon from './Icon.vue'
const props = withDefaults(defineProps<{ total: number; pageSize?: number; disabled?: boolean; label?: string; previousLabel?: string; nextLabel?: string; pageLabel?: (page: number) => string; showJump?: boolean; jumpLabel?: string; jumpActionLabel?: string }>(), { pageSize: 10, label: '分页', previousLabel: '上一页', nextLabel: '下一页', pageLabel: (page: number) => `第 ${page} 页`, showJump: true, jumpLabel: '跳转到页数', jumpActionLabel: '跳转' })
const page = defineModel<number>('page', { default: 1 })
const list = ref<HTMLDivElement>()
const indicator = ref<Record<string, string>>()
const jump = ref('')
const pageCount = computed(() => Math.ceil(props.total / props.pageSize))
let observer: ResizeObserver | undefined
const measure = () => {
  const target = list.value?.querySelector<HTMLElement>('[aria-current="page"]')
  indicator.value = target ? { transform: `translate(${target.offsetLeft}px, ${target.offsetTop}px)`, width: `${target.offsetWidth}px`, height: `${target.offsetHeight}px` } : undefined
}
const jumpToPage = () => {
  const target = Number(jump.value)
  if (!props.disabled && Number.isInteger(target) && target >= 1 && target <= pageCount.value) { page.value = target; jump.value = '' }
}
watch(() => [page.value, props.total, props.pageSize], () => nextTick(measure), { flush: 'post' })
onMounted(() => { measure(); observer = new ResizeObserver(measure); if (list.value) observer.observe(list.value) })
onBeforeUnmount(() => observer?.disconnect())
</script>
<template>
  <PaginationRoot v-model:page="page" :total="total" :items-per-page="pageSize" :sibling-count="0" show-edges :disabled="disabled" :aria-label="label" class="moe-pagination">
    <PaginationList v-slot="{ items }" as-child>
      <div ref="list" class="moe-page-list" :data-indicator-ready="!!indicator">
        <span v-if="indicator" class="moe-page-indicator" :style="indicator" aria-hidden="true" />
        <PaginationPrev class="moe-page-button moe-focus" :aria-label="previousLabel"><Icon name="chevron-left" /></PaginationPrev>
        <template v-for="(item, index) in items" :key="index">
          <PaginationListItem v-if="item.type === 'page'" :value="item.value" class="moe-page-button moe-focus" :aria-label="pageLabel(item.value)">{{ item.value }}</PaginationListItem>
          <PaginationEllipsis v-else class="moe-page-ellipsis" aria-hidden="true">…</PaginationEllipsis>
        </template>
        <PaginationNext class="moe-page-button moe-focus" :aria-label="nextLabel"><Icon name="chevron-right" /></PaginationNext>
      </div>
    </PaginationList>
    <form v-if="showJump && pageCount > 1" class="moe-page-jump" @submit.prevent="jumpToPage"><input v-model="jump" type="number" min="1" :max="pageCount" step="1" :aria-label="jumpLabel" :disabled="disabled" :placeholder="`1–${pageCount}`" class="moe-focus" /><button type="submit" :disabled="disabled || !jump" class="moe-page-button moe-focus">{{ jumpActionLabel }}</button></form>
  </PaginationRoot>
</template>
