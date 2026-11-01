import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Drawer.vue'
import Button from './Button.vue'

const meta = {
  title: 'Overlays/Drawer', component: Component, tags: ['autodocs'],
  args: {"title":"应用详情","description":"保留当前页面上下文。"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><template #trigger><Button variant=\"bordered\">打开抽屉</Button></template><p class=\"text-sm leading-7\">抽屉内容可滚动，Escape 关闭，焦点返回触发按钮。</p><template #footer=\"{ close }\"><Button @click=\"close\">完成</Button></template></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Left: Story = {"args":{"side":"left"}}

