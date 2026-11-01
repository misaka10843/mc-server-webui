import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import Provider from './Provider.vue'
import Dialog from './Dialog.vue'
import Button from './Button.vue'
const meta = { component: Provider, tags: ['autodocs'], title: 'Foundation/Provider', render: () => ({ components: { Provider, Dialog, Button }, setup: () => ({ open: ref(false) }), template: '<Provider><div style="min-height: 150vh"><Dialog v-model:open="open" title="滚动锁定" description="保留滚动条槽，不重复补偿 body。" close-label="关闭"><template #trigger><Button>打开弹窗</Button></template><p>页面位置应保持稳定。</p></Dialog></div></Provider>' }) } satisfies Meta<typeof Provider>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
