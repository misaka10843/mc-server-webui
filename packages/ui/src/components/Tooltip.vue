<script setup lang="ts">
import { TooltipProvider, TooltipRoot, TooltipTrigger, TooltipPortal, TooltipContent } from 'reka-ui'
withDefaults(defineProps<{ text: string; side?: 'top' | 'right' | 'bottom' | 'left' }>(), { side: 'top' })
</script>
<template><TooltipProvider :delay-duration="300"><TooltipRoot><TooltipTrigger as-child><slot /></TooltipTrigger><TooltipPortal><TooltipContent :side="side" :side-offset="7" class="moe-popup moe-popover max-w-64 px-3 py-2 text-xs leading-5">{{ text }}</TooltipContent></TooltipPortal></TooltipRoot></TooltipProvider></template>
