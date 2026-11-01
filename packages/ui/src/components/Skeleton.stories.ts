import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Skeleton from './Skeleton.vue'
const meta = { title: 'Feedback/Skeleton', component: Skeleton, tags: ['autodocs'], args: {"shape":"line"}, render: (args) => ({ components: { Skeleton }, setup: () => ({ args }), template: '<div class="w-64"><Skeleton v-bind="args" /></div>' }) } satisfies Meta<typeof Skeleton>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Avatar: Story = { args: { shape: 'avatar' } }
export const Block: Story = { args: { shape: 'block' } }
