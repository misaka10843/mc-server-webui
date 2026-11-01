import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Divider.vue'
import Button from './Button.vue'

const meta = {
  title: 'Foundation/Divider', component: Component, tags: ['autodocs'],
  args: {},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"grid w-60 gap-5\"><span>上方内容</span><Component v-bind=\"args\" /><span>下方内容</span></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


