import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './PasswordInput.vue'
import Button from './Button.vue'

const meta = {
  title: 'Controls/PasswordInput', component: Component, tags: ['autodocs'],
  args: {"label":"密码","description":"仅展示，不提交数据。"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args, value: ref('') }), template: "<div class=\"max-w-sm\"><Component v-bind=\"args\" v-model=\"value\" autocomplete=\"new-password\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Error: Story = {"args":{"error":"密码不符合要求。"}}

