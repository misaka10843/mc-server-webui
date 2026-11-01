import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import SectionPanel from './SectionPanel.vue'
const meta = { component: SectionPanel, tags: ['autodocs'], title: 'Patterns/SectionPanel', args: { title: '用户登录', description: '管理回调与权限' }, render: args => ({ components: { SectionPanel }, setup: () => ({ args }), template: '<SectionPanel v-bind="args"><p class="text-sm">https://example.com/callback</p></SectionPanel>' }) } satisfies Meta<typeof SectionPanel>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
