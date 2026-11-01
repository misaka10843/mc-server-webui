<script setup lang="ts">
import { apiFetch } from "./api"
import { computed, onMounted, onUnmounted, ref, watch } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeProgress from "@moetopia/ui/components/Progress"
import MoeProvider from "@moetopia/ui/components/Provider"
import MoeSteps from "@moetopia/ui/components/Steps"
import Console from "./Console.vue"
import Users from "./Users.vue"
import Policy from "./Policy.vue"
import LogViewer from "./LogViewer.vue"
import PlugSettings from "./PlugSettings.vue"

type User = { username: string; role: "admin" | "user" }
type Status = { host: string; container?: string; minecraft: string; minecraft_version?: string | null; neoforge_version?: string | null; mod_version?: string | null; plug: string; server_lan_address?: string; server_address?: string; operation?: Operation | null; shutdown?: string; shutdown_error?: string | null; policy_revision?: number | null; policy_enabled?: boolean; idle_since?: number | null; idle_policy?: {day_minutes:number; night_minutes:number; day_start:string; night_start:string; timezone:string}; online?: number | null; max_players?: number | null; players?: {name:string; uuid:string}[]; tps?: number | null; mspt?: number | null; memory_used?: number | null; memory_max?: number | null; host_cpu?: number | null; host_memory_used?: number | null; host_memory_max?: number | null; uptime_seconds?: number | null }
type Operation = { id: string; kind?: string; status: string; detail: string; created_at?: number }
const current = ref<User | null>(null)
const status = ref<Status>({ host: "unknown", minecraft: "unknown", plug: "unknown" })
const username = ref("")
const password = ref("")
const error = ref("")
const connected = ref(false)
let loggingOut = false
const theme = ref<"light" | "dark">("light")
const operation = ref<Operation | null>(null)
const starting = ref(false)
const logs = ref<string[]>([])
const steps = [{ value: "plug", label: "开启插座" }, { value: "host", label: "启动 Ubuntu" }, { value: "container", label: "启动容器" }, { value: "loading", label: "加载 Minecraft" }, { value: "ready", label: "可以加入" }]
const startStep = computed(() => status.value.minecraft === "ready" ? "ready" : status.value.host === "online" ? status.value.container === "running" ? "loading" : "container" : status.value.plug === "on" ? "host" : "plug")
const shutdownMessage = computed(() => {
  if (status.value.shutdown === "preparing" || status.value.shutdown === "poweroff_requested") return status.value.host === "online" ? "服务器正在正常关闭" : "主机已离线，等待插座自动断电"
  if (status.value.shutdown === "off") return "插座已断电"
  if (status.value.shutdown === "failed") return "自动关机未完成，请联系管理员检查"
  return ""
})
const clock = ref(Date.now())
let clockTimer: ReturnType<typeof setInterval> | undefined
const remaining = computed(() => {
  const policy = status.value.idle_policy
  const start = status.value.idle_since
  if (!status.value.policy_enabled || !policy || start == null) return null
  const offset = 8 * 3600000
  const dayMs = 86400000
  const minutes = (value: string) => { const [hour, minute] = value.split(":").map(Number); return hour * 60 + minute }
  const dayStart = minutes(policy.day_start)
  const nightStart = minutes(policy.night_start)
  let point = clock.value
  let deadline = point
  for (let i = 0; i < 4; i++) {
    const local = point + offset
    const midnight = Math.floor(local / dayMs) * dayMs
    const minute = Math.floor((local - midnight) / 60000)
    const night = minute >= nightStart || minute < dayStart
    const boundaryMinute = night ? (minute >= nightStart ? dayStart + 1440 : dayStart) : nightStart
    const boundary = midnight + boundaryMinute * 60000 - offset
    const threshold = (night ? policy.night_minutes : policy.day_minutes) * 60000
    deadline = Math.max(point, start * 1000 + threshold)
    if (deadline <= boundary) break
    point = boundary + 1
  }
  const seconds = Math.max(0, Math.ceil((deadline - clock.value) / 1000))
  return `${Math.floor(seconds / 60)} 分 ${seconds % 60} 秒`
})
let source: EventSource | undefined

