import type { Meta, StoryObj } from '@storybook/vue3-vite'
import SecretDisplay from './SecretDisplay.vue'
const meta = { component: SecretDisplay, title: 'Patterns/SecretDisplay', tags: ['autodocs'], args: { label: '一次性凭据 · One-time credential', value: 'EXAMPLE-ONLY-NOT-A-CREDENTIAL', warning: '仅本次显示，请安全保存。Shown once. Store securely.', copyLabel: '复制 · Copy', copiedLabel: '已复制 · Copied', errorLabel: '复制失败 · Copy failed' } } satisfies Meta<typeof SecretDisplay>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
