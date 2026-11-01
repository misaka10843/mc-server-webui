<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick, useId } from 'vue'
import type { MoeOption } from '../types'
import Dialog from './Dialog.vue'
import Button from './Button.vue'
import Icon from './Icon.vue'
import Kbd from './Kbd.vue'
import Input from './Input.vue'
const props = defineProps<{ title: string; placeholder: string; closeLabel: string; emptyLabel: string; items: MoeOption[] }>()
const emit = defineEmits<{ select: [value: string] }>()
const open = ref(false)
const query = ref('')
const inputId = useId()
const resultsId = useId()
const results = computed(() => { const search = query.value.trim().toLocaleLowerCase(); return props.items.filter(item => !item.disabled && `${item.label} ${item.description ?? ''}`.toLocaleLowerCase().includes(search)) })
watch(open, () => { query.value = '' })
const choose = (value?: string) => { if (!value) return; open.value = false; emit('select', value) }
const focusInput = async (event: Event) => { event.preventDefault(); await nextTick(); document.getElementById(inputId)?.focus() }
const move = (index: number) => { const buttons = document.getElementById(resultsId)?.querySelectorAll('button'); if (buttons?.length) buttons[(index + buttons.length) % buttons.length]?.focus() }
const focusSearch = () => { document.getElementById(inputId)?.focus() }
const shortcut = (event: KeyboardEvent) => { if (!event.repeat && (event.ctrlKey || event.metaKey) && !event.altKey && event.key.toLowerCase() === 'k') { event.preventDefault(); open.value = !open.value } }
onMounted(() => { window.addEventListener('keydown', shortcut) })
onBeforeUnmount(() => { window.removeEventListener('keydown', shortcut) })
</script>
<template><Dialog v-model:open="open" :title="title" :close-label="closeLabel" :show-close-action="false" @open-auto-focus="focusInput"><template #trigger><Button class="moe-search-trigger" color="default" variant="bordered"><Icon name="search" class="size-4" /><span>{{ placeholder }}</span><Kbd>Ctrl K</Kbd></Button></template><Input :id="inputId" v-model="query" :label="title" :placeholder="placeholder" type="search" autocomplete="off" :aria-controls="resultsId" @keydown.down.prevent="move(0)" @keydown.enter.prevent="choose(results[0]?.value)" /><nav :id="resultsId" class="moe-search-results" :aria-label="title"><button v-for="(item, index) in results" :key="item.value" type="button" class="moe-focus" @click="choose(item.value)" @keydown.down.prevent="move(index + 1)" @keydown.up.prevent="index ? move(index - 1) : focusSearch()"><span>{{ item.label }}</span><small v-if="item.description">{{ item.description }}</small></button><p v-if="!results.length" role="status" class="px-3 py-6 text-center text-sm text-muted">{{ emptyLabel }}</p></nav></Dialog></template>
