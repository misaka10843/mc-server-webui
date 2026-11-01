import type { Meta, StoryObj } from '@storybook/vue3-vite'
import CopyButton from './CopyButton.vue'
const meta = { title: 'Actions/CopyButton', component: CopyButton, tags: ['autodocs'], args: { value: 'GET /.well-known/openid-configuration', label: '复制', copiedLabel: '已复制', errorLabel: '复制失败' } } satisfies Meta<typeof CopyButton>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
