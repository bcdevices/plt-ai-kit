#!/usr/bin/env python3
"""
plt_lint.py

Offline validator for PLT (Production Line Tool) test-plan YAML files.

Validates:
  * top-level plan structure (title, suite, setup, teardown, ...)
  * step-level fields (unknown fields, required fields)
  * each step's command against the command catalog:
      - command name is registered
      - argument count >= MinArgs
      - argument types (canPort, uartPort, powerRail, uint32, hexByte, ...)
      - sub-command dispatch (ble gatt <sub>, usb storage <sub>, ...)
      - enum-restricted arguments
      - required step params (e.g. wait needs 'timeout', agentFetch needs 'with')
      - disallowed step params (warning only)

The catalog is loaded from plt_command_catalog.json (adjacent to this file
by default). It is a static input to this tool — regenerate it from the
upstream plt-os repository and commit the result here.

Usage:
    plt-lint <plan.yaml> [<plan2.yaml> ...]
    plt-lint --catalog my_catalog.json plan.yaml
    plt-lint --strict plan.yaml           # unknown top-level/step fields fail
    plt-lint --json plan.yaml             # machine-readable output
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "plt-lint: this tool requires PyYAML. Install with `pip install pyyaml`.\n"
    )
    sys.exit(3)


DEFAULT_CATALOG = Path(__file__).with_name("plt_command_catalog.json")

# YAML fields recognised on the top-level plan.
TOP_LEVEL_FIELDS = {
    "title", "dutProduct", "dutVersion", "identPrefix", "identprefix",
    "bomRev", "panel", "panel-setup", "setup", "trigger", "suite",
    "teardown", "panel-teardown", "calibration", "runs-on",
}
REQUIRED_TOP_LEVEL = {"suite"}


# Step-level field aliases and validation.
# All fields the runtime accepts on a step object, mirroring stepSchema() in
# ly10_pltrunner/internal/suite/schema.go.
DEFAULT_STEP_FIELDS = {
    "command", "expect", "extract", "extractKey", "extractkey",
    "fail", "ground", "id", "ident", "if", "interface", "pack",
    "path", "retry", "send", "target", "timeout", "timeoutms",
    "timeoutMs", "title", "uartcmd", "uartCmd", "with",
    "parent", "agent",
}


# ---------------------------------------------------------------------------
# Command-line tokenization (mirror of ly10_pltrunner/internal/plt/splitLine).
# ---------------------------------------------------------------------------


def split_command_line(line: str) -> list[str]:
    """Match the tokenizer at internal/plt/parser.go:splitLine.

    - spaces separate fields
    - double quotes group tokens (quotes are consumed, not preserved)
    - inside quotes, a backslash escapes the next rune (rune kept verbatim, plus
      the backslash itself is kept -- consistent with the Go implementation).
    """
    in_quote = False
    escape = False
    fields: list[str] = []
    buf: list[str] = []
    for r in line:
        if in_quote:
            if escape:
                buf.append(r)
                escape = False
                continue
            if r == '"':
                in_quote = False
            else:
                buf.append(r)
                if r == "\\":
                    escape = True
        else:
            if r == " ":
                if buf:
                    fields.append("".join(buf))
                    buf = []
            elif r == '"':
                in_quote = True
                escape = False
            else:
                buf.append(r)
    if buf:
        fields.append("".join(buf))
    return fields


# ---------------------------------------------------------------------------
# Value-type validators (matched to catalog `type` names).
# ---------------------------------------------------------------------------


_HANDLE_FORBIDDEN = set("./:\n\t\r")
_CAN_PORT_RE = re.compile(r"^CAN(\d+)$")
_KEY_MACRO_RE = re.compile(r"^%[A-Za-z_][A-Za-z0-9_]*%$")


def _is_key_macro(s: str) -> bool:
    """`%KEY%` placeholders can substitute for any typed argument at runtime."""
    return bool(_KEY_MACRO_RE.match(s))


def _parse_int(s: str) -> int | None:
    """Emulate Go's strconv.ParseInt(..., 0, ...) — accepts 0x, 0o, 0b, dec."""
    try:
        s2 = s
        if s2.startswith(("+", "-")):
            sign = -1 if s2[0] == "-" else 1
            s2 = s2[1:]
        else:
            sign = 1
        if s2.startswith(("0x", "0X")):
            return sign * int(s2, 16)
        if s2.startswith(("0o", "0O")):
            return sign * int(s2, 8)
        if s2.startswith(("0b", "0B")):
            return sign * int(s2, 2)
        return sign * int(s2, 10)
    except (ValueError, IndexError):
        return None


