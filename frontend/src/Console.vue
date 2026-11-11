<script setup lang="ts">
import { apiFetch } from "./api"
import { ref, watch, onUnmounted, nextTick } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"

type Suggestion = { text: string; start: number; end: number; tooltip?: string }
const input = ref("")
const entries = ref<Suggestion[]>([])
const active = ref(0)
const lines = ref<string[]>([])
const history = ref<string[]>([])
const historyIndex = ref(0)
const field = ref<InstanceType<typeof MoeInput> | null>(null)
function inputElement(): HTMLInputElement | undefined { return field.value?.$el.querySelector('input') }
const sending = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined
let requestNumber = 0
const composing = ref(false)

async function request(path: string, payload: object) {
  const response = await apiFetch(`/api/v1/admin/${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
  const result = await response.json()
  if (!response.ok) throw new Error(result.detail ?? "请求失败")
  return result
}
function completeLater() {
  if (timer) clearTimeout(timer)
  const seq = ++requestNumber
  if (composing.value || !input.value) { entries.value = []; return }
  timer = setTimeout(async () => {
    try {
      const cursor = inputElement()?.selectionStart ?? input.value.length
      const result = await request("completions", { input: input.value, cursor })
      if (seq === requestNumber) { entries.value = result.suggestions; active.value = 0 }
    } catch { if (seq === requestNumber) entries.value = [] }
  }, 150)
}
watch(input, completeLater)
onUnmounted(() => { if (timer) clearTimeout(timer); requestNumber++ })
function apply() {
  const item = entries.value[active.value]
  if (!item) return
  input.value = input.value.slice(0, item.start) + item.text + input.value.slice(item.end)
  entries.value = []
  nextTick(() => { inputElement()?.focus(); inputElement()?.setSelectionRange(item.start + item.text.length, item.start + item.text.length) })
}
async function send() {
  const value = input.value.trim()
  if (!value || sending.value || composing.value) return
  entries.value = []
  input.value = ""
  history.value.push(value)
  historyIndex.value = history.value.length
  lines.value.push(`> ${value}`)
  sending.value = true
  try {
    const result = await request("commands", { input: value })
    lines.value.push(...result.output)
  } catch (error) { lines.value.push(`请求失败：${error instanceof Error ? error.message : String(error)}`) }
  finally { sending.value = false; lines.value = lines.value.slice(-500) }
}
function keydown(event: KeyboardEvent) {
  if (composing.value || event.isComposing) return
  if (event.key === "Escape") { entries.value = []; return }
  if (entries.value.length && ["Tab", "ArrowDown", "ArrowUp"].includes(event.key)) {
    event.preventDefault()
    if (event.key === "Tab") { if (event.shiftKey) active.value = (active.value - 1 + entries.value.length) % entries.value.length; apply(); return }
    active.value = (active.value + (event.key === "ArrowDown" ? 1 : -1) + entries.value.length) % entries.value.length
  } else if (event.key === "Enter" && entries.value.length) { event.preventDefault(); apply() }
  else if (event.key === "Enter") { event.preventDefault(); send() }
  else if (["ArrowUp", "ArrowDown"].includes(event.key) && history.value.length) {
    event.preventDefault()
    historyIndex.value = Math.max(0, Math.min(history.value.length, historyIndex.value + (event.key === "ArrowUp" ? -1 : 1)))
    input.value = history.value[historyIndex.value] ?? ""
  }
}
</script>

<template>
  <MoeCard class="console" title="命令终端" description="以服务器控制台身份执行。Tab 补全，↑ ↓ 选择候选或历史命令。">
    <div class="console-output" role="log" aria-label="命令输出"><div v-for="(line, index) in lines" :key="index">{{ line }}</div></div>
    <div class="console-input"><MoeInput id="command-input" ref="field" v-model="input" label="输入命令" placeholder="例如 list、say 服务器即将休息" autocomplete="off" @keydown="keydown" @compositionstart="composing = true" @compositionend="composing = false; completeLater()" @click="completeLater" />
      <MoeButton :disabled="sending || !input.trim()" @click="send">发送</MoeButton>
    </div>
    <ul v-if="entries.length" class="suggestions" role="listbox" aria-label="命令建议"><li v-for="(item, index) in entries" :key="`${item.start}-${item.end}-${item.text}`" :aria-selected="index === active" role="option" @mousedown.prevent="active = index; apply()">{{ item.text }} <small v-if="item.tooltip">{{ item.tooltip }}</small></li></ul>
  </MoeCard>
</template>
