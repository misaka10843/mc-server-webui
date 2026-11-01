import type { Meta, StoryObj } from '@storybook/vue3-vite'
import SchemaFields from './SchemaFields.vue'
const meta = { title: 'Documentation/SchemaFields', component: SchemaFields, tags: ['autodocs'], args: { requiredLabel: '必填', optionalLabel: '可选', emptyLabel: '无字段', fields: [{ name: 'grant_type', type: 'string', required: true, description: '使用的授权流程', constraints: ['enum: authorization_code, refresh_token'] }, { name: 'config', type: 'object', required: true, description: '应用配置', children: [{ name: 'redirect_uris', type: 'array', required: true, constraints: ['maxItems: 5'], children: [{ name: '[]', type: 'string', required: false, constraints: ['format: uri'] }] }] }] } } satisfies Meta<typeof SchemaFields>
export default meta
type Story = StoryObj<typeof meta>
export const Nested: Story = {}
export const Empty: Story = { args: { fields: [] } }
