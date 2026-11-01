import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ConsentDetails from './ConsentDetails.vue'
const meta = { title: 'Identity/ConsentDetails', component: ConsentDetails, tags: ['autodocs'], args: { title: '将读取以下账号信息', items: [{ key: 'name', label: '昵称', field: 'name', value: '示例用户' }, { key: 'email', label: '邮箱地址', field: 'email', value: 'preview@example.com' }] } } satisfies Meta<typeof ConsentDetails>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
