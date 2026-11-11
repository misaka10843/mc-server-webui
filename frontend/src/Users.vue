<script setup lang="ts">
import { apiFetch } from "./api"
import { onMounted, ref } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeSelect from "@moetopia/ui/components/Select"
import MoeSwitch from "@moetopia/ui/components/Switch"
import MoeAlert from "@moetopia/ui/components/Alert"
const roles = [{ value: "user", label: "普通账户" }, { value: "admin", label: "管理员" }]
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
const busy = ref(false)
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
  busy.value = true
  error.value = ""; message.value = ""
  try { await call("admin/users", "POST", { username: username.value, password: password.value, role: role.value }); username.value = ""; password.value = ""; message.value = "账户已创建"; await load() }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
async function update(user: User) {
  busy.value = true
  error.value = ""; message.value = ""
  try {
    await call(`admin/users/${user.id}`, "PUT", { role: user.role, enabled: Boolean(user.enabled), password: resetPasswords.value[user.id] || null })
    resetPasswords.value[user.id] = ""; message.value = "账户已保存。权限或密码变化后，需要重新登录。"; await load()
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
async function changePassword() {
  busy.value = true
  error.value = ""; message.value = ""
  try { await call("auth/password", "POST", { old_password: oldPassword.value, new_password: newPassword.value }); window.location.reload() }
  catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
onMounted(() => { if (props.isAdmin) load() })
</script>

<template>
  <MoeCard v-if="isAdmin" title="账户管理" description="普通账户可以查看状态和开服，管理员可以执行命令、查看日志及修改设置。" padding="lg">
    <form class="account-form" @submit.prevent="create"><MoeInput v-model="username" label="用户名" required /><MoeInput v-model="password" label="初始密码" type="password" required minlength="8" placeholder="至少 8 位" /><MoeSelect v-model="role" label="角色" :options="roles" /><MoeButton type="submit" :disabled="busy">创建账户</MoeButton></form>
    <div v-for="user in users" :key="user.id" class="user-row"><strong>{{ user.username }}</strong><MoeSelect v-model="user.role" label="角色" :options="roles" /><MoeSwitch v-model="user.enabled" label="启用" /><MoeInput v-model="resetPasswords[user.id]" label="重置密码" type="password" placeholder="留空则不修改" /><MoeButton variant="bordered" color="default" :disabled="busy" @click="update(user)">保存</MoeButton></div>
    <details><summary>操作审计</summary><div class="console-output"><div v-for="event in events" :key="event.id">{{ new Date(event.created_at * 1000).toLocaleString() }} · {{ event.username ?? '未知' }} · {{ event.action }} · {{ event.detail }}</div></div></details>
  </MoeCard>
  <MoeCard v-else title="修改密码" description="修改后需要使用新密码重新登录。" padding="lg"><form class="account-form" @submit.prevent="changePassword"><MoeInput v-model="oldPassword" label="当前密码" type="password" autocomplete="current-password" required /><MoeInput v-model="newPassword" label="新密码" type="password" autocomplete="new-password" minlength="8" placeholder="至少 8 位" required /><MoeButton type="submit" :disabled="busy">修改密码</MoeButton></form></MoeCard>
  <MoeAlert v-if="error" class="form-message" title="操作未完成" color="danger" announce>{{ error }}</MoeAlert><MoeAlert v-else-if="message" class="form-message" :title="message" color="success" announce />
</template>
