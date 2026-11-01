import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './DescriptionList.vue'
import Button from './Button.vue'
const meta = { title: 'Feedback/DescriptionList', component: Component, tags: ['autodocs'], args: {"items":[{"key":"name","label":"昵称","value":"演示用户"},{"key":"email","label":"邮箱","value":"demo@example.com"}]}, render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"max-w-lg\"><Component v-bind=\"args\" /></div>" }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}

