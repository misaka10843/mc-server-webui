import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Tooltip from './Tooltip.vue'
import Button from './Button.vue'
const meta = { title: 'Overlays/Tooltip', component: Tooltip, tags: ['autodocs'], args: { text: '鼠标悬停或键盘聚焦均可显示' }, render: (args) => ({ components: { Tooltip, Button }, setup: () => ({ args }), template: '<Tooltip v-bind="args"><Button variant="bordered">查看提示</Button></Tooltip>' }) } satisfies Meta<typeof Tooltip>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const LongText: Story = { args: { text: '说明较长时应换行，不超出屏幕边缘。A long description wraps within the viewport.' } }
