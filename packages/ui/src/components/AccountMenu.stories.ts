import type { Meta, StoryObj } from '@storybook/vue3-vite'
import AccountMenu from './AccountMenu.vue'
const meta = { title: 'Navigation/AccountMenu', component: AccountMenu, tags: ['autodocs'], args: { label: '你的账号', name: '示例用户', email: 'preview@example.com', items: [{ id: 'profile', label: '个人资料', icon: 'user' }, { id: 'sessions', label: '登录会话', icon: 'shield' }, { id: 'logout', label: '退出登录', icon: 'logout', danger: true, separatorBefore: true }] } } satisfies Meta<typeof AccountMenu>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const UnavailableAvatar: Story = { args: { src: '/example-unavailable-avatar.png' } }
