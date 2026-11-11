<script setup lang="ts">
import { onMounted, reactive, ref } from "vue"
import MoeAlert from "@moetopia/ui/components/Alert"
import MoeBadge from "@moetopia/ui/components/Badge"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeNumberInput from "@moetopia/ui/components/NumberInput"
import MoeTextarea from "@moetopia/ui/components/Textarea"
import { apiRequest } from "./api"

const config = reactive({ host: "192.168.101.41", port: 22, username: "", password: "", private_key: "", host_key: "", container: "minecraft", mod_port: 8766, mod_token: "" })
const busy = ref(false)
const configured = ref(false)
const message = ref("")
const error = ref("")
const testResult = ref<{ container: string; poweroff: boolean } | null>(null)
function addressChanged() { config.host_key = ""; testResult.value = null }
async function load() {
  const result = await apiRequest<typeof config | null>("/api/v1/admin/ssh")
  if (result) { Object.assign(config, result); configured.value = true }
}
async function save() {
  busy.value = true; message.value = ""; error.value = ""
  try {
    await apiRequest("/api/v1/admin/ssh", { method: "PUT", body: JSON.stringify(config) })
    config.password = ""; config.private_key = ""; config.mod_token = ""
    await load()
    message.value = "已保存，NAS 正在连接笔记本。"
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
async function test() {
  busy.value = true; error.value = ""; message.value = ""; testResult.value = null
  try {
    const result = await apiRequest<{ host_key: string; container: string; poweroff: boolean }>("/api/v1/admin/ssh/test", { method: "POST", body: JSON.stringify(config) })
    config.host_key = result.host_key; testResult.value = result
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
async function renewHostKey() {
  busy.value = true; error.value = ""
  try {
    const result = await apiRequest<{ host_key: string; fingerprint: string }>("/api/v1/admin/ssh/probe", { method: "POST", body: JSON.stringify({ host: config.host, port: config.port }) })
    config.host_key = result.host_key; message.value = `已读取新指纹 ${result.fingerprint}。保存后生效。`
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
onMounted(() => load().catch(e => { error.value = e.message }))
</script>

<template>
  <MoeCard title="笔记本连接" description="通过局域网 SSH 管理 Minecraft，无需在笔记本安装代理。" padding="lg">
    <div v-if="configured" class="saved-device"><MoeBadge color="success">已配置</MoeBadge><div><strong>{{ config.username }}@{{ config.host }}</strong><p>容器：{{ config.container }} · SSH {{ config.port }}</p></div></div>
    <form @submit.prevent="save"><div class="form-grid"><MoeInput v-model="config.host" label="笔记本 IP" placeholder="192.168.101.41" required @update:model-value="addressChanged" /><MoeInput v-model="config.username" label="SSH 用户名" placeholder="笔记本登录账户" autocomplete="username" required /><MoeInput v-model="config.password" label="SSH 密码" type="password" autocomplete="new-password" :description="configured ? '已保存；留空保持不变。' : '也可以在高级设置中使用 SSH 私钥。'" /><MoeInput v-model="config.container" label="Minecraft 容器名" placeholder="minecraft" required /><MoeInput v-model="config.mod_token" label="command-api 密钥" type="password" autocomplete="off" :description="configured ? '已保存；留空保持不变。' : '与 Minecraft 的 COMMAND_API_TOKEN 一致。'" /></div>
      <details class="advanced-settings"><summary>高级设置 · 端口与 SSH 私钥</summary><div class="form-grid"><MoeNumberInput v-model="config.port" label="SSH 端口" :min="1" :max="65535" @update:model-value="addressChanged" /><MoeNumberInput v-model="config.mod_port" label="command-api 端口" :min="1" :max="65535" /><MoeTextarea v-model="config.private_key" class="form-span" label="OpenSSH 私钥" description="使用未加密私钥时可以不填 SSH 密码。私钥保存在 NAS 数据库中。" /><div class="form-span"><p class="panel-note">首次连接自动记住主机密钥。只有笔记本重装系统或更换 SSH 主机密钥后，才需要更新。</p><MoeButton type="button" variant="light" size="sm" :disabled="busy" @click="renewHostKey">重新读取主机指纹</MoeButton></div></div></details>
      <div class="form-actions"><MoeButton type="submit" :disabled="busy">{{ busy ? '正在处理…' : '保存连接' }}</MoeButton><MoeButton type="button" variant="bordered" color="default" :disabled="busy" @click="test">测试连接</MoeButton><span class="panel-note">首次保存时请保持笔记本开机。</span></div>
    </form>
    <MoeAlert v-if="error" class="form-message" title="连接设置未完成" color="danger" announce>{{ error }}</MoeAlert><MoeAlert v-else-if="message" class="form-message" :title="message" color="success" announce />
    <MoeAlert v-if="testResult" class="form-message" :color="testResult.poweroff ? 'success' : 'warning'" :title="testResult.poweroff ? 'SSH、Docker 和关机权限均可用' : 'SSH 与 Docker 可用，关机权限需要配置'">容器状态：{{ testResult.container }}。<template v-if="!testResult.poweroff">请按部署文档给该账户添加免密执行 systemctl poweroff 的权限。</template></MoeAlert>
  </MoeCard>
</template>
