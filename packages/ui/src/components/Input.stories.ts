import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Input from './Input.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
import { ref } from 'vue'

const meta = { title: 'Foundation/Input', component: Input, tags: ['autodocs'], args: { label: '邮箱 · Email', type: 'email', autocomplete: 'email' } } satisfies Meta<typeof Input>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Error: Story = { args: { error: '请输入有效邮箱。Enter a valid email address.' } }
export const Disabled: Story = { args: { disabled: true } }
export const Description: Story = { args: { description: '用于接收验证码。Used for verification emails.' } }
export const TrailingAction: Story = {
  args: { label: '密码 · Password', type: 'password', autocomplete: 'new-password' },
  render: (args) => ({ components: { Input, Button, Icon }, setup: () => ({ args, shown: ref(false) }), template: '<Input v-bind="args" :type="shown ? \'text\' : \'password\'"><template #trailing><Button variant="quiet" size="icon" :aria-label="shown ? \'隐藏密码 · Hide password\' : \'显示密码 · Show password\'" :aria-pressed="shown" @click="shown = !shown"><Icon :name="shown ? \'eye-off\' : \'eye\'" /></Button></template></Input>' }),
}
