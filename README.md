# CCNote

CCNote is a Codex skill for turning academic concept, formula, diagram, and paper-screenshot explanation requests into detailed Markdown study notes with display-style LaTeX and a reusable note-archive workflow.

It is designed for study sessions where the user repeatedly asks questions such as:

- "Explain this part."
- "Explain this formula."
- "Explain this figure."
- "Turn this explanation into a Markdown note."
- "The formula rendering is broken; rewrite it with strict LaTeX."

The skill helps Codex respond consistently by creating or updating a Markdown note instead of only answering in chat.

## What It Does

CCNote teaches Codex to:

- create detailed academic concept notes from screenshots, formulas, paper excerpts, textbook sections, and diagrams;
- save each explanation as a Markdown file in the current project's established concept-notes folder;
- preserve the user's preferred note language while keeping the skill instructions themselves in English;
- use display-style LaTeX blocks for formulas instead of inline math;
- explain symbols, dimensions, derivations, intuition, examples, pitfalls, and summaries;
- update an existing note when the user asks for a clearer, more detailed, or better-formatted version.

## Repository Layout

```text
.
|-- README.md
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

The installable Codex skill package is the `ccnote/` directory.

Repository-level files such as `README.md`, `CHANGELOG.md`, and `scripts/` are intentionally kept outside the skill package so the installed skill stays clean.

## Installation

From the repository root, run:

```powershell
.\scripts\install-to-codex.ps1
```

By default this installs the skill to:

```text
C:\Users\10188\.codex\skills\ccnote
```

To install to another location:

```powershell
.\scripts\install-to-codex.ps1 -Destination "C:\path\to\skills\ccnote"
```

Restart or refresh Codex after installation if the skill does not appear immediately.

## Updating The Repository From The Installed Skill

If you edit the installed skill directly and want to bring those changes back into this repository, run:

```powershell
.\scripts\sync-from-installed.ps1
```

By default this reads from:

```text
C:\Users\10188\.codex\skills\ccnote
```

To sync from another installed location:

```powershell
.\scripts\sync-from-installed.ps1 -InstalledPath "C:\path\to\skills\ccnote"
```

After syncing, review the diff:

```powershell
git diff
```

Then commit the changes.

## Validation

Run the skill validator from the repository root:

```powershell
.\scripts\validate.ps1
```

The script runs Codex's `quick_validate.py` against the packaged skill directory:

```text
.\ccnote
```

It also enables UTF-8 mode for Python so the validator reads Markdown files consistently on Windows.

## Release Workflow

Use semantic versioning.

For a small patch:

```powershell
# edit ccnote/SKILL.md or ccnote/agents/openai.yaml
.\scripts\validate.ps1
git status
git add .
git commit -m "Update ccnote skill"
```

For a release:

```powershell
# update VERSION and CHANGELOG.md
.\scripts\validate.ps1
git add .
git commit -m "Release v0.1.1"
git tag v0.1.1
git push
git push origin v0.1.1
```

## Usage Examples

Ask Codex:

```text
Use $ccnote to explain this paper screenshot as a detailed Markdown note.
```

Or:

```text
Use $ccnote to revise the existing note and replace inline formulas with display-style LaTeX.
```

Or:

```text
Use $ccnote to explain this derivation step by step and save it into the concept-notes folder.
```

## Note Style

CCNote asks Codex to include:

- a short overview;
- notation and term mapping;
- dimensions and shapes;
- formula-by-formula explanation;
- step-by-step derivation;
- intuition;
- examples;
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

Inline math such as `$...$` should be avoided in generated notes unless the user explicitly asks for it.

## GitHub Repository Description

Recommended repository description:

```text
Codex skill for turning academic concept, formula, diagram, and paper-screenshot explanation requests into detailed Markdown study notes with display-style LaTeX and reusable note-archive workflow.
```

## License

MIT License. See `LICENSE`.

