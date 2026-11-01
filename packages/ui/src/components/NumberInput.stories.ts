import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './NumberInput.vue'
const meta = { title: 'Controls/NumberInput', component: Component, tags: ['autodocs'], args: {"label":"每页条目数","min":1,"max":100,"modelValue":20}, render: args => ({ components: { Component }, setup: () => ({ args, value: ref(args.modelValue) }), template: '<div class="max-w-sm"><Component v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Error: Story = {"args":{"error":"请输入有效数量。"}}