def _check_uint(value: str, bits: int) -> str | None:
    if _is_key_macro(value):
        return None
    n = _parse_int(value)
    if n is None:
        return f"expected unsigned integer, got {value!r}"
    if n < 0:
        return f"expected non-negative integer, got {value!r}"
    if n >= 1 << bits:
        return f"value {value!r} exceeds {bits}-bit range"
    return None


def _check_int(value: str, bits: int) -> str | None:
    if _is_key_macro(value):
        return None
    n = _parse_int(value)
    if n is None:
        return f"expected integer, got {value!r}"
    limit = 1 << (bits - 1)
    if n < -limit or n >= limit:
        return f"value {value!r} exceeds {bits}-bit range"
    return None


def _check_hex_byte(value: str) -> str | None:
    if _is_key_macro(value):
        return None
    n = _parse_int(value)
    if n is None:
        return f"invalid payload byte {value!r}"
    # strconv.ParseInt(v, 0, 8) accepts -128..127
    if n < -128 or n > 127:
        return f"payload byte {value!r} out of int8 range"
    return None


def _check_can_port(value: str) -> str | None:
    if _is_key_macro(value):
        return None
    m = _CAN_PORT_RE.match(value)
    if not m:
        return f"expected CANx port, got {value!r}"
    if int(m.group(1)) < 0:
        return f"CAN port index cannot be negative: {value!r}"
    return None


def _check_uart_port(value: str, uart_ports: set[str]) -> str | None:
    if _is_key_macro(value):
        return None
    if value in uart_ports:
        return None
    # UART{N} for N>=2 is accepted by the runtime (multi-channel and
    # simulated UART setups use these), but is non-standard on stock PLT-106.
    if re.match(r"^UART\d+$", value):
        return None
    return f"expected UARTx port, got {value!r}"


def _check_handle(value: str, kind: str) -> str | None:
    if _is_key_macro(value):
        return None
    if not value:
        return f"empty {kind} handle name"
    if any(ch in _HANDLE_FORBIDDEN for ch in value):
        return f"{kind} handle {value!r} contains forbidden characters"
    return None


def _check_power_rail_or_off(value: str, rails: set[str]) -> str | None:
    if _is_key_macro(value):
        return None
    if value == "off":
        return None
    if value in rails:
        return None
    return f"expected 'off' or one of {sorted(rails)}, got {value!r}"


def _check_ground_range(value: str) -> str | None:
    if _is_key_macro(value):
        return None
    if value in ("all", "none"):
        return None
    # Accept forms like "1", "1-3", "1,3", "1-2,4"
    for part in value.split(","):
        m = re.match(r"^\d+(?:-\d+)?$", part)
        if not m:
            return f"invalid ground range {value!r}"
        if "-" in part:
            lo, hi = part.split("-")
            if int(lo) < 1 or int(hi) > 4 or int(lo) > int(hi):
                return f"invalid ground range {value!r}"
        else:
            if not (1 <= int(part) <= 4):
                return f"invalid ground range {value!r}"
    return None


def _check_uart_break_state(value: str) -> str | None:
    if _is_key_macro(value):
        return None
    if value in ("on", "off"):
        return None
    n = _parse_int(value)
    if n is None or n < 1:
        return f"expected 'on', 'off', or positive milliseconds, got {value!r}"
    return None


def _check_uart_speed_or_tp(value: str) -> str | None:
    if _is_key_macro(value):
        return None
    if value == "tp":
        return None
    n = _parse_int(value)
    if n is None or n <= 0:
        return f"expected 'tp' or positive baud rate, got {value!r}"
    return None


def _check_timeout(value: Any) -> str | None:
    if isinstance(value, int):
        if value < 0:
            return f"timeout may not be negative"
        return None
    if not isinstance(value, str):
        return f"timeout must be a string or integer milliseconds"
    if _is_key_macro(value):
        return None
    # decimal float first (Go run.go parseTimeout)
    if re.match(r"^\d+(\.\d+)?$", value):
        return None
    # otherwise a Go duration string: e.g. "5s", "200ms", "1m30s"
    if re.match(r"^([-+]?\d+(\.\d+)?(ns|us|µs|ms|s|m|h))+$", value):
        return None
    return f"invalid timeout {value!r} (expect e.g. '5s', '200ms', or integer ms)"


