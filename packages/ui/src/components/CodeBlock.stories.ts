import type { Meta, StoryObj } from '@storybook/vue3-vite'
import CodeBlock from './CodeBlock.vue'
const meta = { title: 'Content/CodeBlock', component: CodeBlock, tags: ['autodocs'], args: { title: 'Discovery', code: 'GET /.well-known/openid-configuration', copyLabel: '复制', copiedLabel: '已复制', errorLabel: '复制失败' } } satisfies Meta<typeof CodeBlock>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
