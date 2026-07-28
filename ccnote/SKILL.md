---
name: ccnote
description: Create detailed Markdown study notes for academic concepts from explanations, formulas, paper/book screenshots, diagrams, and derivations. Use when the user asks to explain a concept, formula, image, figure, paper excerpt, textbook section, or asks to generate, save, revise, or archive an explanation as a Markdown note.
---

# CCNote

Use this skill to turn academic explanation requests into reusable Markdown study notes with rigorous display-style LaTeX and enough detail for later self-study.

## Core Behavior

- Write the skill-guided explanation note in the user's preferred language; if the user has an established preference from the project, follow it. For this user's study workflow, default generated notes to Chinese unless the user asks otherwise.
- For concept, formula, image, figure, excerpt, or derivation explanations, create or update a Markdown file, not only a chat answer, unless the user explicitly asks for chat-only output.
- Save notes in the current workspace's established concept-notes folder:
  - Prefer an existing concept-notes folder, even if its name is localized.
  - If there is a project README or prior convention for explanation notes, follow that convention.
  - If no convention exists and the workspace is writable, create a clear concept-notes folder at the workspace root.
- Name files with a clear topic title in the note language.
- If a filename already exists, update it only when the user is asking to modify that same note; otherwise add a more specific title to avoid overwriting.
- At completion, report the created or updated file with a clickable absolute path and a brief core takeaway.

## Explanation Standard

Every note should be detailed enough for a learner who has the prerequisite basics but is meeting the specific topic for the first time.

Include, when relevant:

- A short opening summary of what the section is about.
- Term translation and notation mapping.
- Object definitions and dimensions or shapes.
- Formula-by-formula explanation.
- Step-by-step derivation with no large algebra jumps.
- Geometric or intuitive interpretation.
- A small concrete example when it reduces ambiguity.
- Common misunderstandings or caveats.
- A final one-paragraph or one-section summary.

For screenshots or source excerpts:

- Follow the source structure first.
- Explain the original symbols and formulas before adding broader context.
- Mark added context as explanatory supplement when it goes beyond the screenshot.
- If an image is low-resolution or partially cut off, explain what is visible and state any uncertainty.

## LaTeX and KaTeX Rules

Use strict display-style LaTeX for formulas.

- Avoid inline math like `$...$` in generated Markdown notes.
- Write important formulas as standalone display blocks:

```markdown
$$
\mathbf{A}\mathbf{v}_r
=
\sigma_r \mathbf{u}_r
$$
```

- When explaining a single symbol, still prefer a standalone display block:

```markdown
$$
\mathbf{u}_r
$$
```

- Never put mathematical notation or LaTeX commands inside Markdown inline-code
  backticks. A span such as `` `\phi_m` `` is rendered verbatim instead of as
  math. Move the notation to a standalone `$$ ... $$` block.
- Do not place display-math blocks inside Markdown table cells. If a comparison
  needs mathematical symbols, use plain Unicode symbols in the table when they
  are unambiguous, or move each symbol and its explanation below the table into
  standalone display blocks.
- Fenced code examples may contain literal LaTeX source when the source itself
  is what the note is teaching. Do not treat those code examples as rendered
  formulas.
- Keep prose punctuation outside formula blocks.
- Use notation from the source image or document unless correcting a clear typo.
- Write visible set braces as a matched pair with `\{` and `\}`. Use unescaped `{` and `}` only for TeX grouping and command arguments. Never mix an unescaped opening brace with an escaped closing brace, or the reverse.
- Pair every exact `\left` command with an exact `\right` command in the same formula block.
- Include the leading backslash on LaTeX commands such as `\mathcal`, `\mathbf`, `\mathrm`, `\mathbb`, `\boldsymbol`, `\operatorname`, and `\text`.
- After editing, run the bundled structural validator and fix every reported issue. Do not treat visual inspection as sufficient.

For example, this is invalid because the visible set uses mismatched brace forms:

```markdown
$$
f_{\theta}
\left(
\mathbf r,{Z_i,\mathbf R_i\}
\right)
$$
```

Write it as:

```markdown
$$
f_{\theta}
\left(
\mathbf r,\{Z_i,\mathbf R_i\}
\right)
$$
```

The bundled validator checks structural Markdown and TeX hazards; it is not a complete KaTeX semantic parser.

## Recommended Note Structure

Use this structure by default, adapting headings to the topic and the user's language:

```markdown
# Topic Title

This note explains ...

---

## 1. What This Section Is About

## 2. Core Formula or Definition

## 3. Symbols and Dimensions

## 4. Step-by-Step Derivation or Term-by-Term Explanation

## 5. Intuition

## 6. Simple Example

## 7. Common Pitfalls

## 8. One-Sentence Summary
```

For algorithm sections, include:

- Objective function.
- Inputs and outputs.
- Pseudocode line-by-line meaning.
- Why each update formula is valid.
- Computational or numerical caveats.

For comparison sections, include:

- A compact table only if it clarifies differences.
- Then explain each row in prose.

## File Workflow

1. Inspect the workspace for the established concept-notes folder and any README convention before writing.
2. Choose a descriptive topic filename in the note language.
3. Read an existing same-topic file before modifying it.
4. Write or patch the Markdown note.
5. Verify:
   - The file exists in the target folder.
   - Important formulas use `$$ ... $$` display blocks.
   - No ordinary inline `$...$` formulas remain unless the user explicitly requested inline math.
   - No mathematical notation or LaTeX command is wrapped in Markdown inline-code backticks.
   - No display-math block is embedded in a Markdown table cell.
   - Visible set braces, TeX grouping braces, and exact `\left` / `\right` commands are balanced.
   - The note is detailed enough: dimensions, formula meaning, intuition, and summary are present.
6. Run the validator from the skill directory, passing every Markdown note created or changed:

```text
python scripts/validate_markdown_math.py <note.md> [<note2.md> ...]
```

7. If validation fails, patch the reported formula blocks and rerun until the command exits successfully.
8. Reply briefly with the file path and the core takeaway.

## Handling Follow-Up Corrections

When the user says a previous note is too hard, too brief, or has formula rendering problems:

- Modify the existing note instead of creating a duplicate.
- Expand the exact confusing section with smaller steps and intermediate formulas.
- Replace inline math with display LaTeX blocks.
- Preserve useful prior content and only rewrite broadly when the structure is the problem.

## Default Depth

Use a high-detail teaching style. Assume the user wants at least the depth of:

- explaining what each symbol means;
- explaining why dimensions match;
- deriving matrix or tensor formulas step by step;
- connecting formulas to intuition;
- clarifying how the concept is used in later decomposition, compression, modeling, or analysis work.

Do not compress the explanation into a short answer unless the user explicitly asks for a short answer.

