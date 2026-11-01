import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Kbd.vue'
import Button from './Button.vue'

const meta = {
  title: 'Foundation/Kbd', component: Component, tags: ['autodocs'],
  args: {},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"flex items-center gap-2\"><Component v-bind=\"args\">Ctrl</Component><Component>K</Component></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


