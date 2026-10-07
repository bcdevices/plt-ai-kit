"""Tests for plt_lint.

Run with:
    python3 -m unittest discover -s tools/plt-lint/tests -v
"""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
# plt_lint.py and its catalog ship inside the skill so that every agent
# surface can load them; the tests and fixtures stay here.
TOOL_ROOT = HERE.parents[2] / "skills" / "plt-test-plan-builder" / "scripts"
FIXTURES = HERE / "fixtures"

sys.path.insert(0, str(TOOL_ROOT))
import plt_lint  # noqa: E402


CATALOG = plt_lint.load_catalog(TOOL_ROOT / "plt_command_catalog.json")


def lint(name: str, *, strict: bool = False) -> plt_lint.LintResult:
    doc = plt_lint._read_yaml(FIXTURES / name)
    return plt_lint.lint_plan(doc, name, CATALOG, strict=strict)


def error_messages(r: plt_lint.LintResult) -> list[str]:
    return [f.message for f in r.findings if f.severity == "error"]


class TokenizerTests(unittest.TestCase):
    def test_simple_split(self):
        self.assertEqual(
            plt_lint.split_command_line("canCfg CAN0 500000 fd"),
            ["canCfg", "CAN0", "500000", "fd"],
        )

    def test_quoted_token_kept_whole(self):
        self.assertEqual(
            plt_lint.split_command_line('operator "insert device"'),
            ["operator", "insert device"],
        )

    def test_multiple_spaces_collapse(self):
        self.assertEqual(
            plt_lint.split_command_line("wait   1s"),
            ["wait", "1s"],
        )


class CatalogTests(unittest.TestCase):
    def test_catalog_has_all_commands(self):
        names = {c["name"] for c in CATALOG["commands"]}
        # A sampling of commands we know should exist per parser.go.
        for expected in ["canCfg", "wait", "uart", "scpi", "ble", "usb", "power"]:
            self.assertIn(expected, names)

    def test_catalog_version_is_1(self):
        self.assertEqual(CATALOG["schema_version"], "1")


class ValidPlans(unittest.TestCase):
    def test_minimal_ok(self):
        r = lint("valid_minimal.yaml")
        self.assertEqual(error_messages(r), [])

    def test_ble_ok(self):
        r = lint("ble_ok.yaml")
        self.assertEqual(error_messages(r), [])

    def test_quoted_tokens_ok(self):
        r = lint("tokenization.yaml")
        self.assertEqual(error_messages(r), [], msg=r.findings)


class DetectsErrors(unittest.TestCase):
    def test_unknown_command(self):
        r = lint("unknown_command.yaml")
        errs = error_messages(r)
        self.assertTrue(any("unknown command 'doTheThing'" in m for m in errs), errs)

    def test_too_few_args(self):
        r = lint("too_few_args.yaml")
        errs = error_messages(r)
        self.assertTrue(any("requires at least 2 arg" in m for m in errs), errs)

    def test_bad_can_port(self):
        r = lint("bad_can_port.yaml")
        errs = error_messages(r)
        self.assertTrue(any("expected CANx port" in m for m in errs), errs)

    def test_bad_subcommand(self):
        r = lint("bad_subcommand.yaml")
        errs = error_messages(r)
        self.assertTrue(any("unknown sub-command 'typo-goo'" in m for m in errs), errs)

    def test_bad_timeout(self):
        r = lint("bad_timeout.yaml")
        errs = error_messages(r)
        self.assertTrue(any("invalid timeout" in m for m in errs), errs)

    def test_hex_out_of_range(self):
        r = lint("hex_out_of_range.yaml")
        errs = error_messages(r)
        self.assertTrue(any("out of int8 range" in m for m in errs), errs)

    def test_wait_without_timeout(self):
        r = lint("wait_no_timeout.yaml")
        errs = error_messages(r)
        self.assertTrue(any("requires step field 'timeout:'" in m for m in errs), errs)


class CLI(unittest.TestCase):
    def test_json_output_shape(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = plt_lint.main([
                "--catalog", str(TOOL_ROOT / "plt_command_catalog.json"),
                "--json",
                str(FIXTURES / "valid_minimal.yaml"),
                str(FIXTURES / "unknown_command.yaml"),
            ])
        self.assertEqual(code, 1)  # unknown_command.yaml has an error
        payload = json.loads(buf.getvalue())
        self.assertEqual(len(payload["files"]), 2)
        self.assertEqual(payload["files"][0]["errors"], [])
        self.assertTrue(payload["files"][1]["errors"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
