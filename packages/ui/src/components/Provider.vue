<script setup lang="ts">
import { ConfigProvider } from 'reka-ui'
withDefaults(defineProps<{ locale?: string }>(), { locale: 'zh-CN' })
</script>
<template><ConfigProvider :locale="locale" :scroll-body="{ padding: 0, margin: 0 }"><slot /></ConfigProvider></template>
