import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import RadioGroup from './RadioGroup.vue'

const meta = { title: 'Controls/RadioGroup', component: RadioGroup, tags: ['autodocs'], args: {"label":"资料可见性","options":[{"value":"private","label":"仅自己"},{"value":"public","label":"公开"},{"value":"team","label":"仅团队","disabled":true}]}, render: (args) => ({ components: { RadioGroup }, setup: () => ({ args, value: ref('private') }), template: '<div class="max-w-sm"><RadioGroup v-bind="args" v-model="value" /></div>' }) } satisfies Meta<typeof RadioGroup>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }
