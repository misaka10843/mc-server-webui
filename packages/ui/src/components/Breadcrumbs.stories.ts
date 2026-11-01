import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Breadcrumbs.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/Breadcrumbs', component: Component, tags: ['autodocs'],
  args: {"items":[{"label":"首页","href":"#home"},{"label":"账号中心","href":"#account"},{"label":"安全与登录"}]},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\" />" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


