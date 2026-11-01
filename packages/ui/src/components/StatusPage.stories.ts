import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './StatusPage.vue'
import Button from './Button.vue'
const meta = { title: 'Feedback/StatusPage', component: Component, tags: ['autodocs'], args: { code: '404', title: '好像走到未探索的地方了', description: '这个页面不存在，或地址已经改变。可以回首页重新出发。', illustration: 'not-found' }, render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: '<Component v-bind="args"><template #header><span>Moetopia</span></template><Button>返回首页</Button></Component>' }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const NotFound: Story = {}
export const Restricted: Story = { args: { code: '403', title: '暂时无法进入这里', description: '当前账号没有访问这个页面的权限。', illustration: 'access-restricted' } }
export const Unavailable: Story = { args: { code: '503', title: '暂时没能打开这个页面', description: '请求未能完成，可以稍后重新尝试。', illustration: 'service-unavailable' } }
