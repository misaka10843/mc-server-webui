import type { Meta, StoryObj } from '@storybook/vue3-vite'
import AuthShell from './AuthShell.vue'
import AuthorizationHandshake from './AuthorizationHandshake.vue'
import ConsentDetails from './ConsentDetails.vue'
import PageHeading from './PageHeading.vue'
import Button from './Button.vue'
const meta = {
  title: 'Pages/Authorization', component: AuthShell, parameters: { layout: 'fullscreen' },
  args: { skipLabel: '跳转到主要内容', brandLabel: 'Moetopia' },
  render: args => ({ components: { AuthShell, AuthorizationHandshake, ConsentDetails, PageHeading, Button }, setup: () => ({ args }), template: '<AuthShell v-bind="args"><template #header>Moetopia · 账号中心</template><div class="moe-authorization"><AuthorizationHandshake application="同人图书馆" provider="Moetopia" /><PageHeading title="确认应用访问" description="同人图书馆正在请求访问你的账户" /><ConsentDetails title="将读取以下账号信息" :items="[{ key: \'name\', label: \'昵称\', field: \'name\', value: \'示例用户\' }, { key: \'email\', label: \'邮箱地址\', field: \'email\', value: \'preview@example.com\' }]" /><p class="text-xs text-muted">你的密码与登录凭证不会共享。</p><div class="grid gap-2.5"><Button size="lg">允许访问</Button><Button size="lg" variant="light" color="default">拒绝</Button></div><p class="moe-consent-return">授权后将返回 https://library.example/callback</p></div><template #brand><div><span class="moe-auth-wordmark">Moetopia</span><h2 class="moe-auth-headline">在这里，与你的世界相遇。</h2></div></template><template #footer>仅为组件预览 · 不会提交真实授权</template></AuthShell>' }),
} satisfies Meta<typeof AuthShell>
export default meta
type Story = StoryObj<typeof meta>
export const Consent: Story = {}
