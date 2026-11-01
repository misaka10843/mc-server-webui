import type { Meta, StoryObj } from '@storybook/vue3-vite'
import NavigationGallery from './NavigationGallery.vue'
const meta = { id: 'overview-navigation', title: 'Overview/导航组件工作台', component: NavigationGallery, parameters: { layout: 'fullscreen' } } satisfies Meta<typeof NavigationGallery>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
