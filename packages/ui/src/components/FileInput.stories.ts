import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './FileInput.vue'
const meta = { title: 'Controls/FileInput', component: Component, tags: ['autodocs'], args: {"label":"选择图片","accept":"image/*","description":"只选择文件，不会上传。"}, render: args => ({ components: { Component }, setup: () => ({ args }), template: '<div class="max-w-sm"><Component v-bind="args" /></div>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Multiple: Story = {"args":{"multiple":true}}
export const Disabled: Story = {"args":{"disabled":true}}

