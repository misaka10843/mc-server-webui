import type { Meta, StoryObj } from '@storybook/vue3-vite'
import QrCode from './QrCode.vue'
const meta = { component: QrCode, title: 'Patterns/QrCode', tags: ['autodocs'], args: { value: 'https://example.com', label: '示例二维码 · Example QR code', errorLabel: '无法生成二维码 · QR generation failed' } } satisfies Meta<typeof QrCode>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
