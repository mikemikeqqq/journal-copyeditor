# Copyeditor Skill

[English README](README.en.md) | 中文说明

`copyeditor-skill` 是一个面向学术英文 `.docx` 手稿的 Codex skill，用于帮助作者完成接近专业 copy editor 工作流的语言编辑、修订模式修改、批注、引用/数字审查、格式保真检查和交付前验证。

这个仓库现在是一个**单技能包**：完整仓库本身就是可安装的 skill 目录。请复制或克隆整个目录，而不是只复制 `SKILL.md`，因为该技能依赖 `references/` 中的规则文件和 `scripts/` 中的审查脚本。

## 为什么做这个

很多非英语母语学者在投稿前会遇到三个实际问题：

1. 语法问题并不总是最难的，真正耗时的是发现隐藏在长句、术语不一致、过度声称、引用顺序、数字格式和表格说明里的细节错误。
2. 学术 copy editing 不只是把句子改得更像英语，还要保护作者原意、研究设计边界、统计含义、引用字段、图表编号和 Word 格式。
3. 许多作者需要付费寻找 copy editor，但预算、时间、返修轮次和专业领域匹配都可能成为负担。

`copyeditor-skill` 的目标不是取代作者判断，也不是承诺投稿结果，而是把一套可重复的投稿前 copy-editing 流程交给 Codex：它会尽量保留原始事实和格式，在 Word 修订模式中做局部修改，把无法安全决定的问题写成批注或报告，并用脚本检查常见交付风险。

## 适合谁

- 准备投稿或返修英文论文的非英语母语作者。
- 需要检查 `.docx` 手稿语言、格式、引用、数字和审稿风险的研究者。
- 希望用 Word Track Changes 交付修改痕迹的编辑、助研或导师。
- 想把 AI copy editing 变成可复查工作流，而不是一次性聊天润色的用户。

## 技能索引

| Skill | 状态 | 用途 | 触发词 |
|---|---|---|---|
| `copyeditor-skill` | Beta | 学术 `.docx` copy editing、Word 修订模式、批注、引用/数字审查、格式保真和交付验证 | “copy editing”, “proofread”, “line edit”, “论文润色”, “英文学术校对”, “修订模式”, “批注”, “投稿前语言编辑” |

## 核心能力

| 能力 | 说明 |
|---|---|
| Word 修订模式 | 优先使用 Microsoft Word 自动化，在 `.docx` 中保留可审阅的 tracked changes。 |
| 局部 copy editing | 尽量只修改需要改的词、短语、标点、从句或句子片段，避免整段删除再重写。 |
| Catherine 风格批注 | 默认用 `Catherine` / `C` 作为编辑身份，给作者决策点添加简洁、专业的英文批注。 |
| 学术语气控制 | 使用正式、清晰、审慎的 academic English，避免过度声称和未经证据支持的因果表达。 |
| 术语一致性 | 保持 constructs、变量名、方法名、模型名和关键概念一致，不为了变化而替换同义词。 |
| 引用与参考文献审查 | 检查作者-年份引用顺序、缺失引用、未被引用的参考文献、格式不一致和疑似元数据问题。 |
| 数字与统计审查 | 检查 p 值、置信区间、样本量、表图编号、显著性表达和统计语言。 |
| 格式保真 | 关注字体、字号、段落样式、表格、标题、图注、参考文献、上下标和特殊符号。 |
| Copy Editing Report | 在文末添加 `Copy Editing and Proofreading Report`，列出语言问题、引用/数字问题和审稿风险。 |
| 交付前验证 | 使用脚本检查 CJK/乱码、修订数量、批注作者、报告是否存在、Track Changes 是否开启等。 |

## Codex 推荐安装方式

最简单的方式是把仓库链接交给 Codex，并让它安装完整技能目录：

```text
https://github.com/mikemikeqqq/copyeditor-skill.git
```

推荐提示词：

