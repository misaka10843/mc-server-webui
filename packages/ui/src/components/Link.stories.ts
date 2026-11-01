import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Link.vue'
import Button from './Button.vue'

const meta = {
  title: 'Foundation/Link', component: Component, tags: ['autodocs'],
  args: {"href":"#example"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\">查看指南</Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const External: Story = {"args":{"href":"https://ui.kungal.com","external":true}}

