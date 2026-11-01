import type { Meta, StoryObj } from '@storybook/vue3-vite'
import Component from './Illustration.vue'
import { illustrations } from '../illustrations'
const meta = { title: 'Brand/Illustration', component: Component, tags: ['autodocs'], args: { name: 'auth-welcome', size: 'hero' }, argTypes: { name: { control: 'select', options: Object.keys(illustrations) } } } satisfies Meta<typeof Component>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Gallery: Story = { render: () => ({ components: { Component }, setup: () => ({ names: Object.keys(illustrations) }), template: '<div class="grid grid-cols-2 gap-8 sm:grid-cols-4"><figure v-for="name in names" :key="name" class="grid justify-items-center gap-3"><Component :name="name" /><figcaption class="text-xs text-muted">{{ name }}</figcaption></figure></div>' }) }
export const DesktopOnly: Story = { args: { desktopOnly: true } }
