import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Icon from './Icon.vue'

const meta = { title: 'Foundation/Icon', component: Icon, tags: ['autodocs'], args: { name: 'moon' } } satisfies Meta<typeof Icon>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Sun: Story = { args: { name: 'sun' } }
export const Eye: Story = { args: { name: 'eye' } }
export const EyeOff: Story = { args: { name: 'eye-off' } }
export const Arrow: Story = { args: { name: 'arrow-right' } }
