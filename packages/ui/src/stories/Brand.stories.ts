import type { Meta, StoryObj } from '@storybook/vue3-vite'
import BrandGallery from './BrandGallery.vue'
const meta = { id: 'overview-brand', title: 'Overview/看板娘与品牌配色', component: BrandGallery, parameters: { layout: 'fullscreen' } } satisfies Meta<typeof BrandGallery>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
