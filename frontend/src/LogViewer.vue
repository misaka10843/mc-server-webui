<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeSwitch from "@moetopia/ui/components/Switch"
const props = defineProps<{ lines: string[] }>()
const emit = defineEmits<{ reload: [] }>()
const filter = ref("")
const paused = ref(false)
const area = ref<HTMLDivElement | null>(null)
const scrollTop = ref(0)
const rowHeight = 22
const viewHeight = 402
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
  <MoeCard title="实时日志" description="仅在此页面订阅日志，最多保留最近 5000 行。"><div class="log-controls"><MoeInput v-model="filter" label="筛选日志" type="search" placeholder="输入关键词" /><MoeSwitch v-model="paused" label="暂停滚动" /><MoeButton variant="bordered" color="default" @click="emit('reload')">加载最近日志</MoeButton></div>
    <div ref="area" class="console-output log-viewport" role="log" aria-label="服务器日志" @scroll="onScroll"><div :style="{height: `${top}px`}"></div><div v-for="(line, index) in visible" :key="first + index" class="log-line">{{ line }}</div><div :style="{height: `${bottom}px`}"></div></div>
    <p class="panel-note" style="margin-top:12px">{{ filtered.length }} 行{{ filter ? '匹配' : '日志' }} · {{ paused ? '已暂停自动滚动，仍在接收日志' : '自动跟随最新日志' }}</p>
  </MoeCard>
</template>
