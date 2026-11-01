import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Spinner from './Spinner.vue'
const meta = { title: 'Feedback/Spinner', component: Spinner, tags: ['autodocs'], args: {"label":"正在加载…"}, render: (args) => ({ components: { Spinner }, setup: () => ({ args }), template: '<Spinner v-bind="args" />' }) } satisfies Meta<typeof Spinner>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const English: Story = { args: { label: 'Loading…' } }
