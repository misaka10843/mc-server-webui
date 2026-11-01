import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Popover.vue'
import Button from './Button.vue'

const meta = {
  title: 'Overlays/Popover', component: Component, tags: ['autodocs'],
  args: {"label":"筛选条件"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><template #trigger><Button variant=\"bordered\">打开筛选</Button></template><p class=\"text-sm leading-6\">筛选表单或上下文说明。</p></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


