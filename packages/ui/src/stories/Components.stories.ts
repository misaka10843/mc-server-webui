import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ComponentGallery from './ComponentGallery.vue'
const meta = { id: 'overview-components', title: 'Overview/组件工作台', component: ComponentGallery, parameters: { layout: 'fullscreen' } } satisfies Meta<typeof ComponentGallery>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
