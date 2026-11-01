<template>
  <div class="moe-profile-layout" :data-summary="!!$slots.summary">
    <aside v-if="$slots.summary" class="moe-profile-summary"><slot name="summary" /></aside>
    <div class="moe-profile-content"><slot /></div>
  </div>
</template>
