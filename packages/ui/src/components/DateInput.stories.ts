import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './DateInput.vue'
const meta = { title: 'Controls/DateInput', component: Component, tags: ['autodocs'], args: {"label":"生效日期","min":"2026-01-01","max":"2027-12-31"}, render: args => ({ components: { Component }, setup: () => ({ args }), template: '<div class="max-w-sm"><Component v-bind="args" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Error: Story = {"args":{"error":"请选择有效日期。"}}

