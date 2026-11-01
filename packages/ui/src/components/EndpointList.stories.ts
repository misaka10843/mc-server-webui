import type { Meta, StoryObj } from '@storybook/vue3-vite'
import EndpointList from './EndpointList.vue'
const meta = { title: 'Documentation/EndpointList', component: EndpointList, tags: ['autodocs'], args: { label: 'OAuth / OIDC', emptyLabel: '没有匹配的接口', items: [{ id: 'token', method: 'POST', path: '/oauth/token', title: '兑换、刷新或签发令牌', href: '#token' }, { id: 'userinfo', method: 'GET', path: '/oauth/userinfo', title: '获取获准的用户身份信息', href: '#userinfo' }, { id: 'remove', method: 'DELETE', path: '/api/v1/developer/applications/{id}/test-members/{user_id}', title: '移除应用测试成员', href: '#remove' }] } } satisfies Meta<typeof EndpointList>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Empty: Story = { args: { items: [] } }
