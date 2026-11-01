# Moetopia UI

当前进入页面设计，组件用于用户站与独立管理台。基础控件以 KunUI 为参考，页面结构按 nextmoe 源码对照，交互使用 Reka，配色贴近用户提供的看板娘。页面仍待用户验收，不以源码复核代替视觉确认。共享库不依赖账号 API、Nuxt 路由或数据库，复用归属统一见 [前端规范](../../docs/frontend.md#可复用界面的归属)。

## 预览与验证

在仓库根目录运行：

```powershell
pnpm storybook
```

打开 [组件工作台](http://localhost:6006/?path=/story/overview-components--default)。左侧可进入单个组件，顶部工具栏切换 light/dark，Controls 面板调整故事参数。修改组件后会热更新，无需启动 Go、Docker 或远程依赖。

本轮新增 [导航组件工作台](http://localhost:6006/?path=/story/overview-navigation--default) 和 [常用组件工作台](http://localhost:6006/?path=/story/overview-essentials--default)。三组展示分别用于基础控件、导航及容器/反馈的评审，并非业务页面定稿。

用户提供看板娘后，新增 [看板娘与品牌配色](http://localhost:6006/?path=/story/overview-brand--default)，可将原图、参考色和组件组合放在一起比较明暗主题。

本轮配色更新已通过 UI 类型检查、Storybook 构建及原有 22 项浏览器交互检查；品牌故事另外检查了明暗桌面、375px 窄屏、图片加载和页面脚本错误。实测当前启用的 solid 按钮文字对比度最低为浅色 5.20:1、暗色 7.39:1；这只覆盖该组文字与底色，不表示整套组件已完成 WCAG 验收。

独立组件检查：

```powershell
pnpm --filter @moetopia/ui typecheck
pnpm storybook:build
pnpm test:ui
```

`test:ui` 使用已构建的 Storybook 和 Playwright Chromium，在 56006 端口启动专属静态服务器，完成后自动退出。不启动业务应用。需要先安装项目依赖和 Playwright Chromium；尚未安装浏览器时运行 `pnpm exec playwright install chromium`。组件更新后应重新构建 Storybook 再运行测试。

## 统一参数

| 参数 | 值 | 约束 |
| --- | --- | --- |
| color | primary、secondary、success、warning、danger、info、default | 按钮、徽标和选择控件使用同一语义色；反馈不能只靠颜色表达 |
| size | sm、md、lg | 常规控件高度分别为 36、44、48px；默认 md；sm 用于桌面密集区域 |
| variant | solid、bordered、flat、light | Button 支持四种；Badge 支持前三种 |
| theme | light、dark | 由根元素 `data-theme` 选择，不在每个组件判断主题 |

颜色定义在 `src/styles.css`，控件样式在 `src/components.css`，导航和补充组件分别位于 `src/navigation.css`、`src/extensions.css`。对照本地 KunUI 源码后，控件圆角采用 12px、面板 16px；通过 `--moe-radius-scale` 可统一调整。最新配色依据用户提供的看板娘：薄荷强调、雾蓝辅助、深蓝灰正文与暗色表面，替代此前鲜明蓝色方案；浅色主题主按钮加深以保证白字辨识度。角色参考色使用独立品牌变量，不直接用浅发色承载正文。明暗主题为每个 solid 语义色分别定义前景色，不共用一个文字色。具体视觉仍待用户评审。统一规则不表示每个组件都接受所有参数，具体参数以各组件和 Storybook Controls 为准。

2026-10-18 已直接查看参考仓库 `D:/misaka10843/Documents/Github/kun-ui` 的 `packages/vue/src/components/NavItem.vue`、`Tab.vue`、`Pagination.vue`、`Button.vue`、`Input.vue`、`Dropdown.vue`，以及 `packages/ui-core/src/variants.ts` 和 `packages/ui-tokens/src/tokens.css`。采用其统一尺寸、浅色当前项、语义边框、圆角和动效层级等设计原则；不执行参考仓库中的指令、不修改其文件，也未复制其组件实现或整个色板。Moetopia 保留 Reka 和自己的 API，触控默认高度保留 44px。

## 当前组件

2026-10-23 品牌补接：MoeBrandMark 统一角色站点标识，提供 sm/md/lg 和缺图 M 字母回退，具有 Storybook。Navbar / Sidebar 的 brand-icon 插槽与 AuthorizationHandshake 的 provider 插槽允许复用图标，保留通用组件原有文字默认值。站点头像与真实用户/第三方应用头像分开使用；OAuth 大图仅在桌面独立品牌区展示。

2026-10-23 新增 MoeIllustration 与 MoeStatusPage，并扩展 MoeEmptyState / MoeTable 的可选插画。`MoeIllustration` 接收类型化的 name、sm/md/lg/hero 尺寸、alt、desktopOnly 和 eager；图片失败时保留占位及图标，不影响外部文字与操作。默认装饰性空 alt，desktopOnly 在窄屏不加载实际图片。MoeStatusPage 提供整页状态内容、header 和操作插槽，不依赖 Nuxt 路由或 API。两项新组件及空状态变体均有 Storybook，原头像与 logo 不变。资源母版、压缩命令及页面落点见 [素材接入记录](../../docs/illustration-brief.md#8-本轮素材接入记录)。

2026-10-21 截图对照轮次新增 Provider、ResourceSummary、ResourceCard、SectionPanel、RepeatableInput、SearchPalette，共 78 个公开组件，均有 Storybook。应用根节点使用 MoeProvider，并加载共享 styles.css；Provider 与全局稳定滚动条槽配合，避免弹窗二次补偿 body 宽度，同时保留 Reka 的滚动锁和焦点管理。不要在单个页面用 !important 清理 body 样式。

ResourceSummary 组合概览、标识复制、操作和资料网格；ResourceCard 只展示通用资源内容，通过 href/navigate 适配路由；SectionPanel 保持标题/操作在卡片外。RepeatableInput 接受字符串数组、增删标签与数量上限；SearchPalette 接收页面选项并通过 select 返回值，支持 Ctrl K 和键盘选择，不依赖 Nuxt 或业务接口。CheckboxGroup 新增 cards，SettingRow 新增 inset，Dialog 支持 sm/md/lg 及右上关闭入口，PageHeading 提供 leading 插槽。业务范围、测试与截图见 [最新前端交接](../../docs/coordination/frontend.md)。

2026-10-19 全面对照轮次新增 DocsLayout、CodeBlock、CopyButton、FeatureGrid、DangerZone、ThemePicker、StatGrid，公开组件共 72 个，每项有故事。补足文档侧栏、代码复制反馈、首页结构、危险区、三选主题与未知统计展示；AuthShell 增加 mobile-brand 插槽，Link 的 appearance 提供主次链接按钮，PageHeading 可选择 h1/h2/h3，Dialog 可关闭默认底部关闭操作以组合真实表单操作栏。

本轮应用/Storybook 构建、类型、55 项页面和 31 项组件检查通过；21 张响应式截图及两个真实集成场景的范围见 [前端交接](../../docs/coordination/frontend.md)。界面、未完成后端能力和参考差异统一见 [完整对照](../../docs/nextmoe-parity.md)，不把未连接的表单/统计说成产品交付。

本轮按用户重新提出的 1:1 要求新增 ConsoleLayout、AccountMenu、AuthorizationHandshake、ConsentDetails，公开组件共 65 个。四个组件各有 Storybook，并提供 [完整授权页预览](http://localhost:6006/?path=/story/pages-authorization--consent)；预览不执行真实授权。Navbar 可选择 tablet（768px）/desktop（1024px）抽屉断点，Sidebar 的 rail 变体把折叠控制放到底部。尺寸、未完成业务及验收边界见 [布局核对](../../docs/ui-layout-audit.md)。

Card 的 layout=form 使用内嵌标题和 24px 内边距；默认布局不变。默认内容可通过 padding=none/sm/md/lg 选择 0/12/20/24px，避免页面覆盖内部工具类。本轮构建、49 项页面、29 项组件检查和 12 张截图复核通过；真实 RP 检查受已有 54310 端口占用限制，未执行。自有站点 OAuth 接入仍需 Go RP 契约，不能将静态授权故事称为已接通。

2026-10-19 继续复核 nextmoe 布局，新增 LanguagePicker、NavigationProgress、ProfileSummary、LandingLayout，共 61 个公开组件。布局差异及保留范围见 [复核表](../../docs/ui-layout-audit.md)。

2026-10-18 本轮将账号与开发者合并为用户站，布局参照 nextmoe 的场景划分；新增 AuthShell 和 ProfileLayout 后共有 57 个公开组件。新增组件具有 Storybook，复用边界见 [ADR-0017](../../docs/decisions/0017-user-site-layouts.md)。

| 组件 | 行为及组合 |
| --- | --- |
| MoeButton | 原生按钮；默认 type=button；加载时禁用并保留文字占位，防止宽度跳动。iconOnly 必须由调用方提供 aria-label |
| MoeInput | 字符串 v-model；必填 label；关联 description/error；trailing 插槽接收 size |
| MoeTextarea | 字符串 v-model；标签和错误关联；保留原生输入属性和纵向缩放 |
| MoeCheckbox | boolean 或 indeterminate v-model；文字可点击，支持 name/required/disabled |
| MoeSwitch | boolean v-model；具名开关；不自动发送网络请求 |
| MoeRadioGroup | 字符串 v-model；options；方向键选择，跳过禁用项 |
| MoeSelect | 字符串 v-model；单选 options；键盘选择、Escape 关闭、焦点返回；不支持多选或远程搜索 |
| MoeTabs | 字符串 v-model；items；以 value 命名内容插槽；默认方向键自动激活；segmented/underline 两种 variant，fullWidth 可均分可用空间 |
| MoeBadge | 小型状态文字；不充当按钮 |
| MoeAlert | title、正文、actions；静态默认不播报，announce 开启 role=alert |
| MoeCard | header、正文、footer；默认根元素不交互 |
| MoeDialog | v-model:open；trigger、正文、footer；footer 接收 close；焦点由 Reka 管理 |
| MoeTooltip | text、side；触发器须为可聚焦元素；必要说明不能仅放在 Tooltip |
| MoeSpinner | 必填 label；role=status；页面已有状态播报时避免重复放置 |
| MoeSkeleton | line/avatar/block；装饰性占位；实际加载语义由容器提供 |
| MoeIcon | 现有本地线性 SVG；装饰图标默认隐藏于可访问性树 |
| MoeNavItem | 原生链接；active 对应 aria-current=page；禁用项不提供 href，不进入链接导航；compact 保留可访问名称 |
| MoeNavbar | brand/items/active；brand/actions/mobile-footer 插槽；窄屏显示模态抽屉导航；open 受控；navigate 事件传递原始事件与条目 |
| MoeSidebar | groups/active；v-model:collapsed；分组、计数、收起状态；header/footer 插槽 |
| MoeBreadcrumbs | items；最后一项为当前位置；前置 href 项为链接；长路径自然换行 |
| MoeDropdown | 操作菜单；items；图标、说明、快捷键展示、分隔线、危险及禁用项；select 事件；open 受控 |
| MoeAvatar | name/src；sm/md/lg；circle/square；图片失败时显示名字缩写；当前不提供在线状态或自动抓取图片 |
| MoePagination | total 为总条目数；pageSize 默认 10；v-model:page；滑动选中底板、上一页/下一页、跳页；禁用态与边界保护 |
| MoeLink | 原生链接或 asChild 路由链接；external 添加安全 rel 和新窗口提示；asChild 时提示由调用方提供 |
| MoeDivider | horizontal/vertical；默认 decorative；非装饰性分隔需设置 decorative=false |
| MoeKbd | 展示按键名称，不自动注册快捷键 |
| MoeEmptyState | title/description/icon；动作默认插槽；不伪造数据 |
| MoeProgress | label/value/max；value=null 为不确定进度；showValue 显示百分比 |
| MoeAccordion | 单项展开、可全部收起；字符串 v-model；items；每个 value 对应内容插槽；禁用和方向键导航 |
| MoePopover | trigger/default；open 受控；label 为内容标题，弹层可访问名称由 Reka 关联触发按钮；可交互内容用 Popover，纯提示用 Tooltip |
| MoeToastProvider | 包裹通知使用范围；默认 5 秒；同一应用只放一个 Provider/Viewport；F8 聚焦通知区 |
| MoeToast | title/description/color；v-model:open；依赖 ToastProvider；暂停、关闭与右滑由 Reka 管理 |
| MoeDrawer | 基于 Dialog 的左右抽屉；title/description；open 受控；trigger/default/footer；关闭后归还焦点 |
| MoePasswordInput | 复用 Input；字符串 v-model；显隐按钮；原生属性传递到 input；不判断业务密码强度 |
| MoePinInput | 数字数组 v-model，未填位可为 undefined；默认 6 位；支持粘贴、自动前进、回退、mask；complete 只通知输入完成 |
| MoeSlider | 数字数组 v-model；支持单值/范围；min/max/step；键盘和触摸；数值说明由 label 提供 |
| MoeTable | 泛型 rows/columns/rowKey；原生表格；列插槽、排序事件、aria-sort、加载、空状态；排序和分页数据由调用方维护 |
| MoeSteps | label/items/current；只展示进度，不把步骤伪装成导航；完成项与当前步骤有文字及结构语义 |
| MoeButtonGroup | label；组合按钮；使用正常 Tab 导航，不暗示工具栏方向键模式 |
| MoeTag | label/color；可移除；remove 事件由调用方更新列表 |
| MoeCombobox | 字符串 v-model；options；本地搜索过滤、键盘选择、空结果、禁用与错误；不内置远程请求或创建任意值 |
| MoeNumberInput | number/undefined v-model；Reka NumberField；min/max/step、键盘与增减按钮；默认关闭滚轮改值 |
| MoeFileInput | File[] v-model；原生选择、accept、multiple、禁用、清除；选择文件不等于上传，accept 不替代服务端校验 |
| MoeDateInput | YYYY-MM-DD 字符串 v-model；原生日期输入；min/max；日期选择面板由浏览器提供，不宣称已实现自绘 DatePicker |
| MoeAvatarGroup | label/items/max/size；名字缩写兜底；超出人数有可访问名称；不自动加载成员列表 |
| MoeScrollArea | label/height；垂直与水平滚动条；可聚焦的滚动区域；内容仍使用原生滚动 |
| MoeUserChip | name/description/src；头像与用户说明组合；默认不交互，动作通过插槽提供 |
| MoeCheckboxGroup | 字符串数组 v-model；options；fieldset/legend；独立勾选、单项与整组禁用 |
| MoePageFrame | 公共页框；skipLabel；header/default/footer 插槽；主内容与键盘跳过链接 |
| MoeAuthLayout | 认证布局；illustration/title/caption/description；内容插槽；窄屏隐藏插画，表单自然滚动 |
| MoeAuthShell | 独立认证页壳；header/default/footer/brand 插槽、跳过链接；桌面表单列独立滚动，手机隐藏品牌区；不自动加载图片 |
| MoeProfileLayout | 摘要/内容布局；summary/default 插槽；桌面双栏且摘要吸顶，手机上下排列；不绑定账号或业务 API |
| MoeLanguagePicker | 原生语言名菜单；字符串 v-model、options/label/disabled；当前项勾选、键盘选择、关闭后返回焦点；不读写 Cookie |
| MoeNavigationProgress | active/value/label/error；固定顶部加载条，受外部生命周期控制；value 只作视觉估算，不播报真实百分比 |
| MoeProfileSummary | name/email/src/description；居中头像与身份摘要；无头像时复用名字缩写，不伪造账号角色 |
| MoeLandingLayout | title/description、actions/default 插槽；全宽介绍区域与独立限宽内容分区；不绑定页面路由 |
| MoeWorkspaceLayout | 工作区；sidebar/breadcrumbs/default 插槽；宽屏侧栏、窄屏单列；菜单入口由 Navbar 提供 |
| MoePageHeading | 页面主标题、说明、eyebrow 与 actions；单页主内容只放一个 h1 |
| MoeSettingRow | title/description/icon；内容及 actions 插槽；在多个页面复用设置项或会话操作布局 |
| MoeDescriptionList | key/label/value 列表与按 key 命名插槽；使用 dl/dt/dd；不绑定业务 DTO |
| MoeStatusIndicator | label/state/announce；状态点与可读标签；按需开启状态播报 |

`MoeOption` 为 `{ value, label, description?, disabled? }`。RadioGroup 显示 description；当前 Select/Tabs 不显示该字段为选项副说明，不应依赖它承载必须读取的内容。

旧 Button 调用继续兼容：variant 的 primary/secondary/quiet 分别映射为 solid/bordered/light；size 的 default/icon 分别映射为 md/md 图标按钮。新代码使用统一参数。此 API 并非 KunUI 的兼容实现。

共享布局样式集中在 `src/layouts.css`。Navbar 支持 subtitle 和独立 mobileItems，用同一组件组合应用顶栏与窄屏工作区入口。Tabs 支持默认内容插槽以复用登录/注册表单结构；命名插槽仍优先。Card 的 headingLevel 默认为 h2，嵌套场景可选择 h3/h4。`@moetopia/ui/mascot.png` 仅供明确的品牌参考故事使用；按用户最新要求，实际应用和默认 AuthLayout 故事不加载这张正面立绘。配色保留，可选插画接口待合适素材接入。

## 导航与数据边界

`MoeNavEntry` 为公共导航条目类型，来自内部 `MoeNavItem` 类型，与同名组件区分。导航使用稳定 id 匹配 active，href 由应用提供；不根据部分 URL 自动推断权限或当前路由。Navbar/Sidebar 的 navigate 事件不自动阻止默认跳转，Storybook 为演示而调用 preventDefault。应用接入时可处理事件并调用实际路由，也可让真实链接正常导航；需保留 Ctrl/Cmd/Shift 点击等浏览器行为。

Navbar 在 1024px 以下切换抽屉，选择条目、Escape、遮罩点击均可关闭；回到桌面宽度时自动关闭旧抽屉。actions 插槽应保持紧凑，复杂搜索表单应在宽屏或独立弹层中组织。Sidebar 收起状态建议每项提供图标；没有图标时文字缩略保留。

Pagination 的 page 为从 1 开始的页码。调用方必须提供非负 total、正整数 pageSize，并在查询条件变化导致页码失效时同步重置 page。本轮仅提供按钮分页，不伪称已经支持可爬的分页链接。Table 不内置服务器请求、虚拟滚动、行选择和列拖拽；sort 事件与排序方向必须由调用方一起维护，故事提供真实的本地排序示例。

Toast 不能承载必须及时确认的安全操作或成为表单错误的唯一提示。头像 name 供读屏器识别，不传真实用户数据到 Storybook。PinInput 不校验验证码正确性，也不连接发送验证码接口。

## 交互动效

页面/布局转场与导航加载条样式在 `src/experience.css`，由共享 Nuxt 适配绑定页面生命周期。page 使用 160ms 淡入/位移，layout 使用 140ms 淡入淡出；减少动态效果时移除位移。PageFrame 支持全高 sidebar 槽；Sidebar 新增 title/footerText 默认展示，折叠标签由应用传入当前语言。


动效定义在 `src/motion.css`，统一使用 `styles.css` 的时长和缓动变量：快速反馈 140ms、状态切换 220ms、指示条及对话框进入 300ms。不新增动画依赖。

- Tabs 默认采用分段轨道与滑动选中底板，通过 Reka TabsIndicator 跟随标签位置及宽度；underline 使用同一指示条。内容轻量淡入，不同时保留两个可交互面板。新增下划线、均分宽度、长标签和手动激活故事。
- Button 按压轻微缩放；Input 焦点光晕；Checkbox/Radio 选中标记进入；Switch 滑块平滑移动。禁用控件不提供按压反馈。
- Select 箭头旋转、弹层缩放淡入淡出；Tooltip 同样使用轻量弹层过渡；Dialog 遮罩淡入淡出、面板轻微位移缩放，退出完成后卸载。弹层保留 Reka 的焦点及键盘管理，依据其 [动画机制](https://reka-ui.com/docs/guides/animation) 接入。
- Pagination 使用测量后的滑动选中底板；Sidebar 平滑收起；Drawer 左右滑入滑出；Accordion 按内容高度展开收起；Progress 平滑更新；Toast 淡入、可右滑关闭。
- `prefers-reduced-motion: reduce` 时取消上述位移、缩放和过渡，同时保留静态选中、错误和加载文字；不要求用户等待动画才能操作。

动效不用于反复装饰静态 Card、Badge 或 Alert。完整页面转场留到布局阶段讨论。

## 检查范围与剩余事项

当前公开 61 个组件。本轮共享库及两应用类型检查、应用和 Storybook 构建通过；29 项独立组件检查与 43 项模拟接口页面检查通过（4 个 worker）。真实 OIDC 回归另通过 1 项独立客户端浏览器场景，详见前端协调记录。组件阶段的 123 个故事状态此前已通过运行时渲染检查；新增品牌和布局故事另行查看及验证。已查看桌面明暗主题、移动导航和 375px 窄屏截图。这些检查不代表 WCAG 全面达标，也不代表用户已经接受页面视觉。

Reka 2.11.0 的 RadioGroup 使用延迟焦点选中逻辑；测试瞬时按下并释放方向键时曾只移动焦点。当前测试覆盖按下、等待选中、抬起的完整过程；快速按键和真实辅助技术表现仍需后续核验，不宣称该上游时序问题已修复。

当前已覆盖身份中心与常规后台的主要基础控件。进一步扩展清单包括上传进度与取消、拖放文件、带时区的自绘日期选择器、远程搜索/多选、可爬分页、菜单子级和高级表格；这些尚未实现，不以现有静态示例代替功能。富文本、树形和图表不属于当前基础组件交付。当前已进入页面布局迭代，继续接受组件与页面反馈；合适的场景插画由用户另行提供。
