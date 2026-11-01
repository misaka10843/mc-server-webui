import type { MoeNavItem, MoeNavGroup, MoeMenuItem } from '../types'
export const navigationItems: MoeNavItem[] = [
  { id: 'home', label: '概览', href: '#home', icon: 'home' },
  { id: 'account', label: '账号中心', href: '#account', icon: 'user' },
  { id: 'developer', label: '开发者', href: '#developer', icon: 'code' },
  { id: 'community', label: '社区', href: '#community', icon: 'grid', disabled: true },
]
export const navigationGroups: MoeNavGroup[] = [
  { label: '个人空间', items: [navigationItems[0]!, navigationItems[1]!, { id: 'security', label: '安全与登录', href: '#security', icon: 'shield' }] },
  { label: '开放平台', items: [{ id: 'apps', label: '我的应用', href: '#apps', icon: 'grid', badge: '3' }, navigationItems[2]!, navigationItems[3]!] },
]
export const menuItems: MoeMenuItem[] = [
  { id: 'profile', label: '个人资料', icon: 'user', description: '查看与编辑个人信息' },
  { id: 'settings', label: '偏好设置', icon: 'settings', shortcut: '⌘ ,' },
  { id: 'admin', label: '管理控制台', icon: 'shield', disabled: true },
  { id: 'logout', label: '退出登录', icon: 'logout', danger: true, separatorBefore: true },
]
