<script setup lang="ts">
import { ref } from 'vue'
import { MoeNavbar, MoeSidebar, MoeBreadcrumbs, MoeDropdown, MoeAvatar, MoeButton, MoeIcon, MoePagination, MoeSteps, MoeKbd } from '../index'
import type { MoeNavItem, MoeMenuItem } from '../types'
import { navigationItems, navigationGroups, menuItems } from './navigation-data'
const active = ref('home')
const collapsed = ref(false)
const page = ref(1)
const message = ref('选择导航或菜单查看交互。')
const navigate = (event: MouseEvent, item: MoeNavItem) => { event.preventDefault(); active.value = item.id; message.value = `当前导航：${item.label}` }
const select = (item: MoeMenuItem) => { message.value = `已选择：${item.label}（仅演示，不执行账号操作）` }
</script>
<template>
  <div class="mx-auto grid max-w-6xl gap-8 text-foreground">
    <header class="grid gap-2"><h1 class="text-2xl font-semibold">导航组件工作台</h1><p class="text-sm leading-6 text-muted">顶栏、侧栏是独立组件。缩小窗口查看移动导航；当前内容均为静态演示。</p></header>
    <section aria-label="顶栏预览" class="overflow-hidden rounded-xl border border-line">
      <MoeNavbar brand="Moetopia" label="主导航" :items="navigationItems" :active="active" brand-href="#" @navigate="navigate">
        <template #actions><MoeButton icon-only variant="light" color="default" aria-label="搜索" @click="message = '搜索入口展示示例'"><MoeIcon name="search" /></MoeButton><MoeDropdown label="用户菜单" heading="演示账号" :items="menuItems" @select="select"><button type="button" class="moe-focus rounded-full" aria-label="打开用户菜单"><MoeAvatar name="雨宫 澪" size="sm" /></button></MoeDropdown></template>
        <template #mobile-footer><p class="text-xs text-muted">Moetopia · 与喜欢的世界相连</p></template>
      </MoeNavbar>
      <div class="p-5"><MoeBreadcrumbs :items="[{ label: '个人空间', href: '#space' }, { label: '账号中心', href: '#account' }, { label: '个人资料' }]" /><p class="mt-6 text-sm text-muted" role="status">{{ message }}</p></div>
    </section>
    <section aria-label="侧栏预览" class="flex items-start gap-6">
      <MoeSidebar v-model:collapsed="collapsed" :groups="navigationGroups" :active="active" label="工作区导航" collapsible @navigate="navigate"><template #header><span class="pl-2 text-sm font-semibold">个人空间</span></template><template #footer="{ collapsed: compact }"><div class="flex items-center gap-3 px-1"><MoeAvatar name="雨宫 澪" size="sm" /><div v-if="!compact" class="grid gap-1"><span class="text-xs font-medium">雨宫 澪</span><span class="text-xs text-muted">个人账号</span></div></div></template></MoeSidebar>
      <div class="hidden min-w-0 flex-1 py-3 sm:grid sm:gap-3"><h2 class="font-semibold">分组与收起状态</h2><p class="text-sm leading-7 text-muted">当前项使用浅色底板，禁用项保留说明，计数靠右对齐。收起后保留图标与可访问名称。</p><div class="flex items-center gap-2 text-xs text-muted"><MoeKbd>Tab</MoeKbd><span>移动焦点</span><MoeKbd>Enter</MoeKbd><span>打开链接</span></div></div>
    </section>
    <section aria-label="分页预览" class="grid gap-4"><h2 class="font-semibold">分页 / Pagination</h2><MoePagination v-model:page="page" :total="200" /><p class="text-xs text-muted" role="status">当前第 {{ page }} 页，共 20 页</p></section>
    <section aria-label="步骤预览" class="grid gap-4"><h2 class="font-semibold">步骤 / Steps</h2><MoeSteps label="应用接入流程" current="review" :items="[{ value: 'create', label: '创建应用', description: '填写基础资料' }, { value: 'review', label: '提交审核', description: '确认权限与回调地址' }, { value: 'publish', label: '正式发布', description: '审核后开放接入' }]" /></section>
  </div>
</template>
