import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './EmptyState.vue'
import Button from './Button.vue'

const meta = {
  title: 'Feedback/EmptyState', component: Component, tags: ['autodocs'],
  args: {"title":"还没有创建应用","description":"创建第一个应用，开始接入 Moetopia。"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><Button size=\"sm\">创建应用</Button></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Illustrated: Story = { args: { illustration: 'no-applications' } }
export const NoResults: Story = { args: { title: '没有匹配的结果', description: '试试其他搜索条件。', illustration: 'no-results', illustrationSize: 'sm' } }


