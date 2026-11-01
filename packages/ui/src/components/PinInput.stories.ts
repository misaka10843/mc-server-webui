import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './PinInput.vue'
import Button from './Button.vue'

const meta = {
  title: 'Controls/PinInput', component: Component, tags: ['autodocs'],
  args: {"label":"验证码"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\" />" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Error: Story = {"args":{"error":"验证码已失效。"}}
export const Masked: Story = {"args":{"mask":true}}

