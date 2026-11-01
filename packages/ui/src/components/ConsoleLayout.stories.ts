import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ConsoleLayout from './ConsoleLayout.vue'
import Card from './Card.vue'
import PageHeading from './PageHeading.vue'
import UserChip from './UserChip.vue'
const meta = {
  title: 'Layouts/ConsoleLayout', component: ConsoleLayout, tags: ['autodocs'],
  args: { label: '控制台', active: 'applications', groups: [{ label: '控制台', items: [{ id: 'applications', label: '我的应用', href: '#apps', icon: 'grid' }, { id: 'docs', label: 'API 文档', href: '#docs', icon: 'code' }] }] },
  render: args => ({ components: { ConsoleLayout, Card, PageHeading, UserChip }, setup: () => ({ args }), template: '<ConsoleLayout v-bind="args"><template #account><Card><UserChip name="示例用户" description="preview@example.com" /></Card></template><div class="grid gap-6"><PageHeading title="我的应用" description="管理应用配置、审核与凭据。" /><Card>应用内容区域</Card></div></ConsoleLayout>' }),
} satisfies Meta<typeof ConsoleLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
