import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Table from './Table.vue'
const meta = {
  title: 'Feedback/Table', tags: ['autodocs'], args: { loading: false, empty: false },
  render: args => ({ components: { Table }, setup: () => ({ args, columns: [{ key: 'name', label: '名称' }, { key: 'status', label: '状态' }], rows: [{ id: '1', name: '示例应用', status: '已批准' }, { id: '2', name: '开发预览', status: '审核中' }] }), template: '<Table caption="应用列表" row-key="id" :columns="columns" :rows="args.empty ? [] : rows" :loading="args.loading" empty-title="还没有应用" empty-description="创建应用后会显示在这里。" />' }),
} satisfies Meta<{ loading: boolean; empty: boolean }>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Empty: Story = { args: { empty: true } }
export const Loading: Story = { args: { loading: true } }
