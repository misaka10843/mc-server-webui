<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
const props = defineProps<{ lines: string[] }>()
const emit = defineEmits<{ reload: [] }>()
const filter = ref("")
const paused = ref(false)
const area = ref<HTMLDivElement | null>(null)
const scrollTop = ref(0)
const rowHeight = 22
const viewHeight = 330
const filtered = computed(() => props.lines.filter(line => line.includes(filter.value)))
const first = computed(() => Math.max(0, Math.floor(scrollTop.value / rowHeight) - 5))
const visible = computed(() => filtered.value.slice(first.value, first.value + Math.ceil(viewHeight / rowHeight) + 10))
const top = computed(() => first.value * rowHeight)
const bottom = computed(() => Math.max(0, (filtered.value.length - first.value - visible.value.length) * rowHeight))
function onScroll() { scrollTop.value = area.value?.scrollTop ?? 0 }
watch(() => filtered.value.length, async () => {
  if (!paused.value) {
    await nextTick()
    if (area.value) { area.value.scrollTop = area.value.scrollHeight; onScroll() }
  }
})
</script>
<template>
  <MoeCard class="notice"><h2>服务器日志</h2><div class="log-controls"><label>筛选 <input v-model="filter" type="search" /></label><label><input v-model="paused" type="checkbox" /> 暂停自动滚动</label><MoeButton variant="bordered" @click="emit('reload')">加载最近日志</MoeButton></div>
    <div ref="area" class="console-output log-viewport" role="log" aria-label="服务器日志" @scroll="onScroll"><div :style="{height: `${top}px`}"></div><div v-for="(line, index) in visible" :key="first + index" class="log-line">{{ line }}</div><div :style="{height: `${bottom}px`}"></div></div>
  </MoeCard>
</template>