```text
请从这个仓库安装 Codex skill：
https://github.com/mikemikeqqq/copyeditor-skill.git

请把完整仓库安装到我的 Codex skills 目录中，目标文件夹名使用 copyeditor-skill。
不要只复制 SKILL.md；请保留 agents/、references/ 和 scripts/。
```

安装后，请开启一个新的 Codex 会话，然后自然描述任务，例如：

```text
请使用 $copyeditor-skill 对这篇英文论文进行中等强度 copy editing，保留 Word 修订模式，添加 Catherine 风格批注，检查引用、数字和潜在审稿风险，并在文末加入 Copy Editing and Proofreading Report。
```

## 手动安装

### Windows PowerShell

```powershell
mkdir "$env:USERPROFILE\.codex\skills" -Force
git clone https://github.com/mikemikeqqq/copyeditor-skill.git "$env:USERPROFILE\.codex\skills\copyeditor-skill"
```

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mikemikeqqq/copyeditor-skill.git ~/.codex/skills/copyeditor-skill
```

安装后重启 Codex，让新 skill 被加载。

### 更新

```bash
cd ~/.codex/skills/copyeditor-skill
git pull
```

Windows PowerShell：

```powershell
cd "$env:USERPROFILE\.codex\skills\copyeditor-skill"
git pull
```

关键规则：**保留完整目录结构**。不要只复制 `SKILL.md`，因为许多规则、审查流程和脚本都在 `references/` 与 `scripts/` 中。

## 目录结构

```text
copyeditor-skill/
|-- README.md
|-- README.en.md
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- academic-critical-style.md
|   |-- chinese-influenced-english.md
|   |-- citations-and-report.md
|   |-- copyediting-contract.md
|   |-- deliverable-packaging.md
|   |-- format-preservation.md
|   |-- journal-styles.md
|   |-- minimal-diff-tracked-changes.md
|   |-- reviewer-risk-rubric.md
|   |-- statistics-and-numbers.md
|   |-- style-and-argument.md
|   |-- validation-checklist.md
|   `-- word-com-workflow.md
`-- scripts/
    |-- audit_citations.py
    |-- audit_formatting.py
    |-- audit_numbers.py
    |-- audit_revision_granularity.py
    |-- create_delivery_package.py
    |-- insert_copyediting_report.py
    `-- validate_docx.py
```

## 工作流概览

1. **任务 intake**：确认手稿路径、目标期刊或拼写风格、编辑强度、编辑者姓名和交付格式。
2. **源文件检查**：确认 Word 能打开，记录已有修订、批注、批注作者和 Track Changes 状态。
3. **基线审查**：运行验证脚本、引用审查和数字审查，记录源文件风险。
4. **创建输出副本**：不直接覆盖原稿。
5. **Word 修订模式编辑**：逐段 copy-edit，保留 citation fields、equations、tables、figures 和 local formatting。
6. **批注与报告**：只对作者需要决策的问题添加批注，并在文末加入 copy editing report。
7. **交付前 QA**：重新打开文件，检查修订数量、批注、报告、格式、CJK/乱码、整段替换和 PDF 导出。
8. **交付说明**：报告输出文件、验证摘要、残余风险和作者需要确认的问题。

## Helper Scripts

这些脚本是启发式 QA 工具，不能替代人工判断；它们用于发现高风险位置，让编辑过程可复查。

| 脚本 | 用途 |
|---|---|
| `scripts/validate_docx.py` | 检查 DOCX 是否包含 Track Changes、批注、报告、CJK/乱码、修订标记和潜在丢失内容。 |
| `scripts/audit_citations.py` | 检查 author-date citation、reference list、引用顺序和疑似缺失项。 |
| `scripts/audit_numbers.py` | 检查 p 值、CI、样本量、百分比、表图编号和数字表达。 |
| `scripts/audit_revision_granularity.py` | 检查是否出现整段删除再整段插入的不可审阅修订。 |
| `scripts/audit_formatting.py` | 检查 tracked insertions 与附近文本的显式格式是否可能不一致。 |
| `scripts/insert_copyediting_report.py` | 通过 Word 自动化插入 copy editing report。 |
| `scripts/create_delivery_package.py` | 生成 tracked、clean、PDF 和 audit outputs 的交付包。 |

