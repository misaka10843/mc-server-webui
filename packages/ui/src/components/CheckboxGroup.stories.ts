import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Component from './CheckboxGroup.vue'
const meta = { title: 'Controls/CheckboxGroup', component: Component, tags: ['autodocs'], args: {"label":"显示的通知","options":[{"value":"security","label":"安全提醒"},{"value":"community","label":"社区动态"},{"value":"reserved","label":"其他通知","disabled":true}],"modelValue":["security"]}, render: args => ({ components: { Component }, setup: () => ({ args, value: ref([...(args.modelValue ?? [])]) }), template: '<div class="max-w-sm"><Component v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = {"args":{"disabled":true}}
export const Cards: Story = { args: { variant: 'cards' } }

