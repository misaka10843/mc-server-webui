<script setup lang="ts">
import { onMounted, ref } from "vue"
import MoeAlert from "@moetopia/ui/components/Alert"
import MoeBadge from "@moetopia/ui/components/Badge"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeNumberInput from "@moetopia/ui/components/NumberInput"
import MoeSettingRow from "@moetopia/ui/components/SettingRow"
import MoeSwitch from "@moetopia/ui/components/Switch"
import { apiRequest } from "./api"

const props = defineProps<{ appliedRevision?: number | null; effectiveEnabled?: boolean; shutdownState?: string; shutdownError?: string | null }>()
type Policy = { revision: number; enabled: boolean; day_minutes: number; night_minutes: number; night_start: string; day_start: string }
const policy = ref<Policy | null>(null)
const busy = ref(false)
const error = ref("")
const message = ref("")
async function load() {
  try { const result = await apiRequest<Policy>("/api/v1/admin/policy"); policy.value = { ...result, enabled: Boolean(result.enabled) } }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
async function save() {
  if (!policy.value) return
  busy.value = true; error.value = ""; message.value = ""
  try {
    const result = await apiRequest<Policy & { applied: boolean }>("/api/v1/admin/policy", { method: "PUT", body: JSON.stringify(policy.value) })
    policy.value = { ...result, enabled: Boolean(result.enabled) }
    message.value = result.applied ? "关机计划已生效。" : "计划已保存，连接笔记本后生效。"
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
onMounted(load)
</script>
<template>
  <MoeCard title="空闲关机计划" description="仅在 Minecraft 持续无人时执行。有人加入或连接中断时重新计时。" padding="lg"><form v-if="policy" @submit.prevent="save"><MoeSettingRow title="启用自动关机" description="按香港时间（UTC+8）执行，空闲计时由 NAS 管理。"><template #actions><MoeSwitch v-model="policy.enabled" label="启用自动关机" /></template></MoeSettingRow><div class="form-grid"><MoeInput v-model="policy.night_start" label="夜间开始" type="time" required /><MoeNumberInput v-model="policy.night_minutes" label="夜间无人多久后关机（分钟）" :min="1" :max="1440" /><MoeInput v-model="policy.day_start" label="白天开始" type="time" required /><MoeNumberInput v-model="policy.day_minutes" label="白天无人多久后关机（分钟）" :min="1" :max="1440" /></div><p class="panel-note">例如 23:30 至次日 09:00 使用夜间时长。跨日夜边界仍保留已累计的空闲时间。</p><div class="form-actions"><MoeButton type="submit" :disabled="busy">{{ busy ? '正在保存…' : '保存关机计划' }}</MoeButton><MoeBadge :color="props.effectiveEnabled ? 'success' : 'default'">{{ props.effectiveEnabled ? '自动关机已启用' : '自动关机未启用' }}</MoeBadge></div></form><MoeAlert v-if="props.shutdownState === 'failed'" class="form-message" title="上次关机未完成，计时已暂停" color="warning">{{ props.shutdownError }}。处理原因后重新保存计划即可恢复。</MoeAlert><MoeAlert v-if="error" class="form-message" title="计划未保存" color="danger" announce>{{ error }}</MoeAlert><MoeAlert v-else-if="message" class="form-message" :title="message" color="success" announce /></MoeCard>
</template>
