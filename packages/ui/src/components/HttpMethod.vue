<script setup lang="ts">
defineProps<{ method: string }>()
</script>
<template><span class="moe-http-method" :data-method="method.toLowerCase()">{{ method.toUpperCase() }}</span></template>
