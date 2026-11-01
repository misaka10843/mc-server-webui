import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './PageHeading.vue'
import Button from './Button.vue'
const meta = { title: 'Layouts/PageHeading', component: Component, tags: ['autodocs'], args: {"title":"欢迎回来，雨宫澪","description":"你的基础资料与账号状态。","eyebrow":"MOETOPIA ACCOUNT"}, render: args => ({ components: { Component, Button }, setup: () => ({ args }), template: "<Component v-bind=\"args\"><template #actions><Button variant=\"bordered\">查看详情</Button></template></Component>" }) } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}

