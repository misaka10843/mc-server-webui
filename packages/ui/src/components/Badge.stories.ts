import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Badge from './Badge.vue'
const meta = { title: 'Feedback/Badge', component: Badge, tags: ['autodocs'], args: {"color":"primary"}, render: (args) => ({ components: { Badge }, setup: () => ({ args }), template: '<Badge v-bind="args">待审核 · Pending</Badge>' }) } satisfies Meta<typeof Badge>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Bordered: Story = { args: { variant: 'bordered', color: 'warning' } }
export const Solid: Story = { args: { variant: 'solid', color: 'success' } }
