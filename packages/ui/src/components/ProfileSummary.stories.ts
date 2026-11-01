import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ProfileSummary from './ProfileSummary.vue'
const meta = { title: 'Layouts/ProfileSummary', component: ProfileSummary, tags: ['autodocs'], args: { name: '预览用户', email: 'preview@example.com', description: '使用这个账号登录 Moetopia 与已接入的应用。' }, render: args => ({ components: { ProfileSummary }, setup: () => ({ args }), template: '<div style="max-width:304px"><ProfileSummary v-bind="args"/></div>' }) } satisfies Meta<typeof ProfileSummary>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
