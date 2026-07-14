#!/usr/bin/env python3
"""Check Markdown notes for common structural KaTeX hazards.

This validator intentionally uses only the Python standard library. It catches
repeatable structural mistakes but is not a complete TeX or KaTeX parser.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LEFT_RE = re.compile(r"\\left(?![A-Za-z])")
RIGHT_RE = re.compile(r"\\right(?![A-Za-z])")
BARE_COMMAND_RE = re.compile(
    r"(?<!\\)\b"
    r"(mathcal|mathbf|mathrm|mathbb|boldsymbol|operatorname|text|frac|sqrt)"
    r"\b"
)


@dataclass(frozen=True)
class Issue:
    line: int
    message: str
    block: int | None = None


def _preceding_backslashes(text: str, index: int) -> int:
    count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        count += 1
        cursor -= 1
    return count


def _is_escaped(text: str, index: int) -> bool:
    return _preceding_backslashes(text, index) % 2 == 1


def _strip_inline_code(line: str) -> str:
    """Replace matched Markdown inline-code spans with spaces."""

    chars = list(line)
    cursor = 0
    while cursor < len(line):
        if line[cursor] != "`":
            cursor += 1
            continue

        end_of_run = cursor
        while end_of_run < len(line) and line[end_of_run] == "`":
            end_of_run += 1
        marker = line[cursor:end_of_run]
        close = line.find(marker, end_of_run)
        if close == -1:
            cursor = end_of_run
            continue

        close_end = close + len(marker)
        chars[cursor:close_end] = [" "] * (close_end - cursor)
        cursor = close_end

    return "".join(chars)


def _unescaped_dollar_positions(line: str) -> list[int]:
    return [
        index
        for index, char in enumerate(line)
        if char == "$" and not _is_escaped(line, index)
    ]


def _validate_formula_block(
    lines: list[tuple[int, str]], block_number: int
) -> list[Issue]:
    issues: list[Issue] = []
    group_stack: list[int] = []
    visible_brace_stack: list[int] = []
    left_stack: list[int] = []

    for line_number, line in lines:
        for index, char in enumerate(line):
            escaped = _is_escaped(line, index)
            if char == "{" and escaped:
                visible_brace_stack.append(line_number)
            elif char == "}" and escaped:
                if visible_brace_stack:
                    visible_brace_stack.pop()
                else:
                    issues.append(
                        Issue(
                            line_number,
                            "visible closing brace \\} has no matching \\{",
                            block_number,
                        )
                    )
            elif char == "{" and not escaped:
                group_stack.append(line_number)
            elif char == "}" and not escaped:
                if group_stack:
                    group_stack.pop()
                else:
                    issues.append(
                        Issue(
                            line_number,
                            "TeX group closing brace } has no matching {",
                            block_number,
                        )
                    )

        commands: list[tuple[int, str]] = []
        commands.extend((match.start(), "left") for match in LEFT_RE.finditer(line))
        commands.extend((match.start(), "right") for match in RIGHT_RE.finditer(line))
        for _, command in sorted(commands):
            if command == "left":
                left_stack.append(line_number)
            elif left_stack:
                left_stack.pop()
            else:
                issues.append(
                    Issue(
                        line_number,
                        "\\right has no preceding matching \\left",
                        block_number,
                    )
                )

        for match in BARE_COMMAND_RE.finditer(line):
            issues.append(
                Issue(
                    line_number,
                    f"possible missing backslash before LaTeX command '{match.group(1)}'",
                    block_number,
                )
            )

    for line_number in group_stack:
        issues.append(
            Issue(
                line_number,
                "unclosed TeX grouping brace {; do not pair raw { with visible \\}",
                block_number,
            )
        )
    for line_number in visible_brace_stack:
        issues.append(
            Issue(
                line_number,
                "unclosed visible set brace \\{; close it with \\}",
                block_number,
            )
        )
    for line_number in left_stack:
        issues.append(
            Issue(
                line_number,
                "unclosed \\left command; add the matching \\right",
                block_number,
            )
        )

    return issues


def validate_text(text: str) -> tuple[list[Issue], int]:
    if text.startswith("\ufeff"):
        text = text[1:]

    issues: list[Issue] = []
    in_fence = False
    fence_char = ""
    fence_length = 0
    in_display = False
    display_start = 0
    block_number = 0
    block_lines: list[tuple[int, str]] = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_RE.match(raw_line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
                continue

        if in_fence:
            continue

        line = _strip_inline_code(raw_line)
        stripped = line.strip()

        if stripped == "$$":
            if not in_display:
                in_display = True
                display_start = line_number
                block_number += 1
                block_lines = []
            else:
                issues.extend(_validate_formula_block(block_lines, block_number))
                in_display = False
                display_start = 0
                block_lines = []
            continue

        if "$$" in line:
            issues.append(
                Issue(
                    line_number,
                    "display delimiter $$ must appear alone on its own line",
                    block_number if in_display else None,
                )
            )
            if in_display:
                block_lines.append((line_number, line))
            continue

        if in_display:
            block_lines.append((line_number, line))
            continue

        if _unescaped_dollar_positions(line):
            issues.append(
                Issue(
                    line_number,
                    "ordinary inline $ math is not allowed; use a standalone $$ block",
                )
            )

    if in_display:
        issues.append(
            Issue(display_start, "unclosed display math block; add a closing $$", block_number)
        )
        issues.extend(_validate_formula_block(block_lines, block_number))

    return issues, block_number


def validate_file(path: Path) -> tuple[list[Issue], int]:
    text = path.read_text(encoding="utf-8-sig")
    return validate_text(text)


def _format_issue(path: Path, issue: Issue) -> str:
    block = f" [math block {issue.block}]" if issue.block is not None else ""
    return f"{path}:{issue.line}:{block} {issue.message}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check Markdown notes for common structural KaTeX hazards. "
            "This is not a complete KaTeX parser."
        )
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files to validate")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    had_validation_errors = False

    for path in args.paths:
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2
        if not path.is_file():
            print(f"ERROR: expected a Markdown file: {path}", file=sys.stderr)
            return 2

        try:
            issues, block_count = validate_file(path)
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
            return 2

        if issues:
            had_validation_errors = True
            for issue in issues:
                print(_format_issue(path, issue), file=sys.stderr)
        else:
            print(f"OK: {path} ({block_count} display math blocks)")

    return 1 if had_validation_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
