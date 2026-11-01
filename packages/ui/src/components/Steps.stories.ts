import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Steps.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/Steps', component: Component, tags: ['autodocs'],
  args: {"label":"接入步骤","current":"review","items":[{"value":"create","label":"创建应用"},{"value":"review","label":"提交审核"},{"value":"publish","label":"正式发布"}]},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"w-full max-w-2xl\"><Component v-bind=\"args\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


