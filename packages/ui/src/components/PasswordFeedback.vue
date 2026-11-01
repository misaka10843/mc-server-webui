<script setup lang="ts">
import { computed, ref, watch, onBeforeUnmount } from 'vue'
import { loadPasswordEstimator } from '../password-strength'
import Icon from './Icon.vue'
const props = defineProps<{
  value: string
  minLength: number
  maxBytes: number
  labels: { title: string; minimum: string; maximum: string; policyHint: string; strength: string; levels: string[]; suggestion: string; checking: string; unavailable: string }
}>()
const length = computed(() => Array.from(props.value).length)
const bytes = computed(() => new TextEncoder().encode(props.value).length)
const score = ref<number>()
const failed = ref(false)
let generation = 0
let timer: ReturnType<typeof setTimeout> | undefined
watch(() => props.value, value => {
  const current = ++generation
  clearTimeout(timer); score.value = undefined; failed.value = false
  if (!value || new TextEncoder().encode(value).length > props.maxBytes) return
  timer = setTimeout(async () => {
    try {
      const engine = await loadPasswordEstimator()
      if (generation !== current) return
      score.value = engine.check(value).score
    } catch { if (generation === current) failed.value = true }
  }, 180)
}, { immediate: true })
onBeforeUnmount(() => { generation++; clearTimeout(timer); score.value = undefined })
const rules = computed(() => [
  { label: props.labels.minimum, met: length.value >= props.minLength, count: `${length.value}/${props.minLength}` },
  { label: props.labels.maximum, met: bytes.value <= props.maxBytes, count: `${bytes.value}/${props.maxBytes}` },
])
</script>
<template>
  <section class="moe-password-feedback" :aria-label="labels.title">
    <ul class="grid gap-2"><li v-for="rule in rules" :key="rule.label" class="flex items-center gap-2 text-xs" :class="rule.met ? 'text-primary' : 'text-muted'"><Icon :name="rule.met ? 'check' : 'close'" class="size-3.5 shrink-0" /><span class="flex-1">{{ rule.label }}</span><span class="tabular-nums">{{ rule.count }}</span></li></ul>
    <p class="text-xs leading-5 text-muted">{{ labels.policyHint }}</p>
    <template v-if="value && bytes <= maxBytes">
      <div class="flex items-center justify-between gap-3 text-xs" role="status" aria-live="polite"><span>{{ labels.strength }}</span><span>{{ failed ? labels.unavailable : score === undefined ? labels.checking : labels.levels[score] }}</span></div>
      <meter v-if="score !== undefined" min="0" max="4" low="2" high="3" optimum="4" :value="score" :aria-label="labels.strength" class="h-2 w-full" />
      <p v-if="score !== undefined && score < 3" class="text-xs leading-5 text-muted">{{ labels.suggestion }}</p>
    </template>
  </section>
</template>
