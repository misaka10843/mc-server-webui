import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Select from './Select.vue'

const meta = { title: 'Controls/Select', component: Select, tags: ['autodocs'], args: {"label":"语言","description":"选择界面语言。","options":[{"value":"zh-CN","label":"简体中文"},{"value":"en","label":"English"},{"value":"ja","label":"日本語","disabled":true}]}, render: (args) => ({ components: { Select }, setup: () => ({ args, value: ref('') }), template: '<div class="max-w-sm"><Select v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Select>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
export const Error: Story = { args: { error: '请检查输入内容。' } }