TYPE_CHECKERS = {
    "canPort": lambda v, ctx: _check_can_port(v),
    "uartPort": lambda v, ctx: _check_uart_port(v, ctx["uart_ports"]),
    "agentHandle": lambda v, ctx: _check_handle(v, "agent"),
    "scpiHandle": lambda v, ctx: _check_handle(v, "SCPI"),
    "storageHandle": lambda v, ctx: _check_handle(v, "storage"),
    "powerRailOrOff": lambda v, ctx: _check_power_rail_or_off(v, ctx["power_rails"]),
    "powerStateOrLevel": lambda v, ctx: None,  # covered by runtime + power rail context
    "uartBreakState": lambda v, ctx: _check_uart_break_state(v),
    "uartSpeedOrTp": lambda v, ctx: _check_uart_speed_or_tp(v),
    "hexByte": lambda v, ctx: _check_hex_byte(v),
    "groundRange": lambda v, ctx: _check_ground_range(v),
    "int": lambda v, ctx: _check_int(v, 32),
    "int16": lambda v, ctx: _check_int(v, 16),
    "int32": lambda v, ctx: _check_int(v, 32),
    "uint": lambda v, ctx: _check_uint(v, 32),
    "uint32": lambda v, ctx: _check_uint(v, 32),
    "string": lambda v, ctx: None,
}


# ---------------------------------------------------------------------------
# Data model.
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    file: str
    location: str
    message: str
    severity: str = "error"  # or "warning"

    def format(self) -> str:
        return f"{self.severity.upper()}: {self.file}:{self.location}: {self.message}"


@dataclass
class LintResult:
    findings: list[Finding] = field(default_factory=list)

    def add(self, *a, **kw) -> None:
        self.findings.append(Finding(*a, **kw))

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")

    def ok(self) -> bool:
        return self.error_count == 0


# ---------------------------------------------------------------------------
# Catalog helpers.
# ---------------------------------------------------------------------------


def load_catalog(path: Path) -> dict:
    """Load the command catalog JSON.

    The catalog is a static input to this tool. It is generated and
    maintained in the upstream plt-os repository and checked in here; this
    tool does not regenerate it or verify it against a source of truth.
    """
    if not path.exists():
        raise SystemExit(
            f"plt-lint: catalog {path} does not exist. Copy the generated "
            f"plt_command_catalog.json from the plt-os repository."
        )
    with path.open() as fh:
        cat = json.load(fh)
    if cat.get("schema_version") != "1":
        raise SystemExit(
            f"plt-lint: catalog {path} has schema_version={cat.get('schema_version')!r}, "
            f"expected '1'"
        )
    return cat


def commands_by_name(catalog: dict) -> dict[str, dict]:
    return {c["name"]: c for c in catalog["commands"]}


# ---------------------------------------------------------------------------
# Core linter.
# ---------------------------------------------------------------------------


def _step_params_provided(step: dict) -> set[str]:
    """Which step-level fields carry meaningful values."""
    provided = set()
    for k, v in step.items():
        if v in (None, "", [], {}):
            continue
        provided.add(k)
    return provided


