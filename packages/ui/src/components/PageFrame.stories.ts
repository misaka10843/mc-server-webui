import type { Meta, StoryObj } from '@storybook/vue3-vite'
import PageFrame from './PageFrame.vue'
import Navbar from './Navbar.vue'
import PageHeading from './PageHeading.vue'
import StatusIndicator from './StatusIndicator.vue'
import Sidebar from './Sidebar.vue'
const meta = { title: 'Layouts/PageFrame', component: PageFrame, tags: ['autodocs'], parameters: { layout: 'fullscreen' }, args: { skipLabel: '跳转到主要内容' }, render: args => ({ components: { PageFrame, Navbar, PageHeading, StatusIndicator }, setup: () => ({ args }), template: '<PageFrame v-bind="args"><template #header><Navbar label="示例导航" brand="Moetopia" subtitle="账号中心" :items="[]" /></template><PageHeading title="页面标题" description="页框只负责公共结构，不包含路由或账号请求。" /><template #footer><span>© Moetopia</span><StatusIndicator label="演示状态" state="positive" /></template></PageFrame>' }) } satisfies Meta<typeof PageFrame>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const WithSidebar: Story = { render: args => ({ components: { PageFrame, Sidebar, PageHeading }, setup: () => ({ args }), template: '<PageFrame v-bind="args"><template #sidebar><Sidebar label="管理导航" title="Moetopia" :groups="[{label: \'管理台\', items: [{id: \'overview\', label: \'概览\', href: \'#overview\', icon: \'home\'}]}]" active="overview" collapsible /></template><PageHeading title="管理控制台" description="侧栏使用完整视口高度，内容区域独立排列。" /></PageFrame>' }) }
