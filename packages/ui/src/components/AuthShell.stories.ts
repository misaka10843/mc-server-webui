import type { Meta, StoryObj } from '@storybook/vue3-vite'
import AuthShell from './AuthShell.vue'
import PageHeading from './PageHeading.vue'
import Input from './Input.vue'
import Button from './Button.vue'
const meta = { title: 'Layouts/AuthShell', component: AuthShell, tags: ['autodocs'], args: { skipLabel: '跳转到主要内容', brandLabel: 'Moetopia' }, render: args => ({ components: { AuthShell, PageHeading, Input, Button }, setup: () => ({ args }), template: '<AuthShell v-bind="args"><template #header><a href="#">Moetopia</a><Button variant="light">EN</Button></template><div class="grid gap-6"><PageHeading title="欢迎回来" description="登录你的 Moetopia 账号。"/><Input label="邮箱"/><Button>登录</Button></div><template #footer>© Moetopia</template><template #brand><span class="moe-auth-wordmark">Moetopia</span></template></AuthShell>' }) } satisfies Meta<typeof AuthShell>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
