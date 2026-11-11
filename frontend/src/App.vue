<script setup lang="ts">
import { computed, defineAsyncComponent, onMounted, onUnmounted, ref, watch } from "vue"
import type { MoeNavGroup, MoeNavItem } from "@moetopia/ui/types"
import MoeAlert from "@moetopia/ui/components/Alert"
import MoeBadge from "@moetopia/ui/components/Badge"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeDialog from "@moetopia/ui/components/Dialog"
import MoeEmptyState from "@moetopia/ui/components/EmptyState"
import MoeIcon from "@moetopia/ui/components/Icon"
import MoeInput from "@moetopia/ui/components/Input"
import MoePageHeading from "@moetopia/ui/components/PageHeading"
import MoeProgress from "@moetopia/ui/components/Progress"
import MoeProvider from "@moetopia/ui/components/Provider"
import MoeSidebar from "@moetopia/ui/components/Sidebar"
import MoeSteps from "@moetopia/ui/components/Steps"
import MoeTabs from "@moetopia/ui/components/Tabs"
import { apiFetch, apiRequest } from "./api"

const Console = defineAsyncComponent(() => import("./Console.vue"))
const LogViewer = defineAsyncComponent(() => import("./LogViewer.vue"))
const PlugSettings = defineAsyncComponent(() => import("./PlugSettings.vue"))
const Policy = defineAsyncComponent(() => import("./Policy.vue"))
const SSHSettings = defineAsyncComponent(() => import("./SSHSettings.vue"))
const Users = defineAsyncComponent(() => import("./Users.vue"))

type User = { username: string; role: "admin" | "user" }
type Operation = { id: string; kind?: string; status: string; detail: string; created_at?: number }
type Status = {
  host: string; container?: string; minecraft: string; plug: string
  ssh_configured?: boolean; plug_configured?: boolean; ssh_error?: string | null; mod_error?: string | null
  server_lan_address?: string; server_address?: string; operation?: Operation | null
  shutdown?: string; shutdown_error?: string | null; policy_revision?: number | null; policy_enabled?: boolean
  idle_since?: number | null; idle_policy?: { day_minutes: number; night_minutes: number; day_start: string; night_start: string; timezone: string }
  online?: number | null; max_players?: number | null; players?: { name: string; uuid: string }[]
  tps?: number | null; mspt?: number | null; memory_used?: number | null; memory_max?: number | null; uptime_seconds?: number | null
  minecraft_version?: string | null; neoforge_version?: string | null; mod_version?: string | null
}

const current = ref<User | null>(null)
const status = ref<Status>({ host: "unknown", minecraft: "unknown", plug: "unknown" })
const operation = ref<Operation | null>(null)
const page = ref("overview")
const consoleTab = ref("logs")
const username = ref("")
const password = ref("")
const setupRequired = ref(false)
const initializing = ref(true)
const authBusy = ref(false)
const busy = ref(false)
const refreshing = ref(false)
const error = ref("")
const notice = ref("")
const connected = ref(false)
const confirmShutdown = ref(false)
const logs = ref<string[]>([])
const theme = ref<"light" | "dark">("light")
const clock = ref(Date.now())
let source: EventSource | undefined
let clockTimer: ReturnType<typeof setInterval> | undefined
let loggingOut = false

