import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Button from './Button.vue'
import Icon from './Icon.vue'

const meta = { title: 'Foundation/Button', component: Button, tags: ['autodocs'], render: (args) => ({ components: { Button }, setup: () => ({ args }), template: '<Button v-bind="args">继续 · Continue</Button>' }) } satisfies Meta<typeof Button>
export default meta
type Story = StoryObj<typeof meta>
export const Primary: Story = { args: { variant: 'primary' } }
export const Secondary: Story = { args: { variant: 'secondary' } }
export const Loading: Story = { args: { loading: true } }
export const Disabled: Story = { args: { disabled: true } }
export const IconOnly: Story = { args: { size: 'icon', variant: 'quiet' }, render: (args) => ({ components: { Button, Icon }, setup: () => ({ args }), template: '<Button v-bind="args" aria-label="切换主题 · Change theme"><Icon name="moon" /></Button>' }) }
