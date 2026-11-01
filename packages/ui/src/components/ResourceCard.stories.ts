import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import ResourceCard from './ResourceCard.vue'
const meta = { component: ResourceCard, tags: ['autodocs'], title: 'Patterns/ResourceCard', args: { title: 'Moetopia community', description: '社区统一登录', identifier: 'example-client-id', href: '#detail', linkLabel: '应用详情：Moetopia community' } } satisfies Meta<typeof ResourceCard>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
