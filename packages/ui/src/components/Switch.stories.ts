import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Switch from './Switch.vue'

const meta = { title: 'Controls/Switch', component: Switch, tags: ['autodocs'], args: {"label":"邮件通知","description":"关闭后停止接收邮件。"}, render: (args) => ({ components: { Switch }, setup: () => ({ args, value: ref(false) }), template: '<div class="max-w-sm"><Switch v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Switch>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