def _lint_command_step(
    step: dict,
    step_loc: str,
    file: str,
    catalog: dict,
    cmd_index: dict[str, dict],
    result: LintResult,
    strict: bool,
) -> None:
    command = step.get("command")
    if command is None:
        result.add(file, step_loc, "step has no 'command:' field")
        return
    if not isinstance(command, str):
        result.add(file, step_loc, f"'command' must be a string, got {type(command).__name__}")
        return

    fields = split_command_line(command)
    if not fields:
        result.add(file, step_loc, "empty command string")
        return

    name = fields[0]
    args = fields[1:]
    entry = cmd_index.get(name)
    if entry is None:
        result.add(
            file, step_loc,
            f"unknown command {name!r} (see -command-list or catalog for valid names)",
        )
        return

    if len(args) < entry.get("min_args", 0):
        result.add(
            file, step_loc,
            f"'{name}' requires at least {entry['min_args']} arg(s), got {len(args)}"
            f" — usage: {entry.get('usage', name)}",
        )
        return

    ctx = {
        "uart_ports": set(catalog.get("uart_ports", ["UART0", "UART1"])),
        "power_rails": set(catalog.get("power_rails", [])),
    }

    # Sub-command dispatch if declared.
    subs = entry.get("subcommands") or []
    if subs:
        sub_names = [s["name"] for s in subs]
        if not args:
            result.add(file, step_loc, f"'{name}' expects a sub-command; one of {sub_names}")
            return
        sub_entry = next((s for s in subs if s["name"] == args[0]), None)
        if sub_entry is None:
            result.add(
                file, step_loc,
                f"'{name}' unknown sub-command {args[0]!r}; expected one of {sub_names}",
            )
            return
        if len(fields) < sub_entry.get("min_args", entry["min_args"]):
            result.add(
                file, step_loc,
                f"'{name} {sub_entry['name']}' requires at least "
                f"{sub_entry['min_args']} tokens total, got {len(fields)}",
            )
            return
        _check_args(entry, sub_entry.get("args", []), args[1:], name, step_loc, file, ctx, result)
    else:
        _check_args(entry, entry.get("args", []), args, name, step_loc, file, ctx, result)

    # Required step params.
    provided = _step_params_provided(step)
    for req in entry.get("require_params", []):
        # 'expect' is often supplied inline in the command string for certain
        # commands; treat that as satisfying the requirement.
        if req not in provided:
            result.add(file, step_loc, f"'{name}' requires step field '{req}:'")

    # Disallowed step params → warning (runtime silently ignores them, but the
    # author almost certainly meant something).
    allowed = set(entry.get("allowed_params", []))
    if allowed:
        step_params = provided - {"command", "title", "fail", "ident", "if", "retry"}
        # Fields consumed universally by the runner (structural).
        universal = {"title", "fail", "ident", "if", "retry"}
        for p in sorted(step_params - allowed - universal):
            result.add(
                file, step_loc,
                f"'{name}' has step field '{p}:' which the command does not consume",
                severity="warning",
            )


def _check_args(
    entry: dict,
    schema_args: list[dict],
    provided_args: list[str],
    name: str,
    step_loc: str,
    file: str,
    ctx: dict,
    result: LintResult,
) -> None:
    """Match provided positional args against a list of CatalogArg specs."""
    idx = 0
    for spec in schema_args:
        if spec.get("variadic"):
            # Consume the remainder.
            rest = provided_args[idx:]
            if not rest and not spec.get("optional"):
                result.add(
                    file, step_loc,
                    f"'{name}' missing required '{spec['name']}' argument(s)",
                )
                return
            for j, v in enumerate(rest):
                err = _check_one(spec, v, ctx)
                if err:
                    result.add(file, step_loc, f"'{name}' arg #{idx + j + 1} ({spec['name']}): {err}")
            return
        if idx >= len(provided_args):
            if not spec.get("optional"):
                result.add(
                    file, step_loc,
                    f"'{name}' missing required '{spec['name']}' argument"
                    f" — usage: {entry.get('usage', name)}",
                )
                return
            idx += 1
            continue
        err = _check_one(spec, provided_args[idx], ctx)
        if err:
            result.add(file, step_loc, f"'{name}' arg #{idx + 1} ({spec['name']}): {err}")
        idx += 1
    # Extra positional args are permitted for commands where the spec is
    # deliberately loose (e.g. program's variadic image list). Runtime will
    # decide; we don't error here.


def _check_one(spec: dict, value: str, ctx: dict) -> str | None:
    """Check one positional arg. Returns None on success or an error message."""
    if spec.get("enum") and value not in spec["enum"]:
        # allow key-macro substitutions
        if not _is_key_macro(value):
            return f"expected one of {spec['enum']}, got {value!r}"
    t = spec.get("type", "string")
    checker = TYPE_CHECKERS.get(t)
    if checker is None:
        return None  # unknown type — fall through as string
    return checker(value, ctx)


def _lint_step(
    step: Any,
    step_loc: str,
    file: str,
    catalog: dict,
    cmd_index: dict[str, dict],
    result: LintResult,
    strict: bool,
) -> None:
    if not isinstance(step, dict):
        result.add(file, step_loc, f"step must be a mapping, got {type(step).__name__}")
        return

    # Field-name check.
    known = DEFAULT_STEP_FIELDS
    for k in step.keys():
        if k not in known:
            severity = "error" if strict else "warning"
            result.add(file, step_loc, f"unknown step field {k!r}", severity=severity)

    # Timeout format.
    if "timeout" in step:
        err = _check_timeout(step["timeout"])
        if err:
            result.add(file, step_loc, err)

    # If it's a uart-cmd step, we don't validate command syntax the same way.
    if "command" in step:
        _lint_command_step(step, step_loc, file, catalog, cmd_index, result, strict)
    elif "uartcmd" in step or "uartCmd" in step:
        # These bypass the command catalog entirely; just check timeout above.
        return
    else:
        result.add(file, step_loc, "step is missing a 'command:' or 'uartcmd:' field")


