import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './SettingRow.vue'
import Button from './Button.vue'
const meta = { title: 'Layouts/SettingRow', component: Component, tags: ['autodocs'], args: {"title":"当前会话","description":"最近的账号中心会话。","icon":"shield"}, render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"max-w-xl\"><Component v-bind=\"args\"><template #actions><Button variant=\"light\" color=\"danger\">结束会话</Button></template></Component></div>" }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Inset: Story = { args: { inset: true } }

