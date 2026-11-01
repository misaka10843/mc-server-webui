import type { Meta, StoryObj } from '@storybook/vue3-vite'
import WorkspaceLayout from './WorkspaceLayout.vue'
import Sidebar from './Sidebar.vue'
import Card from './Card.vue'
import PageHeading from './PageHeading.vue'
const meta = { title: 'Layouts/WorkspaceLayout', component: WorkspaceLayout, tags: ['autodocs'], render: () => ({ components: { WorkspaceLayout, Sidebar, Card, PageHeading }, template: '<WorkspaceLayout><template #sidebar><Sidebar label="工作区" :groups="[{ label: \'账号\', items: [{ id: \'profile\', label: \'个人资料\', href: \'#profile\', icon: \'user\' }] }]" active="profile" /></template><div class="grid gap-6"><PageHeading title="个人资料" description="宽屏侧栏，窄屏由顶栏导航提供入口。" /><Card title="基本资料">工作区内容示例</Card></div></WorkspaceLayout>' }) } satisfies Meta<typeof WorkspaceLayout>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
