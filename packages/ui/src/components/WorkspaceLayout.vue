<template>
  <div class="moe-workspace-layout"><div v-if="$slots.sidebar" class="moe-workspace-sidebar"><slot name="sidebar" /></div><div class="moe-workspace-main"><div v-if="$slots.breadcrumbs" class="mb-6"><slot name="breadcrumbs" /></div><slot /></div></div>
</template>
