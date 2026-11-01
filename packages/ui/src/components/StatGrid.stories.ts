import type { Meta, StoryObj } from '@storybook/vue3-vite'
import StatGrid from './StatGrid.vue'
const meta = { title: 'Data/StatGrid', component: StatGrid, tags: ['autodocs'], args: { items: [{ id: 'users', label: '账号', icon: 'user' }, { id: 'apps', label: '应用', icon: 'grid' }, { id: 'reviews', label: '审核', icon: 'shield' }] } } satisfies Meta<typeof StatGrid>
export default meta
type Story = StoryObj<typeof meta>
export const Unavailable: Story = {}
