<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from "vue"
import MoeAlert from "@moetopia/ui/components/Alert"
import MoeBadge from "@moetopia/ui/components/Badge"
import MoeButton from "@moetopia/ui/components/Button"
import MoeCard from "@moetopia/ui/components/Card"
import MoeInput from "@moetopia/ui/components/Input"
import MoeNumberInput from "@moetopia/ui/components/NumberInput"
import MoeSelect from "@moetopia/ui/components/Select"
import MoeTabs from "@moetopia/ui/components/Tabs"
import { apiFetch, apiRequest } from "./api"

type Device = { name: string; did: string; model: string }
type SavedDevice = { mode: string; model: string; did?: string; region?: string; ip?: string; siid: number; piid: number }
const mode = ref("cloud")
const settings = reactive<{ ip: string; token: string; model: string; siid?: number; piid?: number }>({ ip: "", token: "", model: "" })
const savedDevice = ref<SavedDevice | null>(null)
const region = ref("cn")
const devices = ref<Device[]>([])
const selectedDevice = ref("")
const discovery = ref("")
const qrImage = ref("")
const showProperties = ref(false)
const scanning = ref(false)
const saving = ref(false)
const message = ref("")
const error = ref("")
let controller: AbortController | undefined
const regions = [{ value: "cn", label: "中国大陆" }, { value: "sg", label: "新加坡" }, { value: "tw", label: "中国台湾" }, { value: "de", label: "欧洲" }, { value: "us", label: "美国" }, { value: "ru", label: "俄罗斯" }, { value: "i2", label: "印度" }]
const options = computed(() => devices.value.map(device => ({ value: device.did, label: `${device.name} · ${device.model}` })))
const selected = computed(() => devices.value.find(device => device.did === selectedDevice.value))
async function load() {
  savedDevice.value = await apiRequest<SavedDevice | null>("/api/v1/admin/plug")
  if (savedDevice.value) {
    const data = savedDevice.value
    mode.value = data.mode; settings.model = data.model; settings.siid = data.siid; settings.piid = data.piid
    if (data.ip) settings.ip = data.ip
    if (data.region) region.value = data.region
  }
}
function choose() {
  if (selected.value) settings.model = selected.value.model
  if (selected.value?.model === "cuco.plug.v3") { settings.siid = 2; settings.piid = 1 }
  else { settings.siid = undefined; settings.piid = undefined }
  showProperties.value = selected.value?.model !== "cuco.plug.v3"
}
async function scan() {
  const active = new AbortController()
  controller?.abort(); controller = active
  scanning.value = true; message.value = "正在获取二维码…"; error.value = ""; qrImage.value = ""; devices.value = []; selectedDevice.value = ""; discovery.value = ""
  try {
    const response = await apiFetch("/api/v1/admin/plug/qr", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ locale: region.value }), signal: active.signal })
    if (!response.ok || !response.body) throw new Error("无法开始扫码登录，请重新登录 WebUI 后再试。")
    const reader = response.body.pipeThrough(new TextDecoderStream()).getReader()
    let buffer = "", complete = false
    for (;;) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += value
      let boundary: number
      while ((boundary = buffer.indexOf("\n\n")) >= 0) {
        const event = buffer.slice(0, boundary); buffer = buffer.slice(boundary + 2)
        const name = event.match(/^event: (.+)$/m)?.[1], data = event.match(/^data: (.+)$/m)?.[1]
        if (!data) continue
        const result = JSON.parse(data)
        if (name === "qr") { qrImage.value = `data:image/png;base64,${result.image}`; message.value = "用米家 App 扫码，并在手机上确认登录。" }
        if (name === "devices") {
          devices.value = result.devices; discovery.value = result.discovery; qrImage.value = ""; complete = true
          message.value = result.devices.length ? "登录成功，选择插座后保存即可。" : "该地区未找到设备，请确认米家 App 的地区设置。"
        }
        if (name === "error") throw new Error(result.message)
      }
    }
    if (!complete) throw new Error("扫码连接已中断，请重新获取二维码。")
  } catch (e) { if (!active.signal.aborted) error.value = e instanceof Error ? e.message : String(e) }
  finally { if (controller === active) { scanning.value = false; controller = undefined } }
}
function cancelScan() {
  if (!controller && !scanning.value) return
  controller?.abort(); controller = undefined; scanning.value = false; qrImage.value = ""; message.value = "已取消扫码。"
}
async function save() {
  if (mode.value === "cloud" && !selected.value) return
  if (!settings.siid || !settings.piid) { error.value = "请在开关属性中填写 SIID 和 PIID。"; return }
  saving.value = true; error.value = ""; message.value = ""
  try {
    const cloud = mode.value === "cloud"
    await apiRequest(cloud ? "/api/v1/admin/plug/cloud" : "/api/v1/admin/plug", { method: "PUT", body: JSON.stringify(cloud ? { discovery: discovery.value, did: selectedDevice.value, siid: settings.siid, piid: settings.piid } : settings) })
    settings.token = ""; devices.value = []; selectedDevice.value = ""; discovery.value = ""
    await load(); message.value = "插座已连接，配置立即生效。"
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { saving.value = false }
}
async function refresh() {
  saving.value = true; error.value = ""; message.value = ""
  try {
    const result = await apiRequest<{ plug: string }>("/api/v1/server/plug/refresh", { method: "POST" })
    message.value = `插座连接正常，目前${result.plug === "on" ? "正在供电" : "已断电"}。`
  } catch (e) { error.value = e instanceof Error ? e.message : String(e) }
  finally { saving.value = false }
}
onMounted(() => load().catch(e => { error.value = e.message }))
onUnmounted(() => controller?.abort())
</script>

<template>
  <MoeCard title="智能插座" description="开服时自动供电。推荐使用米家云，NAS 无需直连插座。" padding="lg">
    <div v-if="savedDevice" class="saved-device"><MoeBadge color="success">已配置</MoeBadge><div><strong>{{ savedDevice.model }}</strong><p>{{ savedDevice.mode === 'cloud' ? '米家云控制' : `局域网 · ${savedDevice.ip}` }}</p></div><MoeButton variant="light" size="sm" :disabled="saving" @click="refresh">测试读取</MoeButton></div>
    <MoeTabs v-model="mode" label="插座连接方式" :items="[{ value: 'cloud', label: '米家云 · 推荐' }, { value: 'local', label: '局域网直连' }]" @update:model-value="cancelScan">
      <template #cloud><div class="form-grid"><MoeSelect v-model="region" label="米家地区" :options="regions" /><div class="cloud-start"><MoeButton :disabled="scanning || saving" @click="scan">{{ savedDevice?.mode === 'cloud' ? '重新扫码 / 更换插座' : '扫码连接米家' }}</MoeButton></div></div><div v-if="scanning" class="qr-panel"><img v-if="qrImage" :src="qrImage" alt="米家登录二维码" class="login-qr" /><p>{{ message }}</p><MoeButton variant="light" size="sm" @click="cancelScan">取消扫码</MoeButton></div><form v-if="devices.length" @submit.prevent="save"><MoeSelect v-model="selectedDevice" label="选择插座" :options="options" @update:model-value="choose" /><details v-if="selected" class="advanced-settings" :open="showProperties"><summary>开关属性{{ settings.model === 'cuco.plug.v3' ? ' · 已自动识别' : '' }}</summary><div class="form-grid"><MoeNumberInput v-model="settings.siid" label="SIID" :min="1" :max="65535" /><MoeNumberInput v-model="settings.piid" label="PIID" :min="1" :max="65535" /><p class="panel-note form-span">可按型号在 <a href="https://home.miot-spec.com/" target="_blank" rel="noopener">MIoT 规格目录</a>查询。</p></div></details><div class="form-actions"><MoeButton type="submit" :disabled="saving || !selected">{{ saving ? '正在验证…' : '连接并保存插座' }}</MoeButton></div></form><p v-if="!scanning && !devices.length" class="panel-note">使用米家 App 扫码，无需填写账号密码。登录过期时在这里重新扫码即可。</p></template>
      <template #local><form @submit.prevent="save"><div class="form-grid"><MoeInput v-model="settings.ip" label="插座局域网 IP" placeholder="192.168.101.6" required /><MoeInput v-model="settings.token" label="设备 token" type="password" autocomplete="off" :required="savedDevice?.mode !== 'local'" :description="savedDevice?.mode === 'local' ? '已保存；留空保持不变。' : '32 位十六进制 token。'" /><MoeInput v-model="settings.model" label="设备型号" placeholder="cuco.plug.v3" required @update:model-value="value => { if (value === 'cuco.plug.v3') { settings.siid = 2; settings.piid = 1 } }" /><MoeNumberInput v-model="settings.siid" label="开关 SIID" :min="1" :max="65535" /><MoeNumberInput v-model="settings.piid" label="开关 PIID" :min="1" :max="65535" /></div><p class="panel-note">NAS 必须能通过局域网访问插座。无法直连时，请改用米家云。</p><div class="form-actions"><MoeButton type="submit" :disabled="saving">{{ saving ? '正在验证…' : '验证并保存' }}</MoeButton></div></form></template>
    </MoeTabs><MoeAlert v-if="error" class="form-message" title="插座连接未完成" color="danger" announce>{{ error }}</MoeAlert><MoeAlert v-else-if="message && !scanning" class="form-message" :title="message" color="success" announce />
  </MoeCard>
</template>
