import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import RepeatableInput from './RepeatableInput.vue'
const meta = { component: RepeatableInput, tags: ['autodocs'], title: 'Controls/RepeatableInput', args: { label: '回调地址', addLabel: '添加回调地址', removeLabel: '移除回调地址', max: 3 }, render: args => ({ components: { RepeatableInput }, setup: () => ({ args, value: ref(['https://example.com/callback']) }), template: '<div class="max-w-lg"><RepeatableInput v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof RepeatableInput>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = { args: { modelValue: ['https://example.com/callback'] } }
export const Disabled: Story = { args: { modelValue: ['https://example.com/callback'], disabled: true } }
