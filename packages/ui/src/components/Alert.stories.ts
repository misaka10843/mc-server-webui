import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Alert from './Alert.vue'
const meta = { title: 'Feedback/Alert', component: Alert, tags: ['autodocs'], args: {"title":"提示","color":"info"}, render: (args) => ({ components: { Alert }, setup: () => ({ args }), template: '<Alert v-bind="args">保留你的输入，可以稍后重试。</Alert>' }) } satisfies Meta<typeof Alert>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Danger: Story = { args: { color: 'danger', title: '操作失败', announce: true } }
export const Success: Story = { args: { color: 'success', title: '操作完成' } }
