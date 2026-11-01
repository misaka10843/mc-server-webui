import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './AvatarGroup.vue'
const meta = { title: 'Feedback/AvatarGroup', component: Component, tags: ['autodocs'], args: {"label":"协作成员","items":[{"id":"1","name":"雨宫 澪"},{"id":"2","name":"白石 凛"},{"id":"3","name":"松永 葵"},{"id":"4","name":"小春"},{"id":"5","name":"Alice"}],"max":3}, render: args => ({ components: { Component }, setup: () => ({ args }), template: '<div class="max-w-sm"><Component v-bind="args" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Small: Story = {"args":{"size":"sm"}}
export const Large: Story = {"args":{"size":"lg"}}

