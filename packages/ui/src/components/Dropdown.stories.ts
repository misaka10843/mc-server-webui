import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Dropdown.vue'
import Button from './Button.vue'

const meta = {
  title: 'Overlays/Dropdown', component: Component, tags: ['autodocs'],
  args: {"label":"操作菜单","items":[{"id":"profile","label":"个人资料","icon":"user"},{"id":"disabled","label":"暂不可用","disabled":true},{"id":"delete","label":"移除应用","danger":true,"separatorBefore":true}]},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><Button variant=\"bordered\">更多操作</Button></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


