import type { Meta, StoryObj } from '@storybook/vue3-vite'
import HttpMethod from './HttpMethod.vue'
const meta = { title: 'Documentation/HttpMethod', component: HttpMethod, tags: ['autodocs'], args: { method: 'GET' } } satisfies Meta<typeof HttpMethod>
export default meta
type Story = StoryObj<typeof meta>
export const Get: Story = {}
export const Post: Story = { args: { method: 'POST' } }
export const Delete: Story = { args: { method: 'DELETE' } }
