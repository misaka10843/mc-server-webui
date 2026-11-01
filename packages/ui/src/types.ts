export type MoeColor = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'default'
export type MoeSize = 'sm' | 'md' | 'lg'
export type MoeVariant = 'solid' | 'bordered' | 'flat' | 'light'
export interface MoeOption { value: string; label: string; description?: string; disabled?: boolean }
export type MoeIconName = 'languages' | 'sun' | 'moon' | 'eye' | 'eye-off' | 'arrow-right' | 'arrow-left' | 'pencil' | 'trash' | 'copy' | 'chevron-left' | 'chevron-right' | 'chevron-down' | 'menu' | 'close' | 'home' | 'user' | 'shield' | 'grid' | 'code' | 'settings' | 'logout' | 'search' | 'bell' | 'check' | 'plus' | 'inbox' | 'external'
export interface MoeNavItem { id: string; label: string; href: string; icon?: MoeIconName; badge?: string; disabled?: boolean }
export interface MoeNavGroup { label: string; items: MoeNavItem[] }
export interface MoeBreadcrumbItem { label: string; href?: string }
export interface MoeMenuItem { id: string; label: string; icon?: MoeIconName; description?: string; shortcut?: string; disabled?: boolean; danger?: boolean; separatorBefore?: boolean }
export interface MoeTableColumn { key: string; label: string; align?: 'start' | 'end'; sortable?: boolean }
export interface MoeAccordionItem { value: string; title: string; description?: string; disabled?: boolean }
export interface MoeSchemaField { name: string; type: string; required: boolean; description?: string; constraints?: string[]; children?: MoeSchemaField[] }
export interface MoeTreeEntry { id: string; label: string; href?: string; description?: string; method?: string; children?: MoeTreeEntry[] }
