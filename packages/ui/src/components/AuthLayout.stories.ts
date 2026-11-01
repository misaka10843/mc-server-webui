import type { Meta, StoryObj } from '@storybook/vue3-vite'
import AuthLayout from './AuthLayout.vue'
import PageHeading from './PageHeading.vue'
import Input from './Input.vue'
import Button from './Button.vue'
const meta = { title: 'Layouts/AuthLayout', component: AuthLayout, tags: ['autodocs'], render: args => ({ components: { AuthLayout, PageHeading, Input, Button }, setup: () => ({ args }), template: '<AuthLayout v-bind="args"><div class="grid gap-5"><PageHeading title="欢迎回来" description="登录你的 Moetopia 账号。" /><Input label="邮箱" placeholder="you@example.com" /><Button>登录</Button></div></AuthLayout>' }) } satisfies Meta<typeof AuthLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
