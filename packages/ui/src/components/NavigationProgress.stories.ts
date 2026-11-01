import { ref } from 'vue'
import type { Meta, StoryObj } from '@storybook/vue3-vite'
import NavigationProgress from './NavigationProgress.vue'
import Button from './Button.vue'
const meta = { title: 'Feedback/NavigationProgress', component: NavigationProgress, tags: ['autodocs'], args: { active: true, value: 35, label: '正在加载页面 / Loading page' } } satisfies Meta<typeof NavigationProgress>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Failed: Story = { args: { error: true, value: 100 } }
export const Controlled: Story = { render: args => ({ components: { NavigationProgress, Button }, setup: () => ({ args, active: ref(false) }), template: '<NavigationProgress v-bind="args" :active="active"/><div class="flex gap-3"><Button @click="active = true">开始加载</Button><Button @click="active = false">完成</Button></div>' }) }
