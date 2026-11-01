import type { Meta, StoryObj } from '@storybook/vue3-vite'
import ScrollArea from './ScrollArea.vue'
const meta = { title: 'Foundation/ScrollArea', component: ScrollArea, tags: ['autodocs'], args: { label: '示例长列表', height: '240px' }, render: args => ({ components: { ScrollArea }, setup: () => ({ args }), template: '<div class="max-w-sm"><ScrollArea v-bind="args"><ul class="divide-y divide-line"><li v-for="index in 30" :key="index" class="px-4 py-3 text-sm">示例条目 {{ index }}</li></ul></ScrollArea></div>' }) } satisfies Meta<typeof ScrollArea>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
