import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { MoeAlert, MoeBadge, MoeCard, MoeSkeleton, MoeSpinner, MoeTooltip, MoeButton } from '../index'
const meta = { title: 'Feedback/状态与容器', render: () => ({ components: { MoeAlert, MoeBadge, MoeCard, MoeSkeleton, MoeSpinner, MoeTooltip, MoeButton }, template: '<div class="grid max-w-lg gap-5"><MoeAlert title="操作完成" color="success">资料已保存。</MoeAlert><MoeAlert title="请检查输入" color="danger">错误信息由文字说明。</MoeAlert><div class="flex flex-wrap gap-2"><MoeBadge color="primary">待审核</MoeBadge><MoeBadge color="success">已发布</MoeBadge><MoeBadge color="danger" variant="bordered">已暂停</MoeBadge></div><MoeCard title="应用资料" description="边框与层次示例"><p class="text-sm">这里是卡片内容。</p></MoeCard><MoeSpinner label="正在加载…" /><MoeSkeleton /><MoeTooltip text="键盘聚焦同样显示"><MoeButton variant="bordered">查看提示</MoeButton></MoeTooltip></div>' }) } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
