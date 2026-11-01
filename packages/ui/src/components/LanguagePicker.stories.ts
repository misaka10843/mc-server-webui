import { ref } from 'vue'
import type { Meta, StoryObj } from '@storybook/vue3-vite'
import LanguagePicker from './LanguagePicker.vue'
const options = [{ value: 'zh-CN', label: '简体中文', shortLabel: '简中' }, { value: 'zh-TW', label: '繁體中文', shortLabel: '繁中' }, { value: 'en', label: 'English', shortLabel: 'EN' }, { value: 'ja', label: '日本語', shortLabel: '日本語' }]
const meta = { title: 'Navigation/LanguagePicker', component: LanguagePicker, tags: ['autodocs'], args: { label: '语言 / Language', options }, render: args => ({ components: { LanguagePicker }, setup: () => ({ args, value: ref('zh-CN') }), template: '<LanguagePicker v-bind="args" v-model="value" />' }) } satisfies Meta<typeof LanguagePicker>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
