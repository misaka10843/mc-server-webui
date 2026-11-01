import type { Meta, StoryObj } from '@storybook/vue3-vite'
import DocumentLayout from './DocumentLayout.vue'
const meta = { title: 'Documentation/DocumentLayout', component: DocumentLayout, tags: ['autodocs'], args: { label: '本页内容', items: [{ id: 'start', label: '创建应用' }, { id: 'callback', label: '验证回调' }] }, render: args => ({ components: { DocumentLayout }, setup: () => ({ args }), template: '<DocumentLayout v-bind="args"><h1 class="text-2xl font-semibold">授权码登录</h1><section id="start"><h2>创建应用</h2><p>使用标准 OIDC 客户端，按最小权限注册回调与所需范围。</p></section><section id="callback"><h2>验证回调</h2><p>检查 state、nonce、issuer、签名与时效，再建立应用会话。</p></section></DocumentLayout>' }) } satisfies Meta<typeof DocumentLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
