import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './NavItem.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/NavItem', component: Component, tags: ['autodocs'],
  args: {"item":{"id":"account","label":"账号中心","href":"#account","icon":"user"},"active":true},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"max-w-xs\"><Component v-bind=\"args\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"item":{"id":"disabled","label":"暂不可用","href":"#disabled","icon":"grid","disabled":true}}}
export const Compact: Story = {"args":{"compact":true}}

