import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import PasswordFeedback from './PasswordFeedback.vue'
import PasswordInput from './PasswordInput.vue'
const meta = { component: PasswordFeedback, title: 'Patterns/PasswordFeedback', tags: ['autodocs'], args: { value: '', minLength: 15, maxBytes: 256, labels: { title: '密码要求 · Password requirements', minimum: '至少 15 个字符 · At least 15 characters', maximum: '最多 256 字节 · At most 256 bytes', policyHint: '支持空格，不强制大小写、数字或符号。Spaces allowed; no character-class requirement.', strength: '估算强度 · Estimated strength', levels: ['很弱 · Very weak', '较弱 · Weak', '一般 · Fair', '较强 · Strong', '很强 · Very strong'], suggestion: '尝试更长且不常见的独立词组。Try a longer, uncommon passphrase.', checking: '估算中 · Checking', unavailable: '暂不可用 · Unavailable' } }, render: args => ({ components: { PasswordFeedback, PasswordInput }, setup: () => ({ args, password: ref('') }), template: '<div class="grid max-w-md gap-3"><PasswordInput v-model="password" label="新密码 · New password" autocomplete="new-password" /><PasswordFeedback v-bind="args" :value="password" /></div>' }) } satisfies Meta<typeof PasswordFeedback>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
