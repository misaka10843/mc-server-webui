import type { Meta, StoryObj } from '@storybook/vue3-vite'
import RequestPanel from './RequestPanel.vue'
const meta = { title: 'Documentation/RequestPanel', component: RequestPanel, tags: ['autodocs'], args: { title: '在线测试', hint: '使用测试账号和测试应用。', runLabel: '发送请求', clearLabel: '清空', cancelLabel: '停止等待', responseLabel: '实际响应', elapsedLabel: '耗时', copyLabel: '复制', copiedLabel: '已复制', errorLabel: '复制失败', status: 200, elapsed: 12, response: '{"example": true}' } } satisfies Meta<typeof RequestPanel>
export default meta
type Story = StoryObj<typeof meta>
export const Response: Story = {}
export const Busy: Story = { args: { busy: true, response: undefined, status: undefined } }
