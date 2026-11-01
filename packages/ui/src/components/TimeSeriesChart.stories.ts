import type { Meta, StoryObj } from '@storybook/vue3-vite'
import TimeSeriesChart from './TimeSeriesChart.vue'
const meta = { component: TimeSeriesChart, title: 'Patterns/TimeSeriesChart', tags: ['autodocs'], args: { label: '每日授权 · Daily authorizations', missingLabel: '未记录 · Not recorded', partialLabel: '部分日期 · Partial day', points: [{ day: '2026-10-16' }, { day: '2026-10-17', value: 2, partial: true }, { day: '2026-10-18', value: 0 }, { day: '2026-10-19', value: 8 }, { day: '2026-10-20', value: 3 }, { day: '2026-10-21', value: 1, partial: true }] } } satisfies Meta<typeof TimeSeriesChart>
export default meta
type Story = StoryObj<typeof meta>
export const Default: Story = {}
export const Zero: Story = { args: { points: [{ day: '2026-10-20', value: 0 }, { day: '2026-10-21', value: 0, partial: true }] } }