const admin = computed(() => current.value?.role === "admin")
const navigation = computed<MoeNavGroup[]>(() => [
  { label: "服务器", items: [
    { id: "overview", label: "服务器概览", icon: "home", href: "#overview" },
    ...(admin.value ? [{ id: "console", label: "日志与命令", icon: "code" as const, href: "#console" }] : []),
  ] },
  ...(admin.value ? [{ label: "管理", items: [
    { id: "connections", label: "连接设置", icon: "grid" as const, href: "#connections" },
    { id: "automation", label: "自动关机", icon: "moon" as const, href: "#automation" },
    { id: "accounts", label: "账户与审计", icon: "user" as const, href: "#accounts" },
  ] }] : []),
  { label: "个人", items: [{ id: "account", label: "我的账户", icon: "settings", href: "#account" }] },
])
const headings: Record<string, { title: string; description: string }> = {
  overview: { title: "服务器概览", description: "你的世界，现在是什么状态？" },
  console: { title: "日志与命令", description: "实时查看运行日志，像游戏里一样执行命令。" },
  connections: { title: "连接设置", description: "连接笔记本和智能插座，后续操作都在这里完成。" },
  automation: { title: "自动关机", description: "有人时安心游玩，无人时按你的计划休息。" },
  accounts: { title: "账户与审计", description: "邀请朋友开服，管理权限和操作记录。" },
  account: { title: "我的账户", description: "管理你的登录密码。" },
}
const heading = computed(() => headings[page.value])
const running = computed(() => operation.value?.status === "running")
const shuttingDown = computed(() => ["preparing", "poweroff_requested"].includes(status.value.shutdown ?? ""))
const needsSetup = computed(() => status.value.ssh_configured === false || status.value.plug_configured === false)
const ready = computed(() => status.value.minecraft === "ready")
const startDisabled = computed(() => busy.value || running.value || ready.value || shuttingDown.value || needsSetup.value || !connected.value)
const startStep = computed(() => ready.value ? "ready" : status.value.host === "online" ? status.value.container === "running" ? "loading" : "container" : status.value.plug === "on" ? "host" : "plug")
const steps = [{ value: "plug", label: "插座供电" }, { value: "host", label: "笔记本上线" }, { value: "container", label: "启动容器" }, { value: "loading", label: "加载世界" }, { value: "ready", label: "可以加入" }]
const summary = computed(() => {
  if (needsSetup.value) return { title: "先完成连接设置", text: admin.value ? "配置笔记本 SSH 和智能插座，就可以开始使用。" : "管理员完成连接设置后，即可在这里开服。" }
  if (shuttingDown.value) return { title: "服务器正在休息", text: status.value.host === "online" ? "正在保存世界并正常关闭，请稍候。" : "关机请求已发送，等待主机和插座完成关闭。" }
  if (running.value) return { title: "正在准备你的世界", text: operation.value!.detail }
  if (ready.value) return { title: "世界已就绪", text: "服务器运行中，复制连接地址就可以加入。" }
  if (status.value.host === "online") return { title: "笔记本已上线", text: "Minecraft 正在准备中，可以在日志页面查看进度。" }
  if (status.value.shutdown === "off" || status.value.plug === "off") return { title: "服务器已休息", text: "准备好继续冒险了吗？点击开服即可唤醒服务器。" }
  return { title: "随时准备开服", text: "启动后会依次开启插座、连接笔记本并加载世界。" }
})
const elapsed = computed(() => operation.value?.created_at ? `${Math.floor(Math.max(0, clock.value / 1000 - operation.value.created_at) / 60)} 分钟` : "")
const memory = computed(() => status.value.memory_used == null ? "—" : `${(status.value.memory_used / 1073741824).toFixed(1)} GB`)
const memoryPercent = computed(() => status.value.memory_used != null && status.value.memory_max ? Math.min(100, status.value.memory_used / status.value.memory_max * 100) : 0)
const uptime = computed(() => status.value.uptime_seconds == null ? "—" : status.value.uptime_seconds < 3600 ? `${Math.floor(status.value.uptime_seconds / 60)} 分钟` : `${Math.floor(status.value.uptime_seconds / 3600)} 小时 ${Math.floor(status.value.uptime_seconds % 3600 / 60)} 分`)
const remaining = computed(() => {
  const policy = status.value.idle_policy
  const start = status.value.idle_since
  if (!status.value.policy_enabled || !policy || start == null || status.value.shutdown === "failed") return null
  const minutes = (value: string) => { const [hour, minute] = value.split(":").map(Number); return hour * 60 + minute }
  const dayStart = minutes(policy.day_start), nightStart = minutes(policy.night_start)
  let point = clock.value, deadline = point
  for (let index = 0; index < 4; index++) {
    const local = point + 28800000, midnight = Math.floor(local / 86400000) * 86400000
    const minute = Math.floor((local - midnight) / 60000), night = minute >= nightStart || minute < dayStart
    const boundary = midnight + (night ? minute >= nightStart ? dayStart + 1440 : dayStart : nightStart) * 60000 - 28800000
    deadline = Math.max(point, start * 1000 + (night ? policy.night_minutes : policy.day_minutes) * 60000)
    if (deadline <= boundary) break
    point = boundary + 1
  }
  const seconds = Math.max(0, Math.ceil((deadline - clock.value) / 1000))
  return `${Math.floor(seconds / 60)} 分 ${seconds % 60} 秒`
})
const names: Record<string, string> = { unknown: "未确认", online: "已连接", offline: "离线", starting: "加载中", ready: "运行中", on: "供电中", off: "已断电", running: "运行中", exited: "已停止", created: "待启动", paused: "已暂停" }
function label(value?: string) { return value ? names[value] ?? value : "未确认" }

