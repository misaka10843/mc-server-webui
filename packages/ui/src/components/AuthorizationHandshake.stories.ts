import type { Meta, StoryObj } from '@storybook/vue3-vite'
import AuthorizationHandshake from './AuthorizationHandshake.vue'
import BrandMark from './BrandMark.vue'
const meta = { title: 'Identity/AuthorizationHandshake', component: AuthorizationHandshake, tags: ['autodocs'], args: { application: '同人图书馆', provider: 'Moetopia' } } satisfies Meta<typeof AuthorizationHandshake>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Branded: Story = { render: args => ({ components: { AuthorizationHandshake, BrandMark }, setup: () => ({ args }), template: '<AuthorizationHandshake v-bind="args"><template #provider><BrandMark size="lg" /></template></AuthorizationHandshake>' }) }
