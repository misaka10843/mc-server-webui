import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './StatusIndicator.vue'
import Button from './Button.vue'
const meta = { title: 'Feedback/StatusIndicator', component: Component, tags: ['autodocs'], args: {"label":"服务正常","state":"positive"}, render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\" />" }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Pending: Story = { args: { label: '正在连接', state: 'pending' } }
export const Unavailable: Story = { args: { label: '连接暂不可用', state: 'negative', announce: true } }

