import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Dialog from './Dialog.vue'
import Button from './Button.vue'

const meta = {
  title: 'Foundation/Dialog', component: Dialog, tags: ['autodocs'],
  args: { title: '授权说明 · Authorization', description: '请确认应用请求的权限。Review the permissions requested by this application.', closeLabel: '关闭 · Close' },
  render: (args) => ({ components: { Dialog, Button }, setup: () => ({ args }), template: '<Dialog v-bind="args"><template #trigger><Button>打开 · Open</Button></template></Dialog>' }),
} satisfies Meta<typeof Dialog>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
