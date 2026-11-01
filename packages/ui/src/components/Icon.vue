<script setup lang="ts">
import type { MoeIconName } from '../types'
defineProps<{ name: MoeIconName }>()
const paths: Record<MoeIconName, string[]> = {
  languages: ['M3 5h12M9 3v2M5 5c1 5 4 8 9 10M13 5c-1 5-4 8-9 10', 'm13 21 4-10 4 10m-6-4h4'],
  sun: ['M12 3V1m0 22v-2M3 12H1m22 0h-2M4.2 4.2l1.4 1.4m12.8 12.8 1.4 1.4m0-15.6-1.4 1.4M5.6 18.4l-1.4 1.4', 'M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z'],
  moon: ['M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11Z'],
  eye: ['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z', 'M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z'],
  'eye-off': ['m3 3 18 18M9.9 5.2A12 12 0 0 1 12 5c6.5 0 10 7 10 7a17 17 0 0 1-3.2 4.2M6.2 6.2A18 18 0 0 0 2 12s3.5 7 10 7a12 12 0 0 0 5.8-1.5', 'M10 10a2.8 2.8 0 0 0 4 4'],
  'arrow-right': ['M4 12h16m-6-6 6 6-6 6'],
  'arrow-left': ['M20 12H4m6-6-6 6 6 6'],
  pencil: ['m16 3 5 5L9 20l-6 1 1-6Z', 'm14 5 5 5'],
  trash: ['M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15', 'M10 10v7m4-7v7'],
  copy: ['M9 9h12v12H9Z', 'M5 15H3V3h12v2'],
  'chevron-left': ['m15 6-6 6 6 6'],
  'chevron-right': ['m9 6 6 6-6 6'],
  'chevron-down': ['m6 9 6 6 6-6'],
  menu: ['M4 6h16M4 12h16M4 18h16'],
  close: ['m6 6 12 12M6 18 18 6'],
  home: ['m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-8H9v8H4a1 1 0 0 1-1-1Z'],
  user: ['M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z', 'M4 21v-2a8 8 0 0 1 16 0v2'],
  shield: ['m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6Z', 'm8 12 3 3 5-6'],
  grid: ['M3 3h7v7H3ZM14 3h7v7h-7ZM3 14h7v7H3ZM14 14h7v7h-7Z'],
  code: ['m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18'],
  settings: ['M12 8a4 4 0 1 1 0 8 4 4 0 0 1 0-8Z', 'm9 3-1 3-3 1-2 3 2 2-1 3 2 3 3-1 3 2 3-1 1-3 3-1 2-3-2-2 1-3-2-3-3 1-3-2Z'],
  logout: ['M9 4H4v16h5m5-4 4-4-4-4m-6 4h13'],
  search: ['M18 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z', 'm15 15 6 6'],
  bell: ['M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4'],
  check: ['m5 12 4 4L19 6'],
  plus: ['M12 4v16M4 12h16'],
  inbox: ['M4 4h16l2 12v4H2v-4Zm-2 12h6l2 3h4l2-3h6'],
  external: ['M14 3h7v7m0-7L10 14M10 3H3v18h18v-7'],
}
</script>

<template>
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    <path v-for="(path, index) in paths[name]" :key="index" :d="path" />
  </svg>
</template>
