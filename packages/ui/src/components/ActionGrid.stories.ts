import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ActionGrid from './ActionGrid.vue'
const meta = { component: ActionGrid, title: 'Patterns/ActionGrid', tags: ['autodocs'], args: { items: [{ id: 'users', href: '#users', label: '用户管理 · Users', icon: 'user' }, { id: 'applications', href: '#applications', label: '应用审核 · Applications', icon: 'grid' }, { id: 'invitations', href: '#invitations', label: '邀请码 · Invitations', icon: 'plus' }, { id: 'settings', href: '#settings', label: '设置 · Settings', icon: 'settings' }] } } satisfies Meta<typeof ActionGrid>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
