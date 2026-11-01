<script setup lang="ts">
import { computed, ref } from 'vue'
import { MoePasswordInput, MoePinInput, MoeSlider, MoeAccordion, MoePopover, MoeDrawer, MoeToastProvider, MoeToast, MoeButton, MoeIcon, MoeTable, MoeBadge, MoeProgress, MoeEmptyState, MoeTag, MoeButtonGroup, MoeDivider, MoeLink, MoeKbd, MoeAvatar } from '../index'
import type { MoeTableColumn } from '../types'
import { MoeCombobox, MoeNumberInput, MoeFileInput, MoeDateInput, MoeAvatarGroup, MoeScrollArea, MoeUserChip, MoeCheckboxGroup } from '../index'
const password = ref('')
const pin = ref<(number | undefined)[]>([])
const application = ref('')
const quantity = ref<number | undefined>(10)
const date = ref('')
const channels = ref(['security'])
const volume = ref([50])
const progress = ref(35)
const toast = ref(false)
const tags = ref(['Nuxt', 'Go', 'OpenID Connect'])
const sortDirection = ref<'asc' | 'desc'>('asc')
const sortKey = ref('name')
const rows = [{ id: '1', name: 'Moetopia Community', type: 'Web 应用', status: '已批准' }, { id: '2', name: '开发预览', type: '本地客户端', status: '审核中' }, { id: '3', name: 'Personal Gallery', type: 'Web 应用', status: '测试中' }]
const sortedRows = computed(() => [...rows].sort((a, b) => { const key = sortKey.value === 'type' ? 'type' : 'name'; return a[key].localeCompare(b[key]) * (sortDirection.value === 'asc' ? 1 : -1) }))
const sort = (key: string) => { sortDirection.value = sortKey.value === key && sortDirection.value === 'asc' ? 'desc' : 'asc'; sortKey.value = key }
const columns: MoeTableColumn[] = [{ key: 'name', label: '应用名称', sortable: true }, { key: 'type', label: '类型', sortable: true }, { key: 'status', label: '状态' }]
</script>
<template>
  <MoeToastProvider><div class="mx-auto grid max-w-4xl gap-10 text-foreground">
    <header class="grid gap-2"><h1 class="text-2xl font-semibold">常用组件工作台</h1><p class="text-sm text-muted">表单补充、反馈、浮层和数据展示；全部使用假数据。</p></header>
    <section aria-label="补充表单" class="grid gap-6 md:grid-cols-2"><div class="grid content-start gap-5"><MoePasswordInput v-model="password" label="演示密码" autocomplete="new-password" description="不会提交或保存输入。" /><MoePinInput v-model="pin" label="邮箱验证码" description="输入或粘贴 6 位数字。" /></div><div class="grid content-start gap-5"><MoeSlider v-model="volume" label="预览音量" show-value /><div class="flex flex-wrap gap-2"><MoeTag v-for="tag in tags" :key="tag" :label="tag" removable @remove="tags = tags.filter(value => value !== tag)" /></div><MoeButtonGroup label="编辑操作"><MoeButton variant="light" color="default">编辑</MoeButton><MoeButton variant="light" color="default">预览</MoeButton><MoeButton variant="light" color="default" disabled>发布</MoeButton></MoeButtonGroup></div></section>
    <section aria-label="更多表单控件" class="grid items-start gap-6 md:grid-cols-2">
      <div class="grid gap-5"><MoeCombobox v-model="application" label="搜索应用" :options="[{ value: 'community', label: 'Moetopia Community' }, { value: 'gallery', label: 'Personal Gallery' }, { value: 'archive', label: 'Archived', disabled: true }]" /><MoeNumberInput v-model="quantity" label="每页条目数" :min="1" :max="100" /><MoeDateInput v-model="date" label="生效日期" min="2026-01-01" max="2027-12-31" description="使用浏览器原生日期选择器。" /></div>
      <div class="grid gap-5"><MoeFileInput label="选择应用图标" accept="image/*" description="只选择文件，不会上传。" /><MoeCheckboxGroup v-model="channels" label="通知分类" :options="[{ value: 'security', label: '安全提醒' }, { value: 'community', label: '社区动态' }, { value: 'reserved', label: '其他通知', disabled: true }]" /></div>
    </section>
    <MoeDivider />
    <section aria-label="浮层与通知" class="grid gap-4"><h2 class="font-semibold">浮层与通知</h2><div class="flex flex-wrap gap-3"><MoePopover label="筛选条件"><template #trigger><MoeButton variant="bordered">打开筛选</MoeButton></template><p class="text-sm leading-6 text-muted">这里可以放置表单、筛选和上下文操作。</p></MoePopover><MoeDrawer title="应用详情" description="右侧抽屉保留当前页面上下文。"><template #trigger><MoeButton variant="bordered">打开详情抽屉</MoeButton></template><div class="grid gap-4 pt-2"><p class="text-sm">Moetopia Community</p><MoeBadge color="success">已批准</MoeBadge><p class="text-sm leading-7 text-muted">长内容在抽屉内部滚动。Escape 关闭后焦点返回触发按钮。</p></div><template #footer="{ close }"><MoeButton class="w-full" @click="close">完成</MoeButton></template></MoeDrawer><MoeButton @click="toast = true">显示保存通知</MoeButton></div><MoeToast v-model:open="toast" title="设置已保存" description="这是组件展示，不会保存真实账号信息。" color="success" /></section>
    <section aria-label="数据展示" class="grid gap-4"><h2 class="font-semibold">数据表格</h2><MoeTable caption="示例应用列表" :columns="columns" :rows="sortedRows" row-key="id" :sort-key="sortKey" :sort-direction="sortDirection" @sort="sort"><template #cell-name="{ row }"><div class="flex items-center gap-3"><MoeAvatar :name="row.name" shape="square" size="sm" /><span>{{ row.name }}</span></div></template><template #cell-status="{ row }"><MoeBadge :color="row.status === '已批准' ? 'success' : row.status === '审核中' ? 'warning' : 'default'">{{ row.status }}</MoeBadge></template></MoeTable></section>
    <section aria-label="进度展示" class="grid gap-4"><MoeProgress label="资料完善程度" :value="progress" show-value /><MoeProgress label="正在处理请求" /><MoeButton size="sm" variant="light" class="justify-self-start" @click="progress = (progress + 20) % 101">更新进度</MoeButton></section>
    <section aria-label="折叠内容"><MoeAccordion :items="[{ value: 'identity', title: '什么是统一账号？', description: '使用同一身份访问已接入的应用，每个应用独立管理自己的业务权限。' }, { value: 'permissions', title: '如何管理授权？', description: '授权管理的业务入口会在页面布局阶段接入。' }, { value: 'disabled', title: '暂不可用的帮助', disabled: true }]" /></section>
    <section aria-label="空状态展示" class="rounded-xl border border-dashed border-line"><MoeEmptyState title="还没有创建应用" description="准备好应用名称和回调地址后，即可开始接入。"><MoeButton size="sm"><MoeIcon name="plus" />创建应用</MoeButton><MoeLink href="#guide">阅读指南</MoeLink></MoeEmptyState></section>
    <section aria-label="用户与滚动区域" class="grid gap-6 md:grid-cols-2"><div class="grid content-start gap-5"><MoeUserChip name="雨宫 澪" description="Moetopia 成员" /><MoeAvatarGroup label="应用协作者" :max="3" :items="[{ id: '1', name: '雨宫 澪' }, { id: '2', name: '白石 凛' }, { id: '3', name: '松永 葵' }, { id: '4', name: '小春' }, { id: '5', name: 'Alice' }]" /></div><MoeScrollArea label="示例活动记录" height="200px"><ul class="divide-y divide-line"><li v-for="index in 20" :key="index" class="px-4 py-3 text-sm">演示活动 {{ index }}</li></ul></MoeScrollArea></section>
    <footer class="flex flex-wrap items-center gap-2 text-xs text-muted"><MoeKbd>Esc</MoeKbd><span>关闭弹层</span><MoeLink href="https://ui.kungal.com" external>KunUI 参考</MoeLink></footer>
  </div></MoeToastProvider>
</template>
