# CCNote

[English](README.md) | [简体中文](README.zh-CN.md)

CCNote 是一个 Codex skill，用来把学术概念、公式、图示、论文截图、教材片段和推导过程解释成详细的 Markdown 学习笔记，并统一使用展示型 LaTeX 公式块。

它适合这样的学习场景：你不断把论文、教材、课件或截图发给 Codex，让它解释其中的概念和公式，同时希望这些解释被保存成可以长期复习的笔记，而不是只留在聊天记录里。

## 适合谁使用

如果你有下面这些需求，CCNote 会很适合：

- 阅读论文、教材、课件或包含密集符号的截图；
- 希望每次解释都自动整理成 Markdown 笔记；
- 希望公式使用独立 LaTeX 公式块，避免行内公式渲染乱码；
- 希望解释包含符号含义、维度、推导、直觉、例子、常见误区和总结；
- 正在围绕某个技术主题维护一组概念解释笔记。

## 功能特点

- 为概念、公式、图示和推导解释创建或更新 Markdown 笔记。
- 优先使用当前项目已有的概念笔记文件夹。
- 生成笔记时避免使用行内数学公式，默认使用展示型 LaTeX 公式块。
- 按步骤解释公式，不跳过关键代数步骤或维度说明。
- 优先按照截图或原文结构解释，再补充必要背景。
- 支持后续修改，例如“讲得更详细一点”或“把公式改成严格 LaTeX 格式”。

## 安装方法

克隆这个仓库：

```powershell
git clone https://github.com/TheOceanWaves/ccnote.git
cd ccnote
```

把 skill 安装到本地 Codex skills 目录：

```powershell
.\scripts\install-to-codex.ps1
```

默认会安装到：

```text
C:\Users\10188\.codex\skills\ccnote
```

如果你想安装到其他位置：

```powershell
.\scripts\install-to-codex.ps1 -Destination "C:\path\to\skills\ccnote"
```

安装后如果 Codex 没有立刻显示这个 skill，可以重启或刷新 Codex。

## 使用示例

显式调用这个 skill：

```text
Use $ccnote to explain this paper screenshot as a detailed Markdown note.
```

也可以这样问：

```text
Use $ccnote to explain this formula step by step and save it as a concept note.
```

```text
Use $ccnote to revise the existing note and replace inline formulas with display-style LaTeX.
```

```text
Use $ccnote to explain this derivation in detail, including dimensions and intuition.
```

## 笔记风格

CCNote 会引导 Codex 尽量包含：

- 简短概述；
- 术语和符号对应关系；
- 对象定义、维度和形状；
- 公式逐项解释；
- 分步骤推导；
- 直觉或几何意义；
- 必要的小例子；
- 常见误区；
- 简洁总结。

重要公式会写成独立展示块：

```markdown
$$
\mathbf{A}\mathbf{v}_r
=
\sigma_r \mathbf{u}_r
$$
```

除非你明确要求，否则生成笔记时会尽量避免使用 `$...$` 这种行内公式。

## 仓库结构

```text
.
|-- README.md
|-- README.zh-CN.md
|-- LICENSE
|-- CHANGELOG.md
|-- VERSION
|-- scripts/
|   |-- install-to-codex.ps1
|   |-- sync-from-installed.ps1
|   `-- validate.ps1
`-- ccnote/
    |-- SKILL.md
    `-- agents/
        `-- openai.yaml
```

真正可安装的 Codex skill 是 `ccnote/` 目录。

## 可选校验

如果你想检查这个 skill 包的结构是否有效，可以运行：

```powershell
.\scripts\validate.ps1
```

它会对 `ccnote/` 目录运行 Codex skill 校验器。

## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。

