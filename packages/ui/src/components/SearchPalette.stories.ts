import type { Meta, StoryObj } from '@storybook/vue3-vite'
import SearchPalette from './SearchPalette.vue'
const meta = { title: 'Navigation/SearchPalette', component: SearchPalette, tags: ['autodocs'], args: { title: '搜索文档', placeholder: '搜索文档…', closeLabel: '关闭', emptyLabel: '没有匹配的页面', items: [{ value: 'authentication', label: '身份认证', description: 'OAuth / PKCE' }, { value: 'endpoints', label: '协议端点', description: 'Discovery / Token / UserInfo' }] } } satisfies Meta<typeof SearchPalette>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
