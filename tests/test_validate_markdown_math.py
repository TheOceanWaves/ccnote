from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "ccnote"
    / "scripts"
    / "validate_markdown_math.py"
)
SPEC = importlib.util.spec_from_file_location("validate_markdown_math", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ValidateMarkdownMathTests(unittest.TestCase):
    def test_valid_visible_set_and_left_right_pass(self) -> None:
        text = r"""
$$
f_{\theta}
\left(
\mathbf r,\{Z_i,\mathbf R_i\}
\right)
$$
"""
        issues, blocks = VALIDATOR.validate_text(text)
        self.assertEqual(1, blocks)
        self.assertEqual([], issues)

    def test_mixed_visible_and_group_braces_fail(self) -> None:
        text = r"""
$$
f_{\theta}
\left(
\mathbf r,{Z_i,\mathbf R_i\}
\right)
$$
"""
        issues, _ = VALIDATOR.validate_text(text)
        messages = "\n".join(issue.message for issue in issues)
        self.assertIn("visible closing brace", messages)
        self.assertIn("unclosed TeX grouping brace", messages)

    def test_missing_command_backslash_fails(self) -> None:
        issues, _ = VALIDATOR.validate_text(
            r"""
$$
p(\rho\mid\mathbf R,mathcal B)
$$
"""
        )
        self.assertTrue(
            any("missing backslash" in issue.message and "mathcal" in issue.message for issue in issues)
        )

    def test_rightarrow_is_not_counted_as_right_delimiter(self) -> None:
        issues, _ = VALIDATOR.validate_text(
            r"""
$$
\left(\mathbf s_t\right)
\rightarrow
\left(\mathbf s_{t+1}\right)
$$
"""
        )
        self.assertEqual([], issues)

    def test_unclosed_display_block_fails(self) -> None:
        issues, blocks = VALIDATOR.validate_text(
            r"""
$$
\rho(\mathbf r)
"""
        )
        self.assertEqual(1, blocks)
        self.assertTrue(any("unclosed display math block" in issue.message for issue in issues))

    def test_unclosed_left_fails(self) -> None:
        issues, _ = VALIDATOR.validate_text(
            r"""
$$
f\left(\mathbf r
$$
"""
        )
        self.assertTrue(any("unclosed \\left" in issue.message for issue in issues))

    def test_utf8_bom_before_first_display_block_is_accepted(self) -> None:
        issues, blocks = VALIDATOR.validate_text("\ufeff$$\n\\rho(\\mathbf r)\n$$\n")
        self.assertEqual(1, blocks)
        self.assertEqual([], issues)

    def test_inline_math_fails_but_inline_code_is_ignored(self) -> None:
        issues, _ = VALIDATOR.validate_text("Bad $x$ math. Literal `$x$` example.\n")
        self.assertEqual(1, len(issues))
        self.assertIn("inline $ math", issues[0].message)

    def test_fenced_code_is_ignored(self) -> None:
        text = r"""
~~~markdown
$$
\mathbf r,{Z_i,\mathbf R_i\}
$$
~~~
"""
        issues, blocks = VALIDATOR.validate_text(text)
        self.assertEqual(0, blocks)
        self.assertEqual([], issues)

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            valid = root / "valid.md"
            invalid = root / "invalid.md"
            missing = root / "missing.md"
            valid.write_text("$$\n\\rho(\\mathbf r)\n$$\n", encoding="utf-8")
            invalid.write_text("Inline $x$.\n", encoding="utf-8")

            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.assertEqual(0, VALIDATOR.main([str(valid)]))
                self.assertEqual(1, VALIDATOR.main([str(invalid)]))
                self.assertEqual(2, VALIDATOR.main([str(missing)]))


if __name__ == "__main__":
    unittest.main()
