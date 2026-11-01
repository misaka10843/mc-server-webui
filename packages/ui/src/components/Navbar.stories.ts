import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Navbar.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/Navbar', component: Component, tags: ['autodocs'],
  args: {"label":"主导航","brand":"Moetopia","items":[{"id":"home","label":"概览","href":"#home"},{"id":"account","label":"账号中心","href":"#account"},{"id":"community","label":"社区","href":"#community","disabled":true}],"active":"home"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><template #actions><Button size=\"sm\" variant=\"bordered\">登录</Button></template></Component>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}


