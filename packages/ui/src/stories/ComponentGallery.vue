<script setup lang="ts">
import { ref } from 'vue'
import { MoeButton, MoeInput, MoeTextarea, MoeCheckbox, MoeSwitch, MoeRadioGroup, MoeSelect, MoeTabs, MoeBadge, MoeAlert, MoeCard, MoeSpinner, MoeSkeleton, MoeTooltip, MoeDialog } from '../index'
import type { MoeColor, MoeVariant } from '../types'
const colors: MoeColor[] = ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'default']
const variants: MoeVariant[] = ['solid', 'bordered', 'flat', 'light']
const email = ref('')
const notes = ref('')
const checked = ref<boolean | 'indeterminate'>(true)
const notifications = ref(true)
const visibility = ref('private')
const locale = ref('zh-CN')
const tab = ref('account')
const underlineTab = ref('profile')
const loading = ref(false)
const busyPreview = async () => { loading.value = true; await new Promise(resolve => setTimeout(resolve, 1200)); loading.value = false }
</script>

<template>
  <div class="mx-auto grid max-w-5xl gap-10 text-foreground">
    <header class="grid gap-2"><h1 class="text-2xl font-semibold">Moetopia 组件工作台</h1><p class="text-sm text-muted">先评审控件，再组合页面。工具栏可切换明暗主题。</p></header>
    <section class="grid gap-4" aria-label="按钮矩阵"><h2 class="text-lg font-semibold">按钮 / Button</h2>
      <div v-for="variant in variants" :key="variant" class="flex flex-wrap items-center gap-3"><span class="w-16 text-xs text-muted">{{ variant }}</span><MoeButton v-for="color in colors" :key="color" :color="color" :variant="variant">{{ color }}</MoeButton></div>
      <div class="flex flex-wrap items-center gap-3"><MoeButton size="sm">小号</MoeButton><MoeButton>中号</MoeButton><MoeButton size="lg">大号</MoeButton><MoeButton :loading="loading" @click="busyPreview">查看加载状态</MoeButton><MoeButton disabled>不可操作</MoeButton></div>
    </section>
    <section class="grid gap-5" aria-label="表单控件"><h2 class="text-lg font-semibold">表单 / Form</h2>
      <div class="grid items-start gap-7 md:grid-cols-2"><div class="grid gap-5">
        <MoeInput v-model="email" label="邮箱" placeholder="you@example.com" description="说明跟随输入框，不占用额外卡片。" />
        <MoeInput label="错误状态" error="请输入有效邮箱。" />
        <MoeInput label="禁用状态" model-value="不可编辑" disabled />
        <MoeTextarea v-model="notes" label="个人简介" placeholder="写一点关于自己…" description="支持键盘、标签与原生表单属性。" />
      </div><div class="grid gap-3">
        <MoeSelect v-model="locale" label="语言" :options="[{ value: 'zh-CN', label: '简体中文' }, { value: 'en', label: 'English' }, { value: 'ja', label: '日本語（准备中）', disabled: true }]" />
        <MoeCheckbox v-model="checked" label="接收社区动态" description="点击文字也可以切换。" />
        <MoeCheckbox label="暂时不可选" disabled />
        <MoeSwitch v-model="notifications" label="邮件通知" description="更改开关不会自动触发网络请求。" />
        <MoeRadioGroup v-model="visibility" label="资料可见性" :options="[{ value: 'private', label: '仅自己', description: '默认保护隐私' }, { value: 'public', label: '公开' }, { value: 'team', label: '仅团队', disabled: true }]" />
      </div></div>
    </section>
    <section class="grid gap-4" aria-label="导航与状态"><h2 class="text-lg font-semibold">导航与反馈 / Navigation & feedback</h2>
      <MoeTabs v-model="tab" label="设置示例" :items="[{ value: 'account', label: '账号' }, { value: 'security', label: '安全' }, { value: 'apps', label: '应用', disabled: true }]"><template #account>这里只演示组件交互，不连接账号服务。</template><template #security>方向键切换标签，Tab 进入内容区域。</template></MoeTabs>
      <MoeTabs v-model="underlineTab" variant="underline" label="下划线示例" :items="[{ value: 'profile', label: '个人资料', description: '下划线样式适合页面内分区。' }, { value: 'sessions', label: '登录设备', description: '切换时指示条跟随移动，内容轻量淡入。' }, { value: 'permissions', label: '授权管理', description: '两种样式共享键盘操作与焦点规则。' }]" />
      <div class="flex flex-wrap gap-2"><MoeBadge v-for="color in colors" :key="color" :color="color">{{ color }}</MoeBadge></div>
      <div class="grid gap-3 md:grid-cols-2"><MoeAlert title="操作完成" color="success">资料已更新的展示示例。</MoeAlert><MoeAlert title="需要注意" color="warning">状态由文字表达，不只依赖颜色。</MoeAlert><MoeAlert title="连接失败" color="danger">输入会保留，可以稍后重试。</MoeAlert><MoeAlert title="提示" color="info">静态示例不会反复向读屏器播报。</MoeAlert></div>
    </section>
    <section class="grid gap-4" aria-label="容器与浮层"><h2 class="text-lg font-semibold">容器与浮层 / Surfaces</h2>
      <MoeCard title="普通卡片" description="标题、正文、操作区分别组织。"><p class="text-sm leading-7">不带默认悬浮动效，不把整张卡片伪装成按钮。</p><template #footer><MoeButton variant="light">查看详情</MoeButton></template></MoeCard>
      <div class="flex flex-wrap gap-3"><MoeTooltip text="鼠标悬停或键盘聚焦均可显示"><MoeButton variant="bordered">查看提示</MoeButton></MoeTooltip><MoeDialog title="确认操作" description="检查焦点进入、Escape 关闭和焦点返回。" close-label="关闭"><template #trigger><MoeButton>打开对话框</MoeButton></template><p class="text-sm">这是一个纯 UI 示例。</p></MoeDialog></div>
      <MoeSpinner label="正在加载…" /><div class="grid max-w-sm gap-3"><MoeSkeleton shape="avatar" /><MoeSkeleton /><MoeSkeleton shape="block" /></div>
    </section>
  </div>
</template>
