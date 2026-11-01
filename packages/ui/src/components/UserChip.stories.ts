import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './UserChip.vue'
const meta = { title: 'Feedback/UserChip', component: Component, tags: ['autodocs'], args: {"name":"雨宫 澪","description":"个人账号"}, render: args => ({ components: { Component }, setup: () => ({ args }), template: '<div class="max-w-sm"><Component v-bind="args" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


