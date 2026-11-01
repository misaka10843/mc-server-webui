import type { Meta, StoryObj } from '@storybook/vue3-vite'
import FeatureGrid from './FeatureGrid.vue'
const meta = { title: 'Layouts/FeatureGrid', component: FeatureGrid, tags: ['autodocs'], args: { items: [{ id: 'identity', title: '应用信息', description: '让用户识别你的应用。', icon: 'grid' }, { id: 'callback', title: '回调地址', description: '预先注册正确的回调。', icon: 'code' }, { id: 'scopes', title: '最小权限', description: '只申请需要的权限。', icon: 'shield' }] } } satisfies Meta<typeof FeatureGrid>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
