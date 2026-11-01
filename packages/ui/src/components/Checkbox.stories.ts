import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Checkbox from './Checkbox.vue'

const meta = { title: 'Controls/Checkbox', component: Checkbox, tags: ['autodocs'], args: {"label":"接收社区动态","description":"点击标签或按空格切换。"}, render: (args) => ({ components: { Checkbox }, setup: () => ({ args, value: ref(false) }), template: '<div class="max-w-sm"><Checkbox v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Checkbox>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
export const Indeterminate: Story = { render: (args) => ({ components: { Checkbox }, setup: () => ({ args, value: ref<boolean | 'indeterminate'>('indeterminate') }), template: '<Checkbox v-bind="args" v-model="value" />' }) }
