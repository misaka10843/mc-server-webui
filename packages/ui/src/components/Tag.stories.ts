import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Tag.vue'
import Button from './Button.vue'

const meta = {
  title: 'Feedback/Tag', component: Component, tags: ['autodocs'],
  args: {"label":"OpenID Connect","removable":true},
  render: args => ({ components: { Component, Button }, setup: () => ({ args, visible: ref(true) }), template: "<Component v-if=\"visible\" v-bind=\"args\" @remove=\"visible = false\" />" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Plain: Story = {"args":{"removable":false}}