function subscribe() {
  source?.close()
  source = new EventSource("/api/v1/events")
  source.addEventListener("status", event => { status.value = JSON.parse((event as MessageEvent).data); if (status.value.operation) operation.value = status.value.operation })
  source.addEventListener("operation", event => {
    const value: Operation = JSON.parse((event as MessageEvent).data)
    if (operation.value?.id === value.id) operation.value = value
  })
  source.addEventListener("log", event => {
    logs.value.push(JSON.parse((event as MessageEvent).data).line)
    if (logs.value.length > 5000) logs.value.splice(0, logs.value.length - 5000)
  })
  source.addEventListener("session", () => { source?.close(); current.value = null; connected.value = false; if (!loggingOut) error.value = "会话已失效，请重新登录" })
  source.onopen = () => { connected.value = true }
  source.onerror = () => { connected.value = false }
}
async function lifecycle(path: string) {
  starting.value = true
  error.value = ""
  try {
    const response = await apiFetch(`/api/v1/${path}`, { method: "POST" })
    const result = await response.json()
    if (!response.ok) throw new Error(result.detail ?? "启动请求失败")
    const currentOperation = await apiFetch(`/api/v1/operations/${result.id}`)
    if (!currentOperation.ok) throw new Error("无法获取启动状态")
    operation.value = await currentOperation.json()
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { starting.value = false }
}
function shutdownServer() {
  if (window.confirm("确定关闭服务器和主机？有玩家时将先在游戏内广播 60 秒。")) lifecycle("admin/server/shutdown")
}
async function copyAddress(address: string) {
  try {
    await navigator.clipboard.writeText(address)
  } catch {
    error.value = "浏览器无法复制，请手动选择地址"
  }
}
async function loadUser() {
  const response = await apiFetch("/api/v1/auth/me")
  if (response.ok) { current.value = await response.json(); subscribe(); loadLogs() }
}
async function loadLogs() {
  if (current.value?.role !== "admin") return
  const response = await apiFetch("/api/v1/admin/logs")
  if (response.ok) logs.value = (await response.json()).lines
}
async function login() {
  error.value = ""
  const response = await apiFetch("/api/v1/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username: username.value, password: password.value }) })
  if (!response.ok) { error.value = "登录失败，请检查账户和密码"; return }
  password.value = ""
  current.value = await response.json()
  subscribe()
  loadLogs()
}
async function logout() {
  loggingOut = true
  try {
    const response = await apiFetch("/api/v1/auth/logout", { method: "POST" })
    if (response.ok) { source?.close(); current.value = null; connected.value = false; error.value = "" }
  } finally { loggingOut = false }
}
const names: Record<string, string> = { unknown: "未知", online: "在线", offline: "离线", starting: "启动中", ready: "可以加入", on: "供电中", off: "已断电" }
function label(value: string) { return names[value] ?? value }
watch(theme, value => { document.documentElement.dataset.theme = value; localStorage.setItem("mcweb-theme", value) })
onMounted(() => { theme.value = localStorage.getItem("mcweb-theme") === "dark" ? "dark" : "light"; document.documentElement.dataset.theme = theme.value; loadUser(); clockTimer = setInterval(() => { clock.value = Date.now() }, 1000) })
onUnmounted(() => { source?.close(); if (clockTimer) clearInterval(clockTimer) })
</script>

<template>
  <MoeProvider><main class="app-shell">
    <header><div><p class="eyebrow">MINECRAFT SERVER</p><h1>服务器控制台</h1><p>查看服务器状态与运行情况</p></div><div class="header-actions"><MoeButton variant="light" @click="theme = theme === 'light' ? 'dark' : 'light'">{{ theme === 'light' ? '深色' : '浅色' }}</MoeButton><MoeButton v-if="current" variant="bordered" @click="logout">退出登录</MoeButton></div></header>
    <MoeCard v-if="!current" class="login-card">
      <form @submit.prevent="login"><h2>登录</h2><p>使用管理员提供的账户继续。</p><MoeInput v-model="username" label="用户名" autocomplete="username" required /><MoeInput v-model="password" label="密码" type="password" autocomplete="current-password" required /><p v-if="error" role="alert" class="error">{{ error }}</p><MoeButton type="submit">登录</MoeButton></form>
    </MoeCard>
    <template v-else>
      <p class="connection" role="status">{{ connected ? "实时连接正常" : "实时连接中断，正在重连" }} · {{ current.username }}</p>
      <section class="status-grid" aria-label="服务器状态">
        <MoeCard><p>Ubuntu 主机</p><h2>{{ label(status.host) }}</h2></MoeCard>
        <MoeCard><p>Minecraft</p><h2>{{ label(status.minecraft) }}</h2></MoeCard>
        <MoeCard><p>智能插座</p><h2>{{ label(status.plug) }}</h2></MoeCard>
      </section>
      <MoeCard v-if="status.server_lan_address || status.server_address" class="notice"><h2>游戏连接地址</h2><div v-if="status.server_lan_address"><p>局域网：{{ status.server_lan_address }}</p><MoeButton variant="bordered" @click="copyAddress(status.server_lan_address)">复制局域网地址</MoeButton></div><div v-if="status.server_address"><p>公网：{{ status.server_address }}</p><MoeButton variant="bordered" @click="copyAddress(status.server_address)">复制公网地址</MoeButton></div><p v-else>外网玩家请使用管理员提供的游戏连接地址。</p></MoeCard>
      <MoeCard class="notice"><h2>运行状态</h2><p>在线玩家：{{ status.online ?? '未知' }} / {{ status.max_players ?? '未知' }}<span v-if="status.players?.length"> · {{ status.players.map(player => player.name).join('、') }}</span></p><p>TPS：{{ status.tps ?? '未知' }} · MSPT：{{ status.mspt ?? '未知' }} · JVM 内存：{{ status.memory_used != null ? `${Math.round(status.memory_used / 1048576)} / ${Math.round((status.memory_max ?? 0) / 1048576)} MiB` : '未知' }}</p><p>主机 CPU：{{ status.host_cpu == null ? '未知' : `${status.host_cpu}%` }} · 主机内存：{{ status.host_memory_used != null ? `${Math.round(status.host_memory_used / 1048576)} / ${Math.round((status.host_memory_max ?? 0) / 1048576)} MiB` : '未知' }} · 运行时长：{{ status.uptime_seconds != null ? `${Math.floor(status.uptime_seconds / 60)} 分钟` : '未知' }}</p><p v-if="status.minecraft_version">Minecraft {{ status.minecraft_version }} · NeoForge {{ status.neoforge_version }} · Command API {{ status.mod_version }}</p><p v-if="remaining !== null">预计 {{ remaining }} 后进入关机流程</p></MoeCard>
      <MoeCard class="notice"><h2>服务器电源</h2><p v-if="operation?.status === 'running'" role="status">{{ operation.detail }}<span v-if="operation.created_at"> · 已用时 {{ Math.max(0, Math.floor((clock / 1000 - operation.created_at) / 60)) }} 分钟</span></p><p v-else-if="shutdownMessage" role="status">{{ shutdownMessage }}</p><p v-else-if="operation" role="status">{{ operation.detail }}</p><p v-else>按需启动服务器，启动可能需要几分钟。</p><MoeSteps v-if="operation?.kind === 'start' && operation.status === 'running'" label="启动阶段" :items="steps" :current="startStep" /><MoeProgress v-if="operation?.status === 'running'" label="正在处理" :value="null" /><p v-if="error" role="alert" class="error">{{ error }}</p><MoeButton :disabled="starting || operation?.status === 'running' || status.minecraft === 'ready' || status.shutdown === 'preparing' || status.shutdown === 'poweroff_requested'" @click="lifecycle('server/start')">{{ starting || operation?.status === 'running' ? '操作进行中' : '启动服务器' }}</MoeButton> <MoeButton v-if="current.role === 'admin'" color="danger" variant="bordered" :disabled="starting || operation?.status === 'running' || status.minecraft !== 'ready'" @click="shutdownServer">关闭服务器</MoeButton></MoeCard>
      <Console v-if="current.role === 'admin'" />
      <Policy v-if="current.role === 'admin'" :applied-revision="status.policy_revision" :effective-enabled="status.policy_enabled" :shutdown-state="status.shutdown" :shutdown-error="status.shutdown_error" />
      <PlugSettings v-if="current.role === 'admin'" />
      <LogViewer v-if="current.role === 'admin'" :lines="logs" @reload="loadLogs" />
      <Users :is-admin="current.role === 'admin'" />
    </template>
  </main></MoeProvider>
</template>
