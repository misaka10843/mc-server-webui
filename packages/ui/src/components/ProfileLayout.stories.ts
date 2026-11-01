import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ProfileLayout from './ProfileLayout.vue'
import Card from './Card.vue'
import UserChip from './UserChip.vue'
import SettingRow from './SettingRow.vue'
const meta = { title: 'Layouts/ProfileLayout', component: ProfileLayout, tags: ['autodocs'], render: () => ({ components: { ProfileLayout, Card, UserChip, SettingRow }, template: '<ProfileLayout><template #summary><Card title="你的账号"><UserChip name="预览用户" description="preview@example.com"/></Card></template><Card title="资料与安全"><SettingRow title="基本资料" description="你的资料来自当前登录账号。"/><SettingRow title="登录会话" description="查看并结束不再使用的连接。"/></Card></ProfileLayout>' }) } satisfies Meta<typeof ProfileLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
