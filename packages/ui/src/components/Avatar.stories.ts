import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Avatar.vue'
import Button from './Button.vue'

const meta = {
  title: 'Feedback/Avatar', component: Component, tags: ['autodocs'],
  args: {"name":"雨宫 澪"},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\" />" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Small: Story = {"args":{"size":"sm"}}
export const Large: Story = {"args":{"size":"lg"}}
export const Square: Story = {"args":{"shape":"square"}}
export const BrokenImage: Story = {"args":{"src":"/missing-avatar.png"}}

