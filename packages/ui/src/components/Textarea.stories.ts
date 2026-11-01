import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Textarea from './Textarea.vue'

const meta = { title: 'Controls/Textarea', component: Textarea, tags: ['autodocs'], args: {"label":"个人简介","description":"最多 200 个字符。"}, render: (args) => ({ components: { Textarea }, setup: () => ({ args, value: ref('') }), template: '<div class="max-w-sm"><Textarea v-bind="args" v-model="value" maxlength="200" /></div>' }) } satisfies Meta<typeof Textarea>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
export const Error: Story = { args: { error: '请检查输入内容。' } }
