import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Accordion.vue'
import Button from './Button.vue'

const meta = {
  title: 'Controls/Accordion', component: Component, tags: ['autodocs'],
  args: {"items":[{"value":"first","title":"什么是统一账号？","description":"使用同一身份访问已接入的应用。"},{"value":"second","title":"如何管理授权？","description":"业务入口在布局阶段接入。"},{"value":"disabled","title":"暂不可用","disabled":true}]},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"max-w-lg\"><Component v-bind=\"args\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}

