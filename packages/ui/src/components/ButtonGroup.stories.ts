import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './ButtonGroup.vue'
import Button from './Button.vue'

const meta = {
  title: 'Foundation/ButtonGroup', component: Component, tags: ['autodocs'],
  args: {"label":"编辑操作"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><Button variant=\"light\">编辑</Button><Button variant=\"light\">预览</Button><Button variant=\"light\" disabled>发布</Button></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


