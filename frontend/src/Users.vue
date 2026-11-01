<script setup lang="ts">
import { apiFetch } from "./api"
import { onMounted, ref } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
const props = defineProps<{ isAdmin: boolean }>()

type User = { id: number; username: string; role: string; enabled: boolean }
type Audit = { id: number; created_at: number; username: string | null; action: string; detail: string }
const users = ref<User[]>([])
const events = ref<Audit[]>([])
const username = ref("")
const password = ref("")
const role = ref("user")
const error = ref("")
const message = ref("")
const oldPassword = ref("")
const newPassword = ref("")
const resetPasswords = ref<Record<number, string>>({})
async function call(path: string, method = "GET", body?: object) {
  const response = await apiFetch(`/api/v1/${path}`, { method, headers: body ? { "Content-Type": "application/json" } : undefined, body: body ? JSON.stringify(body) : undefined })
  const value = await response.json()
  if (!response.ok) throw new Error(value.detail ?? "请求失败")
  return value
}
async function load() {
  try {
    users.value = (await call("admin/users")).users.map((user: User) => ({ ...user, enabled: Boolean(user.enabled) }))
    events.value = (await call("admin/audit")).events
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
async function create() {
  error.value = ""; message.value = ""
  try { await call("admin/users", "POST", { username: username.value, password: password.value, role: role.value }); username.value = ""; password.value = ""; message.value = "账户已创建"; await load() }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
async function update(user: User) {
  error.value = ""; message.value = ""
  try {
    await call(`admin/users/${user.id}`, "PUT", { role: user.role, enabled: Boolean(user.enabled), password: resetPasswords.value[user.id] || null })
    resetPasswords.value[user.id] = ""; message.value = "账户已更新，其会话已失效"; await load()
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
async function changePassword() {
  error.value = ""; message.value = ""
  try { await call("auth/password", "POST", { old_password: oldPassword.value, new_password: newPassword.value }); window.location.reload() }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
}
onMounted(() => { if (props.isAdmin) load() })
</script>

<template>
  <MoeCard v-if="isAdmin" class="notice"><h2>账户管理</h2><p>新账户的密码至少 12 个字符。修改账户会使其登录会话失效。</p>
    <p v-if="error" class="error" role="alert">{{ error }}</p><p v-if="message" role="status">{{ message }}</p>
    <form class="account-form" @submit.prevent="create"><MoeInput v-model="username" label="用户名" required /><MoeInput v-model="password" label="初始密码" type="password" required minlength="12" /><label>角色 <select v-model="role"><option value="user">普通账户</option><option value="admin">管理员</option></select></label><MoeButton type="submit">创建账户</MoeButton></form>
    <div v-for="user in users" :key="user.id" class="user-row"><strong>{{ user.username }}</strong><label>角色 <select v-model="user.role"><option value="user">普通账户</option><option value="admin">管理员</option></select></label><label><input v-model="user.enabled" type="checkbox" /> 启用</label><label>重置密码 <input v-model="resetPasswords[user.id]" type="password" placeholder="留空则不修改" /></label><MoeButton variant="bordered" @click="update(user)">保存</MoeButton></div>
    <details><summary>操作审计</summary><div class="console-output"><div v-for="event in events" :key="event.id">{{ new Date(event.created_at * 1000).toLocaleString() }} · {{ event.username ?? '未知' }} · {{ event.action }} · {{ event.detail }}</div></div></details>
  </MoeCard>
  <MoeCard class="notice"><h2>修改我的密码</h2><p v-if="error" class="error" role="alert">{{ error }}</p><form class="account-form" @submit.prevent="changePassword"><MoeInput v-model="oldPassword" label="当前密码" type="password" required /><MoeInput v-model="newPassword" label="新密码" type="password" minlength="12" required /><MoeButton type="submit">修改密码</MoeButton></form></MoeCard>
</template>
