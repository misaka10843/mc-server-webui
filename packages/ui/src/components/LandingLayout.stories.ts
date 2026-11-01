import type { Meta, StoryObj } from '@storybook/vue3-vite'
import LandingLayout from './LandingLayout.vue'
import Link from './Link.vue'
import Card from './Card.vue'
const meta = { title: 'Layouts/LandingLayout', component: LandingLayout, tags: ['autodocs'], args: { title: '把你的应用，接入 Moetopia。', description: '让用户使用同一个账号登录你的站点。' }, render: args => ({ components: { LandingLayout, Link, Card }, setup: () => ({ args }), template: '<LandingLayout v-bind="args"><template #actions><Link href="#guide">阅读接入说明</Link></template><Card id="guide" title="接入流程">先准备应用名称、回调地址与需要的权限。</Card></LandingLayout>' }) } satisfies Meta<typeof LandingLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
