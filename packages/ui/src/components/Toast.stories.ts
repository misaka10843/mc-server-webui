import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Toast from './Toast.vue'
import ToastProvider from './ToastProvider.vue'
import Button from './Button.vue'
const meta = { title: 'Feedback/Toast', component: Toast, tags: ['autodocs'], args: { title: '设置已保存', description: '这是一条演示通知。', color: 'success' }, render: args => ({ components: { Toast, ToastProvider, Button }, setup: () => ({ args, open: ref(false) }), template: '<ToastProvider><Button @click="open = true">显示通知</Button><Toast v-bind="args" v-model:open="open" /></ToastProvider>' }) } satisfies Meta<typeof Toast>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Error: Story = { args: { color: 'danger', title: '请求失败', description: '输入已保留，可以稍后重试。' } }
