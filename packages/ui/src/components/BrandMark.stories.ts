import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './BrandMark.vue'
const meta = { title: 'Brand/BrandMark', component: Component, tags: ['autodocs'], args: { size: 'md' } } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Small: Story = { args: { size: 'sm' } }
export const Large: Story = { args: { size: 'lg' } }
