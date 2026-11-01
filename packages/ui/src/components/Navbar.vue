<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'
import { DialogRoot, DialogTrigger, DialogPortal, DialogOverlay, DialogContent, DialogTitle, DialogClose } from 'reka-ui'
import type { MoeNavItem } from '../types'
import NavItem from './NavItem.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
const props = withDefaults(defineProps<{ label: string; brand: string; subtitle?: string; brandHref?: string; items: MoeNavItem[]; mobileItems?: MoeNavItem[]; active?: string; menuLabel?: string; closeLabel?: string; breakpoint?: 'tablet' | 'desktop' }>(), { brandHref: '/', menuLabel: '打开导航', closeLabel: '关闭导航', breakpoint: 'desktop' })
const open = defineModel<boolean>('open', { default: false })
const emit = defineEmits<{ navigate: [event: MouseEvent, item: MoeNavItem] }>()
const navigate = (event: MouseEvent, item: MoeNavItem) => { emit('navigate', event, item); open.value = false }
let media: MediaQueryList | undefined
const closeOnDesktop = () => { if (media?.matches) open.value = false }
onMounted(() => { media = window.matchMedia(props.breakpoint === 'tablet' ? '(min-width: 768px)' : '(min-width: 1024px)'); media.addEventListener('change', closeOnDesktop) })
onBeforeUnmount(() => media?.removeEventListener('change', closeOnDesktop))
</script>

<template>
  <header class="moe-navbar" :data-breakpoint="breakpoint">
    <DialogRoot v-model:open="open">
      <DialogTrigger as-child><Button class="moe-navbar-toggle" variant="light" color="default" icon-only :aria-label="menuLabel"><Icon name="menu" /></Button></DialogTrigger>
      <DialogPortal>
        <DialogOverlay class="moe-dialog-overlay fixed inset-0 z-40 bg-overlay" />
        <DialogContent class="moe-drawer moe-drawer-left" :aria-describedby="undefined">
          <div class="moe-drawer-heading"><DialogTitle class="font-semibold">{{ label }}</DialogTitle><DialogClose as-child><Button icon-only variant="light" color="default" :aria-label="closeLabel"><Icon name="close" /></Button></DialogClose></div>
          <nav :aria-label="label" class="moe-mobile-nav"><NavItem v-for="item in mobileItems ?? items" :key="item.id" :item="item" :active="active === item.id" @navigate="navigate" /></nav>
          <div v-if="$slots['mobile-footer']" class="mt-auto border-t border-line pt-4"><slot name="mobile-footer" /></div>
        </DialogContent>
      </DialogPortal>
    </DialogRoot>
    <a :href="brandHref" class="moe-navbar-brand moe-focus" :data-brand-icon="!!$slots['brand-icon'] || undefined"><slot name="brand-icon" /><slot name="brand"><span class="moe-navbar-wordmark"><span>{{ brand }}</span><span v-if="subtitle" class="moe-navbar-subtitle">{{ subtitle }}</span></span></slot></a>
    <nav :aria-label="label" class="moe-navbar-links"><NavItem v-for="item in items" :key="item.id" :item="item" :active="active === item.id" @navigate="navigate" /></nav>
    <div class="moe-navbar-actions"><slot name="actions" /></div>
  </header>
</template>
