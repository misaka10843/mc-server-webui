import type { Meta, StoryObj } from '@storybook/vue3-vite'
import NavigationTree from './NavigationTree.vue'
const meta = { title: 'Documentation/NavigationTree', component: NavigationTree, tags: ['autodocs'], args: { label: '文档目录', active: 'token', expanded: ['api', 'oauth'], items: [{ id: 'api', label: 'API 参考', children: [{ id: 'oauth', label: 'OAuth / OIDC', children: [{ id: 'token', method: 'POST', label: '兑换令牌', description: '/oauth/token', href: '#token' }, { id: 'userinfo', method: 'GET', label: '用户资料', description: '/oauth/userinfo', href: '#userinfo' }] }] }] } } satisfies Meta<typeof NavigationTree>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
