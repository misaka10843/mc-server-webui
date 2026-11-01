import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { MoeButton, MoeInput, MoeBadge } from '../index'
const meta = { title: 'Foundation/尺寸与变体', render: () => ({ components: { MoeButton, MoeInput, MoeBadge }, template: '<div class="grid gap-6"><div v-for="size in [\'sm\', \'md\', \'lg\']" :key="size" class="flex flex-wrap items-end gap-3"><div class="w-56"><MoeInput label="同尺寸对齐" :size="size" :placeholder="size" /></div><MoeButton :size="size">{{ size }}</MoeButton></div><div v-for="variant in [\'solid\', \'bordered\', \'flat\', \'light\']" :key="variant" class="flex flex-wrap gap-3"><MoeButton v-for="color in [\'primary\',\'secondary\',\'success\',\'warning\',\'danger\',\'info\',\'default\']" :key="color" :color="color" :variant="variant">{{ color }}</MoeButton></div></div>' }) } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
