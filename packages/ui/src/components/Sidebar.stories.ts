import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Sidebar.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/Sidebar', component: Component, tags: ['autodocs'],
  args: {"label":"个人空间","groups":[{"label":"账号","items":[{"id":"profile","label":"个人资料","href":"#profile","icon":"user"},{"id":"security","label":"安全与登录","href":"#security","icon":"shield"}]}],"active":"profile","collapsible":true},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><template #header><span class=\"text-sm font-medium\">个人空间</span></template></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Collapsed: Story = {"args":{"collapsed":true}}

