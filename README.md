# CCNote

[English](README.md) | [简体中文](README.zh-CN.md)

CCNote is a Codex skill for turning academic concept, formula, diagram, and paper-screenshot explanation requests into detailed Markdown study notes with display-style LaTeX.

It is built for study workflows where you repeatedly ask Codex to explain textbook pages, paper excerpts, formulas, tensor diagrams, derivations, or screenshots, and you want those explanations saved as reusable notes instead of disappearing in chat history.

## Who It Is For

CCNote is useful if you:

- read academic papers, textbooks, lecture slides, or screenshots with dense notation;
- want explanations saved as Markdown notes automatically;
- prefer formulas written as display-style LaTeX blocks;
- want explanations that include notation, dimensions, derivations, intuition, examples, pitfalls, and summaries;
- maintain a project folder of concept notes while studying a technical topic.

## Features

- Creates or updates Markdown notes for concept, formula, figure, and derivation explanations.
- Uses the current project's established concept-notes folder when one exists.
- Avoids inline math in generated notes and prefers display-style LaTeX blocks.
- Explains formulas step by step instead of skipping algebra or dimensional reasoning.
- Follows source screenshots or excerpts first, then adds helpful context when needed.
- Supports follow-up revisions such as "make this more detailed" or "fix formula rendering."
- Runs a bundled, dependency-free structural validator after note edits to catch common KaTeX hazards such as mismatched visible braces, unbalanced `\left` / `\right`, and missing command backslashes.

## Installation

Clone this repository:

```powershell
git clone https://github.com/TheOceanWaves/ccnote.git
cd ccnote
```

Install the skill into your local Codex skills directory:

```powershell
.\scripts\install-to-codex.ps1
```

By default, the script installs CCNote to:

```text
C:\Users\10188\.codex\skills\ccnote
```

To install to another location:

```powershell
.\scripts\install-to-codex.ps1 -Destination "C:\path\to\skills\ccnote"
```

Restart or refresh Codex after installation if the skill does not appear immediately.

## How To Use

Invoke the skill explicitly:

```text
Use $ccnote to explain this paper screenshot as a detailed Markdown note.
```

Other example prompts:

```text
Use $ccnote to explain this formula step by step and save it as a concept note.
```

```text
Use $ccnote to revise the existing note and replace inline formulas with display-style LaTeX.
```

```text
Use $ccnote to explain this derivation in detail, including dimensions and intuition.
```

## Note Style

CCNote asks Codex to include:

- a short overview;
- term and notation mapping;
- object definitions, dimensions, and shapes;
- formula-by-formula explanation;
- step-by-step derivation;
- intuition or geometric meaning;
- a small example when useful;
- common pitfalls;
- a concise summary.

Important formulas should be written as display blocks:

```markdown
$$
\mathbf{A}\mathbf{v}_r
=
\sigma_r \mathbf{u}_r
$$
```

Inline math such as `$...$` should be avoided in generated notes unless explicitly requested.

After creating or revising a note, CCNote runs its bundled validator until the file passes:

```powershell
python "$HOME\.codex\skills\ccnote\scripts\validate_markdown_math.py" "C:\path\to\note.md"
```

The validator is a lightweight structural check rather than a complete KaTeX parser. It reports the file, source line, and math block for common syntax hazards.

## Repository Layout

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
|-- tests/
|   `-- test_validate_markdown_math.py
`-- ccnote/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    `-- scripts/
        `-- validate_markdown_math.py
```

The installable Codex skill package is the `ccnote/` directory.

## Optional Validation

If you want to check that the packaged skill is structurally valid, run:

```powershell
.\scripts\validate.ps1
```

This runs Codex's skill validator against the `ccnote/` package.

To validate one or more Markdown notes directly:

```powershell
python .\ccnote\scripts\validate_markdown_math.py "C:\path\to\note.md"
```

## License

MIT License. See [LICENSE](LICENSE).

