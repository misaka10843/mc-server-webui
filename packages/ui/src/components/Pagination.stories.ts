import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './Pagination.vue'
import Button from './Button.vue'

const meta = {
  title: 'Navigation/Pagination', component: Component, tags: ['autodocs'],
  args: {"total":200},
  render: args => ({ components: { Component, Button }, setup: () => ({ args, value: ref(1) }), template: "<Component v-bind=\"args\" v-model:page=\"value\" />" }),
} satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const SinglePage: Story = {"args":{"total":8}}
export const Empty: Story = {"args":{"total":0}}