常用命令：

```powershell
python scripts/validate_docx.py "edited.docx" --source "source.docx" --require-report --require-comment-author Catherine --fail-on-suspect
python scripts/audit_citations.py "manuscript.docx" --json-output "citation_audit.json" --summary-output "citation_audit.md"
python scripts/audit_numbers.py "manuscript.docx" --json-output "numbers_audit.json" --summary-output "numbers_audit.md"
python scripts/audit_revision_granularity.py "edited.docx" --summary-output "revision_granularity_audit.md" --json-output "revision_granularity_audit.json"
python scripts/audit_formatting.py "edited.docx" --summary-output "formatting_audit.md" --json-output "formatting_audit.json"
python scripts/create_delivery_package.py "edited.docx" --output-dir "output/doc" --clean-copy --pdf
```

## 设计原则

1. **事实优先**：不编造数据、方法、引用、机制、限制、p 值、样本量或图表信息。
2. **修订可审阅**：copy editing 应以局部 tracked changes 呈现，不把普通语言修改变成整段替换。
3. **格式保真**：改语言时保护字体、字号、段落、表格、图注、参考文献和上下标。
4. **证据边界清楚**：相关、回归、结构方程、meta-analysis 和 moderation 结果通常应写成 association，除非研究设计支持因果推断。
5. **批注有必要**：不为每个语法修改批注，只在含义不清、证据不足、术语冲突、统计/引用问题或作者决策点上批注。
6. **输出优先**：目标是可交付的 `.docx`、clean copy、PDF、审查报告和验证摘要，而不是泛泛建议。

## 非 Codex 场景

用于 Claude Code、ChatGPT 自定义工作流或其他 agent 时，建议保留一个稳定的仓库 clone，再创建轻量 subagent、slash command 或 custom prompt wrapper，指向真实的 `SKILL.md`，并保留 `references/` 与 `scripts/`。

手动或非 Codex 使用时：

1. 将完整技能目录复制到你的 prompt library 或项目中。
2. 保留 `SKILL.md`、`agents/`、`references/`、`scripts/` 和 README。
3. 如果目标 agent 有自己的 frontmatter 或工具格式要求，再调整 `SKILL.md` 的 metadata。

## 限制与注意事项

- 该技能不是法律、伦理、统计或投稿成功保证。
- 它不能替作者决定研究事实、数据解释、作者贡献、版权、伦理审批或目标期刊政策。
- Word tracked changes 的最终交付最适合在装有 Microsoft Word 的 Windows 环境中完成。
- 自动化脚本是启发式检查工具；发现问题后仍需要人工核验。
- 如果手稿含有大量公式、特殊符号、参考文献管理器字段或已有复杂修订，应更谨慎地做小范围编辑和多轮验证。

## 贡献指南

欢迎提交 issue 或 PR。比较有价值的贡献包括：

- 新增 journal style profile，例如 APA、Harvard、Nature、Elsevier、IEEE、Vancouver 的细化规则。
- 改进 citation/reference audit、numbers audit 或 formatting audit 的检测逻辑。
- 增加真实但脱敏的测试样例和失败案例。
- 补充中英文学术写作中常见的 translationese、construct drift 或 overclaiming 模式。
- 改进 README、安装说明或跨平台使用说明。

提交 PR 时请尽量说明：

1. 修改解决了什么 copy-editing 问题。
2. 是否影响现有工作流或脚本参数。
3. 如何验证修改，例如运行了哪个脚本或检查了哪个 `.docx` 场景。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=mikemikeqqq/copyeditor-skill&type=Date)](https://star-history.com/#mikemikeqqq/copyeditor-skill&Date)

## License

MIT License. See [LICENSE](LICENSE).
