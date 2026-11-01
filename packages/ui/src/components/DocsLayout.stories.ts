import type { Meta, StoryObj } from '@storybook/vue3-vite'
import DocsLayout from './DocsLayout.vue'
const meta = { title: 'Layouts/DocsLayout', component: DocsLayout, tags: ['autodocs'], args: { label: '文档导航', active: 'start', groups: [{ label: '接入指南', items: [{ id: 'start', label: '快速开始', href: '#start' }, { id: 'auth', label: '身份认证', href: '#auth' }] }] }, render: args => ({ components: { DocsLayout }, setup: () => ({ args }), template: '<DocsLayout v-bind="args"><article><h1 class="text-2xl font-semibold">快速开始</h1><p class="mt-4 text-sm text-muted">文档正文与固定侧栏独立滚动。</p></article></DocsLayout>' }) } satisfies Meta<typeof DocsLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
