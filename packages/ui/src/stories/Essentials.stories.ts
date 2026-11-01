import type { Meta, StoryObj } from '@storybook/vue3-vite'
import EssentialsGallery from './EssentialsGallery.vue'
const meta = { id: 'overview-essentials', title: 'Overview/常用组件工作台', component: EssentialsGallery, parameters: { layout: 'fullscreen' } } satisfies Meta<typeof EssentialsGallery>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
