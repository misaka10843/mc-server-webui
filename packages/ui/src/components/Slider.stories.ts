import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Slider.vue'
import Button from './Button.vue'

const meta = {
  title: 'Controls/Slider', component: Component, tags: ['autodocs'],
  args: {"label":"预览音量","showValue":true},
  render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<div class=\"w-72 max-w-full\"><Component v-bind=\"args\" /></div>" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Range: Story = {"args":{"modelValue":[20,80]}}

