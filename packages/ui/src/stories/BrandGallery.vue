<script setup lang="ts">
import { ref } from 'vue'
import mascot from '../assets/mascot-mint.png'
import { MoeButton, MoeInput, MoeTabs, MoeBadge, MoeSwitch, MoeIcon } from '../index'
const palette = [
  { name: '薄荷', detail: '头发与领带', token: '--moe-brand-mint' },
  { name: '雾蓝', detail: '发梢与阴影', token: '--moe-brand-fog' },
  { name: '蓝灰', detail: '外套与轮廓', token: '--moe-brand-navy' },
  { name: '浅桃', detail: '肤色与暖意', token: '--moe-brand-peach' },
]
const email = ref('')
const tab = ref('account')
const notifications = ref(true)
</script>
<template>
  <div class="mx-auto grid max-w-5xl gap-8 text-foreground">
    <header class="grid gap-2"><p class="text-xs font-medium tracking-widest text-primary">MOETOPIA · CHARACTER & COLOR</p><h1 class="text-2xl font-semibold">薄荷与雾蓝</h1><p class="max-w-xl text-sm leading-7 text-muted">从看板娘的发色、外套和细节延伸出轻柔的配色，保留清晰、轻快的组件交互。</p></header>
    <div class="grid items-start gap-8 md:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)]">
      <figure class="overflow-hidden rounded-2xl border border-line bg-white"><img :src="mascot" width="1086" height="1448" alt="Moetopia 候选看板娘：薄荷绿短发、C++ 发夹、深蓝灰连帽外套" class="mx-auto max-h-[640px] w-full object-contain" /><figcaption class="border-t border-line px-4 py-3 text-center text-xs text-[var(--moe-brand-navy)]">用户提供的候选立绘 · 原图预览</figcaption></figure>
      <div class="grid gap-7">
        <section aria-label="角色参考色" class="grid grid-cols-2 gap-3"><div v-for="color in palette" :key="color.name" class="overflow-hidden rounded-xl border border-line bg-surface"><div class="h-16" :style="{ background: `var(${color.token})` }" /><div class="grid gap-1 p-3"><p class="text-sm font-medium">{{ color.name }}</p><p class="text-xs text-muted">{{ color.detail }}</p></div></div></section>
        <section aria-label="品牌组件组合" class="grid gap-5 rounded-2xl border border-line bg-surface p-5"><div class="flex items-center justify-between gap-3"><h2 class="font-semibold">与你喜欢的世界相连</h2><MoeBadge>Moetopia</MoeBadge></div><MoeTabs v-model="tab" label="品牌预览标签" :items="[{ value: 'account', label: '账号' }, { value: 'security', label: '安全' }, { value: 'apps', label: '应用' }]"><template #account><p class="text-sm text-muted">一个账号，连接属于你的社区与创作。</p></template><template #security><p class="text-sm text-muted">安全设置使用同一套安静、清晰的视觉。</p></template><template #apps><p class="text-sm text-muted">品牌色贯穿导航、应用与操作状态。</p></template></MoeTabs><MoeInput v-model="email" label="邮箱" placeholder="you@example.com" description="纯组件展示，不会提交信息。" /><MoeSwitch v-model="notifications" label="接收社区动态" /><div class="flex flex-wrap gap-3"><MoeButton>继续<MoeIcon name="arrow-right" /></MoeButton><MoeButton variant="bordered" color="secondary">了解更多</MoeButton><MoeButton variant="light">稍后再说</MoeButton></div></section>
        <p class="text-xs leading-6 text-muted">浅色以暖白和薄荷为主；暗色取外套的深蓝灰。浅薄荷用于装饰与选中底色，正文和浅色主题主按钮采用更深的颜色保证辨识度。</p>
      </div>
    </div>
  </div>
</template>