def _lint_steps(
    section: str,
    steps: Any,
    file: str,
    catalog: dict,
    cmd_index: dict[str, dict],
    result: LintResult,
    strict: bool,
    parent_ident: str | None = None,
) -> None:
    if steps is None:
        return
    if not isinstance(steps, list):
        result.add(file, section, f"'steps' must be a list, got {type(steps).__name__}")
        return
    for i, step in enumerate(steps):
        loc = f"{section}[{i}]" if parent_ident is None else f"{section}({parent_ident})[{i}]"
        _lint_step(step, loc, file, catalog, cmd_index, result, strict)


def lint_plan(
    doc: Any,
    file: str,
    catalog: dict,
    strict: bool = False,
) -> LintResult:
    result = LintResult()
    cmd_index = commands_by_name(catalog)

    if not isinstance(doc, dict):
        result.add(file, "", f"top-level YAML must be a mapping, got {type(doc).__name__}")
        return result

    for k in doc.keys():
        if k not in TOP_LEVEL_FIELDS:
            severity = "error" if strict else "warning"
            result.add(file, "", f"unknown top-level field {k!r}", severity=severity)

    for req in REQUIRED_TOP_LEVEL:
        if req not in doc:
            result.add(file, "", f"missing required top-level field {req!r}")

    # setup, panel-setup, trigger, teardown, panel-teardown all have {steps: [...]}
    for section in ("setup", "panel-setup", "trigger", "teardown", "panel-teardown"):
        if section in doc:
            block = doc[section]
            if not isinstance(block, dict):
                result.add(file, section, f"{section!r} must be a mapping with 'steps:'")
                continue
            _lint_steps(section, block.get("steps"), file, catalog, cmd_index, result, strict)

    # suite: list of items each with { ident, title, steps: [...] }
    suite = doc.get("suite")
    if suite is not None:
        if not isinstance(suite, list):
            result.add(file, "suite", f"'suite' must be a list, got {type(suite).__name__}")
        else:
            for i, item in enumerate(suite):
                if not isinstance(item, dict):
                    result.add(
                        file, f"suite[{i}]",
                        f"suite item must be a mapping, got {type(item).__name__}",
                    )
                    continue
                ident = item.get("ident")
                _lint_steps(
                    f"suite[{i}]", item.get("steps"), file, catalog, cmd_index,
                    result, strict, parent_ident=ident,
                )

    return result


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def _read_yaml(path: Path) -> Any:
    with path.open() as fh:
        return yaml.safe_load(fh)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="plt-lint",
        description="Offline linter for PLT test-plan YAML.",
    )
    ap.add_argument("files", nargs="+", help="test plan YAML file(s) to lint")
    ap.add_argument(
        "--catalog", type=Path, default=DEFAULT_CATALOG,
        help=f"path to command catalog JSON (default: {DEFAULT_CATALOG})",
    )
    ap.add_argument(
        "--strict", action="store_true",
        help="treat unknown top-level and step fields as errors (not warnings)",
    )
    ap.add_argument(
        "--json", dest="json_output", action="store_true",
        help="emit findings as a JSON document on stdout",
    )
    ap.add_argument(
        "-q", "--quiet", action="store_true",
        help="on success, print nothing",
    )
    ns = ap.parse_args(argv)

    catalog = load_catalog(ns.catalog)
    all_results: list[tuple[str, LintResult]] = []

    for f in ns.files:
        path = Path(f)
        try:
            doc = _read_yaml(path)
        except yaml.YAMLError as e:
            r = LintResult()
            r.add(str(path), "", f"YAML parse error: {e}")
            all_results.append((str(path), r))
            continue
        r = lint_plan(doc, str(path), catalog, strict=ns.strict)
        all_results.append((str(path), r))

    exit_code = 0
    if ns.json_output:
        payload = {
            "files": [
                {
                    "file": name,
                    "errors": [
                        f.__dict__ for f in r.findings if f.severity == "error"
                    ],
                    "warnings": [
                        f.__dict__ for f in r.findings if f.severity == "warning"
                    ],
                }
                for name, r in all_results
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        for name, r in all_results:
            if r.findings:
                for f in r.findings:
                    print(f.format())
            elif not ns.quiet:
                print(f"OK: {name}")
    if any(not r.ok() for _, r in all_results):
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
