<script setup lang="ts">
import { onMounted, reactive, ref } from "vue"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import { apiFetch } from "./api"

type Device = { name: string; ip: string; token: string; model: string }
const settings = reactive<{ ip: string; token: string; model: string; siid: number | null; piid: number | null }>({ ip: "", token: "", model: "", siid: null, piid: null })
const login = reactive({ username: "", password: "", locale: "cn" })
const devices = ref<Device[]>([])
const message = ref("")
const busy = ref(false)
const configured = ref(false)

async function load() {
  const response = await apiFetch("/api/v1/admin/plug")
  if (!response.ok) { message.value = "无法读取插座配置"; return }
  const data = await response.json()
  if (data) { Object.assign(settings, data); configured.value = true }
}
async function discover() {
  if (location.protocol !== "https:" && !["localhost", "127.0.0.1", "[::1]"].includes(location.hostname)) {
    message.value = "请在 WebUI 所在设备通过 localhost 访问，或使用 HTTPS 后再登录米家"
    return
  }
  busy.value = true; message.value = ""
  try {
    const response = await apiFetch("/api/v1/admin/plug/discover", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(login) })
    const result = await response.json()
    login.password = ""
    if (!response.ok) throw new Error(result.detail)
    devices.value = result
    message.value = result.length ? "请选择插座" : "该地区未找到设备"
  } catch (e) { message.value = e instanceof Error ? e.message : String(e) }
  finally { login.password = ""; busy.value = false }
}
function choose(index: string) {
  if (!index) return
  const device = devices.value[Number(index)]
  if (device) Object.assign(settings, { ip: device.ip, token: device.token, model: device.model })
}
async function save() {
  busy.value = true; message.value = ""
  try {
    const response = await apiFetch("/api/v1/admin/plug", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(settings) })
    const result = await response.json()
    if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "请检查填写的内容")
    settings.token = ""; devices.value = []; configured.value = true; message.value = "已连接并保存插座配置"
  } catch (e) { message.value = e instanceof Error ? e.message : String(e) }
  finally { busy.value = false }
}
onMounted(load)
</script>

<template>
  <MoeCard class="notice"><h2>智能插座设置</h2><p>填写设备信息并保存，保存前会读取插座状态。token 留空表示沿用已保存的值。</p>
    <details><summary>从米家账号读取设备</summary><p>请使用 HTTPS 或在运行 WebUI 的设备上通过 localhost 访问。账号密码仅用于本次查询。</p>
      <form class="policy-form" @submit.prevent="discover"><label>小米账号 <input v-model="login.username" autocomplete="username" required /></label><label>密码 <input v-model="login.password" type="password" autocomplete="current-password" required /></label><label>地区 <select v-model="login.locale"><option value="cn">中国大陆</option><option value="sg">新加坡</option><option value="de">欧洲</option><option value="us">美国</option><option value="ru">俄罗斯</option><option value="i2">印度</option></select></label><MoeButton type="submit" :disabled="busy">读取设备</MoeButton></form>
      <label v-if="devices.length">选择插座 <select @change="choose(($event.target as HTMLSelectElement).value)"><option value="">请选择</option><option v-for="(device, index) in devices" :key="index" :value="index">{{ device.name }} · {{ device.model }}</option></select></label>
    </details>
    <form class="policy-form" @submit.prevent="save"><label>局域网 IP <input v-model="settings.ip" required /></label><label>设备 token <input v-model="settings.token" type="password" :required="!configured" autocomplete="off" /></label><label>设备型号 <input v-model="settings.model" required /></label><label>开关 SIID <input v-model.number="settings.siid" type="number" min="1" required /></label><label>开关 PIID <input v-model.number="settings.piid" type="number" min="1" required /></label><MoeButton type="submit" :disabled="busy">验证并保存</MoeButton></form><p>开关 SIID 和 PIID 可按型号在 <a href="https://home.miot-spec.com/" target="_blank" rel="noopener">MIoT 规格目录</a>查询。</p><p role="status">{{ message }}</p>
  </MoeCard>
</template>
