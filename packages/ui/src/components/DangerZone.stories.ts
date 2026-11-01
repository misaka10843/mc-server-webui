import type { Meta, StoryObj } from '@storybook/vue3-vite'
import DangerZone from './DangerZone.vue'
const meta = { title: 'Feedback/DangerZone', component: DangerZone, tags: ['autodocs'], args: { title: '注销账号', description: '危险操作必须由实际服务确认，示例不会删除数据。' } } satisfies Meta<typeof DangerZone>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
