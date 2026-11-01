import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Progress.vue'
import Button from './Button.vue'

const meta = {
  title: 'Feedback/Progress', component: Component, tags: ['autodocs'],
  args: {"label":"资料完善程度","value":65,"showValue":true},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"w-72 max-w-full\"><Component v-bind=\"args\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Indeterminate: Story = {"args":{"value":null}}
export const Complete: Story = {"args":{"value":100,"color":"success"}}

