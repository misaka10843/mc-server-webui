import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ThemePicker from './ThemePicker.vue'
const meta = { title: 'Navigation/ThemePicker', component: ThemePicker, tags: ['autodocs'], args: { label: '切换主题', lightLabel: '浅色', darkLabel: '深色', systemLabel: '跟随系统' }, render: args => ({ components: { ThemePicker }, setup: () => ({ args }), data: () => ({ selection: 'light' as 'light' | 'dark' | 'system' }), template: '<div><ThemePicker v-bind="args" v-model="selection" /><p role="status">{{ selection }}</p></div>' }) } satisfies Meta<typeof ThemePicker>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
