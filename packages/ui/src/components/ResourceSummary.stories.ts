import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import ResourceSummary from './ResourceSummary.vue'
const meta = { component: ResourceSummary, tags: ['autodocs'], title: 'Patterns/ResourceSummary', args: { title: 'Moetopia community', description: '社区统一登录', identifier: 'example-client-id', copyLabel: '复制', copiedLabel: '已复制', errorLabel: '复制失败', items: [{ key: 'type', label: '客户端类型', value: 'Public' }, { key: 'status', label: '状态', value: '测试中' }, { key: 'version', label: '版本', value: '1' }, { key: 'created', label: '创建时间', value: '2026-10-19' }] } } satisfies Meta<typeof ResourceSummary>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
