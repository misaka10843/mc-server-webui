<script setup lang="ts">
import { apiFetch } from "./api"
import { onMounted, ref } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"

const props = defineProps<{ appliedRevision?: number | null; effectiveEnabled?: boolean; shutdownState?: string; shutdownError?: string | null }>()
type Policy = { revision: number; enabled: boolean; day_minutes: number; night_minutes: number; night_start: string; day_start: string }
const policy = ref<Policy | null>(null)
const error = ref("")
const saved = ref("")
async function load() {
  const response = await apiFetch("/api/v1/admin/policy")
  if (response.ok) { const value = await response.json(); policy.value = { ...value, enabled: Boolean(value.enabled) } }
}
async function save() {
  if (!policy.value) return
  error.value = ""; saved.value = ""
  const response = await apiFetch("/api/v1/admin/policy", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(policy.value) })
  const result = await response.json()
  if (!response.ok) { error.value = result.detail ?? "保存失败"; return }
  policy.value = { ...result, enabled: Boolean(result.enabled) }
  saved.value = result.applied ? "策略已发送给主机" : "策略已保存，等待主机同步"
}
onMounted(load)
</script>
<template>
  <MoeCard v-if="policy" class="notice"><h2>空闲关机策略</h2><p>香港时间；无人时间跨时段连续计算。主机需完成部署配置后才能启用。</p>
    <form class="policy-form" @submit.prevent="save"><label><input v-model="policy.enabled" type="checkbox" /> 启用自动关机</label><label>白天空闲（分钟）<input v-model.number="policy.day_minutes" type="number" min="1" max="1440" required /></label><label>夜间空闲（分钟）<input v-model.number="policy.night_minutes" type="number" min="1" max="1440" required /></label><label>夜间开始 <input v-model="policy.night_start" type="time" required /></label><label>白天开始 <input v-model="policy.day_start" type="time" required /></label><MoeButton type="submit">保存策略</MoeButton></form>
    <p role="status">{{ saved }} <span v-if="props.appliedRevision === policy.revision">· 已同步主机，自动关机{{ props.effectiveEnabled ? (props.shutdownState === 'failed' ? '已暂停' : '已启用') : '未启用' }}</span><span v-else>· 等待主机同步</span></p><p v-if="props.shutdownState === 'failed'" class="error" role="alert">{{ props.shutdownError || '上次关机失败' }}。请处理原因后重新保存策略。</p><p v-if="error" class="error" role="alert">{{ error }}</p>
  </MoeCard>
</template>
