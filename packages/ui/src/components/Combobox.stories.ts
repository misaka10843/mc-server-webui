import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './Combobox.vue'
const meta = { title: 'Controls/Combobox', component: Component, tags: ['autodocs'], args: {"label":"选择应用","options":[{"value":"community","label":"Moetopia Community"},{"value":"gallery","label":"Personal Gallery"},{"value":"disabled","label":"Archived","disabled":true}]}, render: args => ({ components: { Component }, setup: () => ({ args }), template: '<div class="max-w-sm"><Component v-bind="args" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Error: Story = {"args":{"error":"请选择一个应用。"}}

