import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Tabs from './Tabs.vue'

const meta = { title: 'Controls/Tabs', component: Tabs, tags: ['autodocs'], args: {"label":"账号设置","items":[{"value":"account","label":"账号","description":"账号设置内容"},{"value":"security","label":"安全","description":"安全设置内容"},{"value":"apps","label":"应用","disabled":true}]}, render: (args) => ({ components: { Tabs }, setup: () => ({ args, value: ref('account') }), template: '<div class="max-w-sm"><Tabs v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof Tabs>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Underline: Story = { args: { variant: 'underline' } }
export const FullWidth: Story = { args: { fullWidth: true } }
export const LongLabels: Story = { args: { items: [{ value: 'account', label: '个人资料与偏好设置', description: '长标签可横向滚动。' }, { value: 'security', label: 'Security & sign-in methods', description: 'Keyboard navigation remains available.' }, { value: 'apps', label: '应用与授权管理', description: '已授权应用。' }] } }
export const ManualActivation: Story = { args: { activationMode: 'manual' } }