function navigate(event: MouseEvent, item: MoeNavItem) { event.preventDefault(); page.value = item.id; error.value = ""; notice.value = "" }
function subscribe() {
  source?.close()
  connected.value = false
  source = new EventSource(`/api/v1/events?logs=${admin.value && page.value === "console"}`)
  source.addEventListener("status", event => { status.value = JSON.parse((event as MessageEvent).data); operation.value = status.value.operation ?? null })
  source.addEventListener("operation", event => { operation.value = JSON.parse((event as MessageEvent).data) })
  source.addEventListener("log", event => {
    logs.value.push(JSON.parse((event as MessageEvent).data).line)
    if (logs.value.length > 5000) logs.value.splice(0, logs.value.length - 5000)
  })
  source.addEventListener("session", () => {
    source?.close(); current.value = null; connected.value = false; logs.value = []
    if (!loggingOut) error.value = "登录已失效，请重新登录"
  })
  source.onopen = () => { connected.value = true }
  source.onerror = () => { connected.value = false }
}
async function lifecycle(path: string) {
  busy.value = true; error.value = ""; notice.value = ""
  try {
    const result = await apiRequest<{ id: string }>(`/api/v1/${path}`, { method: "POST" })
    operation.value = await apiRequest<Operation>(`/api/v1/operations/${result.id}`)
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false; confirmShutdown.value = false }
}
async function refreshPlug() {
  refreshing.value = true; error.value = ""; notice.value = ""
  try { await apiRequest("/api/v1/server/plug/refresh", { method: "POST" }); notice.value = "插座状态已更新" }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { refreshing.value = false }
}
async function copyAddress(address: string) {
  try { await navigator.clipboard.writeText(address); notice.value = "游戏地址已复制" }
  catch { notice.value = `请手动复制：${address}` }
}
async function loadLogs() {
  try { logs.value = (await apiRequest<{ lines: string[] }>("/api/v1/admin/logs")).lines }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
async function authenticate() {
  authBusy.value = true; error.value = ""
  try {
    current.value = await apiRequest<User>(setupRequired.value ? "/api/v1/setup" : "/api/v1/auth/login", { method: "POST", body: JSON.stringify({ username: username.value, password: password.value }) })
    password.value = ""; setupRequired.value = false; page.value = "overview"; subscribe()
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { authBusy.value = false }
}
async function logout() {
  loggingOut = true
  try {
    await apiRequest("/api/v1/auth/logout", { method: "POST" })
    source?.close(); current.value = null; connected.value = false; logs.value = []; error.value = ""; notice.value = ""; operation.value = null
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { loggingOut = false }
}
watch(page, async (value, old) => {
  if (!current.value || (value !== "console" && old !== "console")) return
  if (value === "console") await loadLogs()
  if (current.value) subscribe()
})
watch(theme, value => { document.documentElement.dataset.theme = value; localStorage.setItem("mcweb-theme", value) })
onMounted(async () => {
  theme.value = localStorage.getItem("mcweb-theme") === "dark" ? "dark" : "light"
  document.documentElement.dataset.theme = theme.value
  clockTimer = setInterval(() => { clock.value = Date.now() }, 1000)
  try {
    const setup = await apiRequest<{ required: boolean }>("/api/v1/setup")
    setupRequired.value = setup.required
    if (!setup.required) {
      const response = await apiFetch("/api/v1/auth/me")
      if (response.ok) { current.value = await response.json(); subscribe() }
      else if (response.status !== 401) throw new Error("暂时无法读取登录状态")
    }
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { initializing.value = false }
})
onUnmounted(() => { source?.close(); if (clockTimer) clearInterval(clockTimer) })
</script>

<template>
  <MoeProvider>
    <div v-if="initializing" class="app-loading"><MoeProgress label="正在连接控制台" :value="null" /></div>
    <main v-else-if="!current" class="auth-page">
      <section class="auth-intro"><div class="brand"><span class="brand-mark"><MoeIcon name="grid" /></span><span>MC SERVER<span class="brand-caption">你的私人服务器</span></span></div><div class="auth-story"><span class="eyebrow">一个世界，随时出发</span><h1>想玩的时候，<br />再叫醒服务器。</h1><p>开服、查看状态、邀请朋友。<br />剩下的，交给你的 NAS。</p><div class="auth-cubes" aria-hidden="true"><span></span><span></span><span></span><span></span></div></div><p class="auth-footnote">按需开机 · 空闲休眠 · 实时管理</p></section>
      <section class="auth-main"><MoeCard class="auth-card" padding="lg"><div class="auth-heading"><MoeBadge color="primary">{{ setupRequired ? '首次使用' : '欢迎回来' }}</MoeBadge><h2>{{ setupRequired ? '创建管理员' : '登录控制台' }}</h2><p>{{ setupRequired ? '设置一个管理员账户，然后在网页连接你的设备。' : '使用管理员提供的账户，继续你的冒险。' }}</p></div><form @submit.prevent="authenticate"><MoeInput v-model="username" label="用户名" autocomplete="username" placeholder="你的账户名称" required /><MoeInput v-model="password" label="密码" type="password" :autocomplete="setupRequired ? 'new-password' : 'current-password'" :minlength="setupRequired ? 8 : undefined" :description="setupRequired ? '至少 8 位，无需包含特殊符号。' : undefined" required /><MoeAlert v-if="error" title="暂时无法继续" color="danger" announce>{{ error }}</MoeAlert><MoeButton type="submit" size="lg" :disabled="authBusy">{{ authBusy ? '正在处理…' : setupRequired ? '创建并进入控制台' : '登录' }}<MoeIcon name="arrow-right" /></MoeButton></form></MoeCard><p class="auth-help">{{ setupRequired ? '已有数据库会自动保留账户，无需重新初始化。' : '还没有账户？请联系服务器管理员。' }}</p></section>
    </main>
    <div v-else class="dashboard">
      <MoeSidebar class="app-sidebar" label="主导航" :groups="navigation" :active="page" @navigate="navigate"><template #header><div class="brand"><span class="brand-mark"><MoeIcon name="grid" /></span><span>MC SERVER<span class="brand-caption">服务器控制台</span></span></div></template><template #footer><div class="sidebar-account"><span class="account-avatar">{{ current.username.slice(0, 1).toUpperCase() }}</span><div><strong>{{ current.username }}</strong><span>{{ admin ? '管理员' : '玩家' }}</span></div><MoeButton icon-only variant="light" color="default" aria-label="退出登录" @click="logout"><MoeIcon name="logout" /></MoeButton></div></template></MoeSidebar>
      <div class="dashboard-main"><header class="topbar"><span class="topbar-location">控制台 <span>/</span> {{ heading.title }}</span><div class="topbar-actions"><span class="live-label"><i :class="{ connected }"></i>{{ connected ? '实时连接' : '正在重连' }}</span><MoeButton icon-only variant="light" color="default" :aria-label="theme === 'light' ? '切换深色主题' : '切换浅色主题'" @click="theme = theme === 'light' ? 'dark' : 'light'"><MoeIcon :name="theme === 'light' ? 'moon' : 'sun'" /></MoeButton><MoeButton class="mobile-logout" icon-only variant="light" color="default" aria-label="退出登录" @click="logout"><MoeIcon name="logout" /></MoeButton></div></header>
        <main class="page-content"><MoePageHeading :title="heading.title" :description="heading.description" /><MoeAlert v-if="error" class="page-feedback" title="操作未完成" color="danger" announce>{{ error }}</MoeAlert><MoeAlert v-else-if="notice" class="page-feedback" :title="notice" color="success" announce />
          <template v-if="page === 'overview'">
            <section class="server-hero" :data-ready="ready"><div class="hero-content"><MoeBadge :color="ready ? 'success' : running ? 'info' : 'default'"><span class="status-dot"></span>{{ ready ? '正在运行' : running ? '启动中' : shuttingDown ? '正在关闭' : '按需开服' }}</MoeBadge><h2>{{ summary.title }}</h2><p>{{ summary.text }}</p><div class="hero-actions"><MoeButton v-if="needsSetup && admin" @click="page = 'connections'">配置设备 <MoeIcon name="arrow-right" /></MoeButton><MoeButton v-else :disabled="startDisabled" size="lg" @click="lifecycle('server/start')">{{ ready ? '服务器运行中' : running ? '正在启动…' : '启动服务器' }}<MoeIcon v-if="!ready && !running" name="arrow-right" /></MoeButton><MoeButton v-if="admin && ready" variant="bordered" color="default" :disabled="busy || running || shuttingDown" @click="confirmShutdown = true">正常关机</MoeButton><span v-if="running && elapsed" class="hero-elapsed">已用时 {{ elapsed }}</span></div></div><div class="hero-emblem" aria-hidden="true"><MoeIcon name="grid" /><span>MINECRAFT</span></div><div v-if="running && operation?.kind === 'start'" class="hero-progress"><MoeSteps label="开服进度" :items="steps" :current="startStep" /></div></section>
            <MoeAlert v-if="status.shutdown === 'failed'" title="关机已暂停" color="warning" class="page-feedback">{{ status.shutdown_error || '上一次关机未完成，请检查连接。' }}<template v-if="admin" #actions><MoeButton variant="light" size="sm" @click="page = 'automation'">查看关机设置</MoeButton></template></MoeAlert>
            <MoeAlert v-if="operation?.status === 'failed'" title="上次操作未完成" color="warning" class="page-feedback">{{ operation.detail }}</MoeAlert>
            <div class="metric-grid"><MoeCard><span class="metric-label">在线玩家</span><strong class="metric-value">{{ status.online ?? '—' }}<small> / {{ status.max_players ?? '—' }}</small></strong><span class="metric-hint">{{ ready ? status.online ? '有人正在探索世界' : '世界安静，等待下一次冒险' : '服务器就绪后显示' }}</span></MoeCard><MoeCard><span class="metric-label">服务器 TPS</span><strong class="metric-value">{{ status.tps?.toFixed(1) ?? '—' }}<small> / 20</small></strong><span class="metric-hint">{{ status.mspt == null ? '等待性能数据' : `${status.mspt.toFixed(1)} ms / tick` }}</span></MoeCard><MoeCard><span class="metric-label">游戏内存</span><strong class="metric-value">{{ memory }}</strong><MoeProgress v-if="status.memory_max" label="游戏内存使用" :value="memoryPercent" /><span v-else class="metric-hint">服务器就绪后显示</span></MoeCard><MoeCard><span class="metric-label">本次运行</span><strong class="metric-value metric-uptime">{{ uptime }}</strong><span class="metric-hint">{{ remaining ? `${remaining} 后进入关机流程` : status.policy_enabled ? '空闲时自动关机' : '自动关机未启用' }}</span></MoeCard></div>
            <div class="overview-grid"><div class="overview-primary"><MoeCard title="在线玩家" :description="status.online ? `${status.online} 位玩家正在服务器中` : '邀请朋友，一起填满这个世界'"><div v-if="status.players?.length" class="player-list"><div v-for="player in status.players" :key="player.uuid" class="player-item"><span class="player-avatar">{{ player.name.slice(0, 1).toUpperCase() }}</span><strong>{{ player.name }}</strong><MoeBadge color="success">在线</MoeBadge></div></div><MoeEmptyState v-else :title="ready ? '现在还没有玩家' : '服务器尚未就绪'" :description="ready ? '复制右侧的连接地址，邀请朋友加入。' : '开服后会实时显示在线玩家。'" icon="user" /></MoeCard><MoeCard v-if="status.minecraft_version" class="version-card"><span>运行版本</span><div><MoeBadge>Minecraft {{ status.minecraft_version }}</MoeBadge><MoeBadge>NeoForge {{ status.neoforge_version }}</MoeBadge><MoeBadge>Command API {{ status.mod_version }}</MoeBadge></div></MoeCard></div><div class="overview-secondary"><MoeCard title="连接地址"><div v-for="address in [{ name: '局域网', value: status.server_lan_address }, { name: '公网', value: status.server_address }].filter(item => item.value)" :key="address.name" class="address-item"><span>{{ address.name }}</span><code>{{ address.value }}</code><MoeButton icon-only variant="light" color="default" :aria-label="`复制${address.name}地址`" @click="copyAddress(address.value!)"><MoeIcon name="copy" /></MoeButton></div><p class="panel-note">{{ status.server_address ? '外网玩家使用公网地址加入。' : '外网玩家请使用管理员提供的游戏地址。' }}</p></MoeCard><MoeCard title="连接状态"><div class="connection-row"><span>笔记本 SSH</span><MoeBadge :color="status.host === 'online' ? 'success' : 'default'">{{ label(status.host) }}</MoeBadge></div><div class="connection-row"><span>Minecraft 容器</span><MoeBadge :color="status.container === 'running' ? 'success' : 'default'">{{ label(status.container) }}</MoeBadge></div><div class="connection-row"><span>智能插座</span><MoeBadge :color="status.plug === 'on' ? 'success' : 'default'">{{ label(status.plug) }}</MoeBadge></div><MoeButton variant="light" size="sm" :disabled="refreshing || !status.plug_configured" @click="refreshPlug">{{ refreshing ? '读取中…' : '刷新插座状态' }}</MoeButton><p v-if="admin && status.ssh_error" class="field-error">{{ status.ssh_error }}</p><p v-if="admin && status.mod_error && !ready" class="panel-note">{{ status.mod_error }}</p></MoeCard></div></div>
          </template>
          <template v-else-if="page === 'console' && admin"><MoeTabs v-model="consoleTab" label="控制台内容" :items="[{ value: 'logs', label: '实时日志' }, { value: 'commands', label: '命令终端' }]" variant="segmented"><template #logs><LogViewer :lines="logs" @reload="loadLogs" /></template><template #commands><Console /></template></MoeTabs></template>
          <template v-else-if="page === 'connections' && admin"><div class="settings-stack"><SSHSettings /><PlugSettings /></div></template>
          <template v-else-if="page === 'automation' && admin"><Policy :applied-revision="status.policy_revision" :effective-enabled="status.policy_enabled" :shutdown-state="status.shutdown" :shutdown-error="status.shutdown_error" /><MoeCard class="automation-note" title="关机如何进行"><ol><li>NAS 根据在线人数和日夜时间计算连续空闲。</li><li>达到阈值后，mod 再次检查玩家状态并保存世界。</li><li>Minecraft 容器正常退出后，通过 SSH 关闭笔记本。</li><li>插座按米家中的低功率规则断电。</li></ol><p class="panel-note">NAS 和笔记本失去连接时，自动关机会暂停。有人加入时重新计时。</p></MoeCard></template>
          <Users v-else-if="page === 'accounts' && admin" :is-admin="true" />
          <Users v-else-if="page === 'account'" :is-admin="false" />
          <footer class="page-footer"><span>MC Server WebUI</span><span>按需开服，安心游玩。</span></footer>
        </main>
      </div>
      <MoeDialog v-model:open="confirmShutdown" title="正常关闭服务器？" description="会先保存世界并停止 Minecraft，再关闭笔记本。有玩家时会先广播 60 秒。" close-label="关闭对话框" :show-close-action="false"><template #footer><div class="dialog-actions"><MoeButton variant="bordered" color="default" @click="confirmShutdown = false">取消</MoeButton><MoeButton color="danger" :disabled="busy" @click="lifecycle('admin/server/shutdown')">{{ busy ? '正在提交…' : '确认关机' }}</MoeButton></div></template></MoeDialog>
    </div>
  </MoeProvider>
</template>
