#!/usr/bin/env python3
"""Static validator for GitHub Skills exercise repositories.

Checks repository structure, workflow wiring, grading, workflow security, step
content, README conventions and learning-design heuristics, then prints a report
grouped by severity (Blocking / Important / Nice to improve).

Only the Python standard library is required. When PyYAML is installed it is used
to parse workflows; otherwise a built-in parser for the YAML subset used by GitHub
Actions workflows is used.

Usage:
  python validate_exercise.py [REPO_DIR] [--format text|markdown|json]
                              [--strict] [--online] [--template-repo OWNER/NAME]

Exit status: 1 when blocking findings exist (or important ones with --strict).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:  # Optional dependency.
    import yaml  # type: ignore

    YAML_ENGINE = "PyYAML"
except ImportError:  # pragma: no cover - exercised when PyYAML is absent
    yaml = None
    YAML_ENGINE = "built-in subset parser"

KNOWN_GOOD_TOOLKIT = "v0.9.3"
READING_WPM = 200  # technical reading speed for novices
MINUTES_PER_INSTRUCTION = 0.75
MINUTES_FEEDBACK_WAIT = 1.0
SEVERITIES = ("error", "warning", "info")
LABELS = {"error": "Blocking", "warning": "Important", "info": "Nice to improve"}

STEP_HEADING_RE = re.compile(r"^##\s+Step\s+(\d+)\s*:?\s*(.*)$")
THEORY_RE = re.compile(r"^(#{2,3})\s+(?:(\U0001F4D6|:book:)\s*)?Theory\b\s*:?\s*(.*)$")
ACTIVITY_RE = re.compile(r"^(#{2,3})\s+(?:(\u2328\ufe0f?|:keyboard:)\s*)?Activity\b\s*(\d+)?\s*:?\s*(.*)$")
H2_OR_H3_RE = re.compile(r"^#{2,3}\s")
TOP_ITEM_RE = re.compile(r"^(\d+)\.\s+\S")
NESTED_ITEM_RE = re.compile(r"^( +)(?:\d+\.|[-*+])\s+\S")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
IMG_MD_RE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]+)[^)]*\)")
LINK_MD_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(\s*([^)\s]+)[^)]*\)")
ATTR_RE = r'{}\s*=\s*["\']([^"\']*)["\']'
NUNJUCKS_VAR_RE = re.compile(r"(?<!\$)\{\{\s*([A-Za-z_]\w*)")
RAW_BLOCK_RE = re.compile(r"\{%-?\s*raw\s*-?%\}.*?\{%-?\s*endraw\s*-?%\}", re.DOTALL)
ENABLE_RE = re.compile(r"gh\s+workflow\s+enable\s+[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"replace-me|<STEP>|<NEXT_STEP>", re.IGNORECASE)
INJECTION_RE = re.compile(
    r"\$\{\{\s*(github\.event\.(issue\.(title|body)|comment\.body|review\.body|review_comment\.body|"
    r"pull_request\.(title|body|head\.ref|head\.label)|discussion\.(title|body)|"
    r"head_commit\.(message|author\.(name|email))|commits\b[^}]*\.(message|author)|pages\b[^}]*page_name|"
    r"workflow_run\.head_branch)|github\.head_ref)\b"
)
VAGUE_VERBS = ("understand", "know", "learn", "appreciate", "be aware", "become familiar", "explore")
VAGUE_LINK_TEXT = {"here", "click here", "this", "this link", "link", "read more", "more"}


# --------------------------------------------------------------------------- report


@dataclass
class Finding:
    severity: str
    rule: str
    path: str
    message: str
    fix: str = ""
    line: int | None = None


@dataclass
class Report:
    root: str
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def add(self, severity, rule, path, message, fix="", line=None):
        shown = Path(path).as_posix() if str(path) not in ("-", "") else str(path)
        self.findings.append(Finding(severity, rule, shown, message, fix, line))

    def count(self, severity):
        return sum(1 for f in self.findings if f.severity == severity)


# --------------------------------------------------------------------------- mini YAML


class MiniYAMLError(ValueError):
    pass


class MiniYAML:
    """Parser for the block-style YAML subset used by GitHub Actions workflows.

    Supports block mappings and sequences, literal and folded block scalars,
    single-line flow sequences and mappings, quoted and plain scalars, comments
    and folded plain-scalar continuation lines. Anchors, aliases and tags are
    treated as plain text.
    """

    def __init__(self, text: str):
        self.lines = text.replace("\t", "    ").splitlines()
        self.i = 0

    @staticmethod
    def _indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    def _skip(self):
        while self.i < len(self.lines):
            st = self.lines[self.i].strip()
            if st == "" or st.startswith("#") or st in ("---", "..."):
                self.i += 1
                continue
            break

    def parse(self):
        self._skip()
        if self.i >= len(self.lines):
            return None
        return self._block(self._indent(self.lines[self.i]))

    def _block(self, ind):
        self._skip()
        content = self.lines[self.i].strip()
        if content == "-" or content.startswith("- "):
            return self._seq(ind)
        return self._map(ind)

    @staticmethod
    def _strip_comment(s: str) -> str:
        quote = None
        for idx, ch in enumerate(s):
            if quote:
                if ch == quote:
                    quote = None
            elif ch in "'\"" and (idx == 0 or s[idx - 1] in " [{,:"):
                quote = ch
            elif ch == "#" and (idx == 0 or s[idx - 1] in " \t"):
                return s[:idx].rstrip()
        return s.rstrip()

    @staticmethod
    def _split_key(content: str):
        quote = None
        for idx, ch in enumerate(content):
            if quote:
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"" and idx == 0:
                quote = ch
                continue
            if ch == ":" and (idx + 1 == len(content) or content[idx + 1] in " \t"):
                key = content[:idx].strip()
                if len(key) >= 2 and key[0] == key[-1] and key[0] in "'\"":
                    key = key[1:-1]
                return key, content[idx + 1:].strip()
        return None, content

    def _map(self, ind):
        result = {}
        while True:
            self._skip()
            if self.i >= len(self.lines):
                break
            raw = self.lines[self.i]
            cur = self._indent(raw)
            if cur < ind:
                break
            if cur > ind:
                raise MiniYAMLError(f"unexpected indentation at line {self.i + 1}")
            content = raw.strip()
            if content == "-" or content.startswith("- "):
                break
            key, rest = self._split_key(content)
            if key is None:
                raise MiniYAMLError(f"expected 'key: value' at line {self.i + 1}")
            self.i += 1
            result[key] = self._value(rest, ind)
        return result

    def _seq(self, ind):
        result = []
        while True:
            self._skip()
            if self.i >= len(self.lines):
                break
            raw = self.lines[self.i]
            cur = self._indent(raw)
            if cur != ind:
                if cur > ind:
                    raise MiniYAMLError(f"unexpected indentation at line {self.i + 1}")
                break
            content = raw.strip()
            if not (content == "-" or content.startswith("- ")):
                break
            after = content[1:]
            item = after.strip()
            item_indent = cur + 1 + (len(after) - len(after.lstrip(" ")))
            if item == "":
                self.i += 1
                self._skip()
                if self.i < len(self.lines) and self._indent(self.lines[self.i]) > ind:
                    result.append(self._block(self._indent(self.lines[self.i])))
                else:
                    result.append(None)
                continue
            key, _ = self._split_key(self._strip_comment(item))
            if key is not None and not item.startswith(("[", "{")):
                self.lines[self.i] = " " * item_indent + item
                result.append(self._map(item_indent))
            else:
                self.i += 1
                result.append(self._value(item, ind))
        return result

    def _value(self, rest, ind):
        if rest[:1] in ("|", ">"):
            return self._block_scalar(rest, ind)
        rest = self._strip_comment(rest)
        if rest == "":
            self._skip()
            if self.i >= len(self.lines):
                return None
            nxt = self.lines[self.i]
            nind = self._indent(nxt)
            content = nxt.strip()
            if nind == ind and (content == "-" or content.startswith("- ")):
                return self._seq(ind)
            if nind <= ind:
                return None
            if content == "-" or content.startswith("- ") or self._split_key(self._strip_comment(content))[0] is not None:
                return self._block(nind)
            self.i += 1
            return self._value(content, nind - 1)
        if rest[0] in "[{":
            text = rest
            while not self._balanced(text) and self.i < len(self.lines):
                text += " " + self._strip_comment(self.lines[self.i].strip())
                self.i += 1
            end = self._flow_end(text)
            if end < 0:
                raise MiniYAMLError(f"unterminated flow collection (line {self.i})")
            if self._strip_comment(text[end + 1:]).strip():
                raise MiniYAMLError(f"unexpected text after flow collection (line {self.i})")
            return self._flow(text[:end + 1])
        if rest[0] in "'\"":
            text = rest
            while self._quote_end(text) < 0 and self.i < len(self.lines):
                nxt = self.lines[self.i].strip()
                text += (" " if nxt else "\n") + nxt
                self.i += 1
            end = self._quote_end(text)
            if end < 0:
                raise MiniYAMLError(f"unterminated quoted scalar (line {self.i})")
            if self._strip_comment(text[end + 1:]).strip():
                raise MiniYAMLError(f"unexpected text after quoted scalar (line {self.i})")
            return self._quoted(text[:end + 1])
        parts = [rest]
        while self.i < len(self.lines):
            nxt = self.lines[self.i]
            if nxt.strip() == "" or self._indent(nxt) <= ind or nxt.strip().startswith("#"):
                break
            parts.append(self._strip_comment(nxt.strip()))
            self.i += 1
        text = " ".join(parts)
        if ": " in text or text.endswith(":"):
            raise MiniYAMLError(f"mapping values are not allowed here (line {self.i}); quote the value")
        return self._scalar(text)

    @staticmethod
    def _quote_end(text):
        """Index of the quote that closes text[0], or -1 if it is not closed."""
        q, idx = text[0], 1
        while idx < len(text):
            ch = text[idx]
            if q == '"' and ch == "\\":
                idx += 2
                continue
            if ch == q:
                if q == "'" and text[idx + 1:idx + 2] == "'":
                    idx += 2
                    continue
                return idx
            idx += 1
        return -1

    @staticmethod
    def _flow_end(text):
        """Index of the bracket that closes text[0], or -1 if it is not closed."""
        depth, quote = 0, None
        for idx, ch in enumerate(text):
            if quote:
                if ch == quote:
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    return idx
        return -1

    @staticmethod
    def _balanced(text):
        depth, quote = 0, None
        for ch in text:
            if quote:
                if ch == quote:
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
        return depth <= 0

    def _block_scalar(self, header, ind):
        style = header[0]
        chomp = "-" if "-" in header[1:3] else "+" if "+" in header[1:3] else ""
        body, block_ind = [], None
        while self.i < len(self.lines):
            raw = self.lines[self.i]
            if raw.strip() == "":
                body.append("")
                self.i += 1
                continue
            cur = self._indent(raw)
            if cur <= ind:
                break
            if block_ind is None:
                block_ind = cur
            if cur < block_ind:
                break
            body.append(raw[block_ind:])
            self.i += 1
        trailing = 0
        while body and body[-1] == "":
            body.pop()
            trailing += 1
        if style == "|":
            text = "\n".join(body)
        else:
            text = self._fold(body)
        if chomp == "-":
            return text
        if chomp == "+":
            return text + "\n" * (trailing + 1)
        return text + "\n" if text else ""

    @staticmethod
    def _fold(body):
        """Folded scalar: join normal lines with spaces; keep breaks around more-indented lines."""
        filled = [i for i, line in enumerate(body) if line != ""]
        if not filled:
            return ""
        text = "\n" * filled[0] + body[filled[0]]
        for a, b in zip(filled, filled[1:]):
            gap = b - a - 1
            more = body[a][:1] in (" ", "\t") or body[b][:1] in (" ", "\t")
            sep = "\n" * (gap + 1) if more else (" " if gap == 0 else "\n" * gap)
            text += sep + body[b]
        return text

    def _flow(self, text):
        text = text.strip()
        if text in ("[]", "{}"):
            return [] if text == "[]" else {}
        inner = text[1:-1]
        items, buf, depth, quote = [], "", 0, None
        for ch in inner:
            if quote:
                buf += ch
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"":
                quote = ch
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
            if ch == "," and depth == 0:
                items.append(buf.strip())
                buf = ""
            else:
                buf += ch
        if buf.strip():
            items.append(buf.strip())
        if text[0] == "[":
            return [self._flow(i) if i[:1] in "[{" else self._quoted(i) if i[:1] in "'\"" else self._scalar(i) for i in items]
        result = {}
        for item in items:
            key, val = self._split_key(item)
            if key is None:
                key, val = item, None
            result[key] = None if val in (None, "") else self._quoted(val) if val[:1] in "'\"" else self._scalar(val)
        return result

    @staticmethod
    def _quoted(text):
        q = text[0]
        end = len(text) - 1
        while end > 0 and text[end] != q:
            end -= 1
        inner = text[1:end] if end > 0 else text[1:]
        if q == "'":
            return inner.replace("''", "'")
        return bytes(inner, "utf-8").decode("unicode_escape", errors="replace") if "\\" in inner else inner

    @staticmethod
    def _scalar(text):
        low = text.lower()
        if low in ("true", "false"):
            return low == "true"
        if low in ("null", "~"):
            return None
        if re.fullmatch(r"-?\d+", text):
            return int(text)
        if re.fullmatch(r"-?\d+\.\d+", text):
            return float(text)
        return text


def load_yaml(text: str):
    if yaml is not None:
        return yaml.safe_load(text)
    return MiniYAML(text).parse()


# --------------------------------------------------------------------------- helpers


def read(path: Path) -> str:
    # utf-8-sig drops a byte order mark, which Windows editors often add.
    return path.read_text(encoding="utf-8-sig", errors="replace")


def line_of(text: str, needle: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    return None


def code_mask(lines: list[str]) -> list[bool]:
    """True for lines inside (or delimiting) a fenced code block."""
    mask, fence = [], None
    for line in lines:
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(1)
            mask.append(True)
        elif fence is not None:
            mask.append(True)
            if line.strip().startswith(fence):
                fence = None
        else:
            mask.append(False)
    return mask


def without_raw(text: str) -> str:
    return RAW_BLOCK_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def words(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"https?://\S+", " ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def triggers_of(data: dict) -> dict:
    on = data.get("on", data.get(True)) if isinstance(data, dict) else None
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return {str(e): None for e in on}
    return on if isinstance(on, dict) else {}


def glob_to_regex(pattern: str) -> re.Pattern:
    out, i = "", 0
    while i < len(pattern):
        ch = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
            continue
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
            continue
        out += {"*": "[^/]*", "?": "[^/]"}.get(ch, re.escape(ch))
        i += 1
    return re.compile("^" + out + "$")


def repo_slug_from_git(root: Path) -> str | None:
    if not shutil.which("git"):
        return None
    try:
        url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"], capture_output=True,
                             text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    return f"{m.group(1)}/{m.group(2)}" if m else None


# --------------------------------------------------------------------------- model


@dataclass
class Activity:
    number: int | None
    title: str
    emoji: str | None
    level: int
    start: int
    lines: list[str]
    has_trouble: bool
    instructions: int
    max_depth: int
    list_breaks: list[tuple[int, bool]]  # (line, numbering visibly restarts at 1)


@dataclass
class StepDoc:
    number: int
    path: Path
    text: str
    heading_number: int | None = None
    theory_count: int = 0
    theory_words: int = 0
    activities: list[Activity] = field(default_factory=list)
    total_words: int = 0


@dataclass
class Workflow:
    path: Path
    number: int | None
    text: str
    data: dict | None
    error: str | None = None

    @property
    def name(self) -> str:
        if not isinstance(self.data, dict):
            return ""
        return str(self.data.get("name", "")).split("#")[0].strip()

    @property
    def jobs(self) -> dict:
        jobs = self.data.get("jobs") if isinstance(self.data, dict) else None
        return jobs if isinstance(jobs, dict) else {}

    @property
    def env(self) -> dict:
        env = self.data.get("env") if isinstance(self.data, dict) else None
        return env if isinstance(env, dict) else {}

    def steps(self):
        for job_id, job in self.jobs.items():
            if isinstance(job, dict):
                for step in as_list(job.get("steps")):
                    if isinstance(step, dict):
                        yield job_id, job, step

    def runs(self):
        for _, _, step in self.steps():
            if isinstance(step.get("run"), str):
                yield step["run"]

    def enables(self) -> list[str]:
        return [m.strip() for run in self.runs() for m in ENABLE_RE.findall(run)]

    def calls(self, needle: str) -> bool:
        return any(isinstance(j, dict) and needle in str(j.get("uses", "")) for j in self.jobs.values())


def parse_step(path: Path, number: int) -> StepDoc:
    text = read(path)
    doc = StepDoc(number=number, path=path, text=text, total_words=words(text))
    lines = text.splitlines()
    mask = code_mask(lines)
    for idx, line in enumerate(lines):
        if mask[idx]:
            continue
        m = STEP_HEADING_RE.match(line)
        if m and doc.heading_number is None:
            doc.heading_number = int(m.group(1))
    sections, current = [], None
    for idx, line in enumerate(lines):
        if not mask[idx] and H2_OR_H3_RE.match(line):
            current = [idx, line, []]
            sections.append(current)
        elif current is not None:
            current[2].append((idx, line, mask[idx]))
    for start, heading, body in sections:
        if THEORY_RE.match(heading):
            doc.theory_count += 1
            doc.theory_words += words("\n".join(line for _, line, _ in body))
        am = ACTIVITY_RE.match(heading)
        if am:
            doc.activities.append(analyse_activity(start, heading, am, body))
    return doc


def analyse_activity(start, heading, match, body) -> Activity:
    raw = [line for _, line, _ in body]
    has_trouble = any(re.search(r"<summary>.*Having trouble", line, re.IGNORECASE) for line in raw)
    instructions, depth, breaks = 0, 1, []
    item_lines = [i for i, (_, line, in_code) in enumerate(body) if not in_code and TOP_ITEM_RE.match(line)]
    for i, (_, line, in_code) in enumerate(body):
        if not in_code and TOP_ITEM_RE.match(line):
            instructions += 1
        nm = NESTED_ITEM_RE.match(line)
        if nm and not in_code:
            depth = max(depth, 1 + (len(nm.group(1)) + 1) // 3)
    if len(item_lines) >= 2:
        first, last = item_lines[0], item_lines[-1]
        flagged_items = set()
        for i in range(first + 1, last):
            lineno, line, _ = body[i]
            prev = body[i - 1][1]
            if line.strip() and not line.startswith((" ", "\t")) and not TOP_ITEM_RE.match(line) and prev.strip() == "":
                nxt = next(j for j in item_lines if j > i)
                if nxt not in flagged_items:
                    flagged_items.add(nxt)
                    breaks.append((lineno + 1, TOP_ITEM_RE.match(body[nxt][1]).group(1) == "1"))
    title = match.group(4).strip()
    return Activity(
        number=int(match.group(3)) if match.group(3) else None,
        title=title,
        emoji=match.group(2),
        level=len(match.group(1)),
        start=start + 1,
        lines=raw,
        has_trouble=has_trouble,
        instructions=instructions,
        max_depth=depth,
        list_breaks=breaks,
    )


# --------------------------------------------------------------------------- checks


def load(root: Path, report: Report):
    steps_dir = root / ".github" / "steps"
    wf_dir = root / ".github" / "workflows"
    steps, review = {}, None
    if steps_dir.is_dir():
        for p in sorted(steps_dir.glob("*.md")):
            m = re.match(r"^(\d+)-", p.name)
            if m:
                n = int(m.group(1))
                if n in steps:
                    report.add("error", "S003", p.relative_to(root), f"Two step files share number {n}.",
                               "Give every step file a unique leading number.")
                steps[n] = parse_step(p, n)
            elif p.name.lower().startswith("x-"):
                review = p
    workflows = []
    if wf_dir.is_dir():
        for p in sorted(list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))):
            m = re.match(r"^(\d+)-", p.name)
            text = read(p)
            try:
                data = load_yaml(text)
                err = None
            except Exception as exc:  # noqa: BLE001 - report any parser error
                data, err = None, str(exc).splitlines()[0]
            workflows.append(Workflow(p, int(m.group(1)) if m else None, text, data, err))
    return steps, review, workflows


def check_structure(root, steps, review, workflows, report):
    if not (root / ".github" / "steps").is_dir() or not steps:
        report.add("error", "S001", ".github/steps", "No numbered step files found.",
                   "Create .github/steps/1-step.md, 2-step.md, ... from the scaffold templates.")
    numbers = sorted(steps)
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        report.add("error", "S002", ".github/steps", f"Step numbers are not contiguous from 1: {numbers}.",
                   "Renumber step files 1..N without gaps.")
    if len(numbers) > 5:
        report.add("warning", "S004", ".github/steps", f"{len(numbers)} steps. Exercises should have five or fewer.",
                   "Split the topic into a series of exercises (see the workshop-design skill).")
    if review is None:
        report.add("error", "S005", ".github/steps", "Missing x-review.md recap.",
                   "Add .github/steps/x-review.md and post it from the final workflow.")
    for name, sev in (("README.md", "error"), ("LICENSE", "warning"), (".gitignore", "info")):
        if not (root / name).exists():
            report.add(sev, "S006", name, f"Missing {name}.", "Copy it from the scaffold assets or exercise-template.")
    start = [w for w in workflows if w.number == 0]
    if not start:
        report.add("error", "S007", ".github/workflows", "Missing the Step 0 start workflow (0-start-exercise.yml).",
                   "Add .github/workflows/0-start-exercise.yml from the scaffold assets.")
    for wf in workflows:
        if not isinstance(wf.data, dict):
            continue
        if wf.number is None and wf.name.lower().startswith("step "):
            report.add("warning", "S008", wf.path.relative_to(root),
                       f"Workflow '{wf.name}' does not start with a digit, so Step 0 will not disable it.",
                       "Rename the file to start with its step number.")
        if wf.number is not None and not wf.name.lower().startswith("step "):
            report.add("warning", "S009", wf.path.relative_to(root),
                       "Filename starts with a digit but the workflow is not an exercise step; Step 0 will disable it.",
                       "Rename non-exercise workflows so they do not start with a digit.")


def check_workflows(root, steps, review, workflows, report):
    exercise = [w for w in workflows if w.number is not None]
    names = {w.name for w in workflows}
    # An unparsable step workflow still exists; avoid cascading "missing workflow" findings.
    names |= {f"Step {w.number}" for w in exercise if not isinstance(w.data, dict)}
    last_n = max((w.number for w in exercise), default=None)
    toolkit_refs: dict[str, list[str]] = {}
    file_set = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    posted: dict[str, list[tuple[Workflow, dict | None]]] = {}

    for wf in workflows:
        rel = wf.path.relative_to(root)
        if wf.error or not isinstance(wf.data, dict):
            reason = wf.error or ("the file is empty" if not wf.text.strip() else "it is not a mapping")
            report.add("error", "W001", rel, f"Workflow is not a valid workflow: {reason}.", "Fix the YAML syntax.")
            continue
        for m in PLACEHOLDER_RE.finditer(wf.text):
            report.add("error", "C008", rel, f"Unfilled placeholder '{m.group(0)}'.",
                       "Replace every template placeholder.", line_of(wf.text, m.group(0)))
            break
        if wf.number is not None:
            expected = f"Step {wf.number}"
            if not wf.name:
                report.add("error", "W002", rel, "Workflow has no name.", f"Set `name: {expected}`.")
            elif wf.name != expected:
                report.add("warning", "W002", rel, f"Workflow name '{wf.name}' does not match '{expected}'.",
                           f"Set `name: {expected}` so `gh workflow enable` targets resolve.")
        for target in wf.enables():
            if target not in names:
                report.add("error", "W003", rel, f"`gh workflow enable \"{target}\"` names a workflow that does not exist.",
                           "Point it at an existing `Step N` workflow name.", line_of(wf.text, target))
        collect_uses(wf, toolkit_refs, report, root)
        check_security(wf, report, root)
        check_permissions(wf, report, root)
        for job_id, job, step in wf.steps():
            uses = str(step.get("uses", ""))
            if uses.startswith("GrantBirki/comment"):
                with_ = step.get("with") if isinstance(step.get("with"), dict) else {}
                target = str(with_.get("file", ""))
                m = re.search(r"env\.([A-Z0-9_]+)", target)
                if m:
                    target = str(wf.env.get(m.group(1), ""))
                if target.startswith(".github/steps/"):
                    vars_ = with_.get("vars")
                    parsed = None
                    if isinstance(vars_, str):
                        try:
                            parsed = load_yaml(re.sub(r"\$\{\{.*?\}\}", "x", vars_))
                        except Exception:  # noqa: BLE001
                            parsed = {}
                    posted.setdefault(target, []).append((wf, parsed if isinstance(parsed, dict) else ({} if vars_ else None)))
        for key, value in wf.env.items():
            if isinstance(value, str) and value.startswith(".github/") and not (root / value).exists():
                report.add("error", "W004", rel, f"env {key} points to missing file {value}.",
                           "Fix the path or create the file.", line_of(wf.text, key))

        if wf.number is not None:
            check_triggers(wf, report, root, file_set)
            check_grading(wf, report, root)
        if wf.number == 0:
            if not wf.calls("start-exercise.yml"):
                report.add("error", "W010", rel, "Step 0 does not call the toolkit start-exercise.yml workflow.",
                           "Use the scaffold 0-start-exercise.yml template.")
            start_job = next((j for j in wf.jobs.values() if isinstance(j, dict) and "start-exercise.yml" in str(j.get("uses", ""))), None)
            if start_job is not None and "is_template" not in str(start_job.get("if", "")):
                report.add("error", "W011", rel, "Start job is not guarded with `!github.event.repository.is_template`.",
                           "Add the guard so the exercise never starts inside the template repository.")
            if "Step 1" not in wf.enables() and 1 in steps:
                report.add("error", "W012", rel, "Step 0 does not enable `Step 1`.", "Add `gh workflow enable \"Step 1\"`.")
        elif wf.number is not None and wf.number == last_n:
            if not wf.calls("finish-exercise.yml"):
                report.add("error", "W013", rel, "Final workflow does not call finish-exercise.yml.",
                           "Add the finish_exercise job from the N-step-final.yml template.")
            if wf.enables():
                report.add("warning", "W014", rel, "Final workflow enables another workflow.", "Only disable itself.")
            if review is not None and review.name not in wf.text:
                report.add("error", "W015", rel, f"Final workflow does not post {review.name}.",
                           "Set REVIEW_FILE to .github/steps/x-review.md and post it.")
        elif wf.number is not None:
            nxt = f"Step {wf.number + 1}"
            if nxt not in wf.enables():
                report.add("error", "W016", rel, f"Step {wf.number} does not enable `{nxt}`.",
                           f"End post_next_step_content with `gh workflow enable \"{nxt}\"`.")
            if wf.calls("finish-exercise.yml"):
                report.add("error", "W017", rel, "Intermediate step calls finish-exercise.yml.",
                           "Only the final step finishes the exercise.")
            nf = f"STEP_{wf.number + 2}_FILE"
            if wf.number + 2 in steps and nf in wf.env:
                report.add("warning", "W018", rel, f"Step {wf.number} references {nf}; it should post step {wf.number + 1}.",
                           f"Use STEP_{wf.number + 1}_FILE.")
    if exercise and sum(1 for w in exercise if w.calls("finish-exercise.yml")) > 1:
        report.add("error", "W019", ".github/workflows", "More than one workflow calls finish-exercise.yml.",
                   "Only the final step finishes the exercise.")
    expected_poster = {doc.path.relative_to(root).as_posix(): n - 1 for n, doc in steps.items()}
    if review is not None and last_n is not None:
        expected_poster[review.relative_to(root).as_posix()] = last_n
    for relp, want in expected_poster.items():
        posters = sorted({wf.number for wf, _ in posted.get(relp, []) if wf.number is not None})
        if not posted.get(relp):
            if relp.split("/")[-1][:1].isdigit():
                report.add("error", "W020", relp, "No workflow posts this step file.",
                           f"Post it from `Step {want}` via STEP_{want + 1}_FILE.")
            continue
        wrong = [p for p in posters if p != want]
        if wrong:
            report.add("error", "W028", relp, f"Posted by `Step {', Step '.join(map(str, wrong))}`; expected `Step {want}`.",
                       f"Each step file is posted by the previous step's workflow; this one belongs to `Step {want}`.")
        if len(posted[relp]) > 1:
            report.add("warning", "W029", relp, f"Posted {len(posted[relp])} times (by Steps {posters}).",
                       "Post each step file exactly once so learners never see it twice.")
    check_toolkit_refs(toolkit_refs, report)
    check_template_vars(root, steps, review, posted, report)


def collect_uses(wf, toolkit_refs, report, root):
    rel = wf.path.relative_to(root)
    entries = []
    for job in wf.jobs.values():
        if isinstance(job, dict) and job.get("uses"):
            entries.append((str(job["uses"]), None))
    for _, _, step in wf.steps():
        if step.get("uses"):
            entries.append((str(step["uses"]), step.get("with") if isinstance(step.get("with"), dict) else None))
    for uses, with_ in entries:
        if uses.startswith("./") or "@" not in uses:
            continue
        action, ref = uses.rsplit("@", 1)
        if action.startswith("skills/exercise-toolkit"):
            toolkit_refs.setdefault(ref, []).append(str(rel))
        if ref in ("main", "master", "HEAD", "latest"):
            report.add("error", "W021", rel, f"`{uses}` is pinned to a moving branch.",
                       "Pin a released tag (or a full commit SHA).", line_of(wf.text, uses))
        if action.startswith("tj-actions/changed-files"):
            report.add("warning", "W022", rel, "tj-actions/changed-files was compromised in March 2025 (CVE-2025-30066).",
                       "Prefer `git diff --name-only` with fetch-depth 0, or pin a reviewed full commit SHA.", line_of(wf.text, uses))
        if action == "skills/action-keyphrase-checker" and ref.startswith("v1"):
            report.add("info", "W023", rel, "action-keyphrase-checker v1 runs on Node 20.", "Use `@v2` (Node 24).",
                       line_of(wf.text, uses))
        if action == "GrantBirki/comment" and ref != "v2.1.1":
            report.add("info", "W024", rel, f"GrantBirki/comment@{ref} differs from the template and EMU strict allowlist pin v2.1.1.",
                       "Use v2.1.1 unless you have verified the newer major and your audience's allowlists.")
        if action == "actions/checkout" and with_ and with_.get("repository") == "skills/exercise-toolkit":
            toolkit_refs.setdefault(str(with_.get("ref", "<default branch>")), []).append(str(rel))


def check_toolkit_refs(toolkit_refs, report):
    if not toolkit_refs:
        return
    if len(toolkit_refs) > 1:
        detail = "; ".join(f"{ref}: {len(files)} use(s)" for ref, files in sorted(toolkit_refs.items()))
        report.add("error", "W025", ".github/workflows", f"Mixed exercise-toolkit refs ({detail}).",
                   "Use one release tag everywhere, including `ref:` of the toolkit checkout.")
    for ref in toolkit_refs:
        if ref == "<default branch>":
            report.add("error", "W026", ".github/workflows", "A toolkit checkout has no `ref:`.",
                       "Pin the checkout to the same tag as the reusable workflows.")
        elif re.fullmatch(r"v\d+\.\d+\.\d+", ref) and ref != KNOWN_GOOD_TOOLKIT:
            report.add("info", "W027", ".github/workflows", f"exercise-toolkit pinned to {ref}; verified version is {KNOWN_GOOD_TOOLKIT}.",
                       "Check the latest release and upgrade every reference together.")


def check_triggers(wf, report, root, file_set):
    rel = wf.path.relative_to(root)
    triggers = triggers_of(wf.data)
    if not triggers:
        report.add("error", "W030", rel, "Workflow has no `on:` triggers.", "Add the learner-action trigger.")
        return
    if wf.number == 0:
        push = triggers.get("push")
        if "push" not in triggers:
            report.add("warning", "W031", rel, "Step 0 has no `push` trigger, so copying the exercise will not start it.",
                       "Enable `push` on `main`, or tell learners to run the workflow manually.")
        elif isinstance(push, dict) and push.get("branches") and "main" not in as_list(push.get("branches")):
            report.add("warning", "W031", rel, "Step 0 push trigger does not include `main`.", "Trigger on pushes to main.")
        return
    if "pull_request_target" in triggers:
        report.add("warning", "W032", rel, "`pull_request_target` runs with write access in the base repository context.",
                   "Use `pull_request` for exercise grading.")
    if "issue_comment" in triggers and "pull_request" not in wf.text.split("issue_comment", 1)[-1]:
        report.add("info", "W033", rel, "`issue_comment` also fires for pull request comments.",
                   "Guard jobs with `!github.event.issue.pull_request` (or the reverse) as intended.")
    push = triggers.get("push")
    if "push" in triggers:
        cfg = push if isinstance(push, dict) else {}
        branches = [str(b) for b in as_list(cfg.get("branches"))]
        ignored = [str(b) for b in as_list(cfg.get("branches-ignore"))]
        paths = [str(p) for p in as_list(cfg.get("paths"))]
        hits_main = (not branches and "main" not in ignored) or any(glob_to_regex(b).match("main") for b in branches)
        guarded = has_initial_push_guard(wf)
        if hits_main and not paths and not guarded:
            report.add("error", "W034", rel, "`push` can fire on `main` without a `paths` filter; it will run when the exercise is copied.",
                       "Filter by branch or by paths of files the learner creates (see triggers reference).")
        if hits_main and paths and not guarded:
            existing = sorted({f for p in paths if not p.startswith("!") for f in file_set if glob_to_regex(p).match(f)})
            if existing:
                report.add("warning", "W035", rel,
                           f"`paths` filter matches files that already exist in the template ({', '.join(existing[:3])}); the copy push can trigger it early.",
                           "Filter on files the learner creates, or add an initial-commit guard.")


GUARD_PATTERNS = (
    re.compile(r"github\.event\.created\s*==\s*false"),
    re.compile(r"!\s*github\.event\.created\b"),
    re.compile(r"head_commit\.message\s*!=\s*['\"]Initial commit['\"]"),
    re.compile(r"github\.run_number\s*(?:!=\s*1\b|>\s*1\b|>=\s*2\b)"),
)


def has_initial_push_guard(wf) -> bool:
    """True when every job that starts the workflow has an `if:` that rejects the template-copy push.

    Reads parsed `if:` values, so comments cannot satisfy it, and recognizes only conditions that exclude the
    initial push (for example `github.event.created == false`), not ones that merely mention those fields.
    Jobs that `need` another job are skipped automatically when that job is skipped.
    """
    roots = [job for job in wf.jobs.values() if isinstance(job, dict) and not job.get("needs")]
    return bool(roots) and all(any(p.search(str(job.get("if", ""))) for p in GUARD_PATTERNS) for job in roots)


def check_grading(wf, report, root):
    rel = wf.path.relative_to(root)
    jobs = wf.jobs

    def with_of(step):
        value = step.get("with")
        return value if isinstance(value, dict) else {}

    grading_ids = [jid for jid, job in jobs.items() if isinstance(job, dict) and (
        jid == "check_step_work" or "step-results-table.md" in json.dumps(job.get("steps", []), default=str))]
    for jid in grading_ids:
        job = jobs[jid]
        steps = [s for s in as_list(job.get("steps")) if isinstance(s, dict)]
        job_text = json.dumps(steps, default=str)
        checks = [s for s in steps if s.get("continue-on-error") in (True, "true")]
        if not checks:
            report.add("warning", "W040", rel, f"Grading job `{jid}` has no checks with `continue-on-error: true`.",
                       "Keep each check independent so every result is reported.")
        fails = [s for s in steps if "exit 1" in str(s.get("run", "")) and "outcome" in str(s.get("if", ""))]
        if checks and not fails:
            report.add("error", "W041", rel, f"Grading job `{jid}` never fails, so wrong work still advances.",
                       "End with `if: contains(steps.*.outcome, 'failure')` and `run: exit 1`.")
        table = next((s for s in steps if "step-results-table.md" in str(with_of(s).get("file", ""))), None)
        if table is not None:
            vars_ = str(with_of(table).get("vars", ""))
            for check in checks:
                cid = check.get("id")
                # A step whose outputs feed a later check (for example wait-for-workflow) is not a check itself.
                if cid and f"steps.{cid}." not in vars_ and f"steps.{cid}.outputs" not in job_text:
                    report.add("warning", "W042", rel, f"Check `{cid}` is not reported in results_table.",
                               "Add a learner-readable row for every check.")
            if "step_number" not in vars_:
                report.add("warning", "W043", rel, "results_table comment does not pass `step_number`.", "Pass step_number.")
        for s in steps:
            if str(s.get("uses", "")).startswith("peter-evans/find-comment"):
                if "comment-author" not in with_of(s):
                    report.add("warning", "W044", rel, "find-comment has no `comment-author` filter; it can target the learner's comment.",
                               "Add `comment-author: github-actions[bot]`.", line_of(wf.text, "peter-evans/find-comment"))
            if str(s.get("uses", "")).startswith("skills/exercise-toolkit/actions/wait-for-workflow"):
                sid = s.get("id")
                if not sid or not re.search(rf"steps\.{re.escape(str(sid))}\.outputs\.conclusion", job_text):
                    report.add("error", "W046", rel, "wait-for-workflow succeeds even when the awaited run fails; its `conclusion` output is never checked.",
                               "Add a check step that fails unless `steps.<id>.outputs.conclusion == 'success'` (see grading patterns).",
                               line_of(wf.text, "wait-for-workflow"))
        for downstream in ("post_next_step_content", "post_review_content"):
            job_d = jobs.get(downstream)
            if isinstance(job_d, dict) and jid not in as_list(job_d.get("needs")):
                report.add("error", "W045", rel, f"`{downstream}` does not need `{jid}`; failed grading will still advance the learner.",
                           f"Set `needs: [find_exercise, {jid}]`.", line_of(wf.text, f"{downstream}:"))


def check_permissions(wf, report, root):
    rel = wf.path.relative_to(root)
    top = wf.data.get("permissions") if isinstance(wf.data, dict) else None
    jobs = wf.jobs
    job_perms = [isinstance(j, dict) and "permissions" in j for j in jobs.values()]
    if top is None and not all(job_perms):
        report.add("warning", "W050", rel, "Permissions are not declared for every job; defaults are read-only in many organizations.",
                   "Declare `permissions: {}` at the top and grant each job what it needs.")
    if top == "write-all":
        report.add("warning", "W051", rel, "`permissions: write-all` grants every scope.", "Grant per-job least privilege.")
    if isinstance(top, dict) and str(top.get("actions")) == "write":
        for jid, job in jobs.items():
            if isinstance(job, dict) and jid == "check_step_work" and "permissions" not in job:
                report.add("info", "W052", rel, "The learner-triggered grading job inherits `actions: write` from the workflow.",
                           "Least privilege: `permissions: {}` at the top and per-job grants (see the framework contract).")


def check_security(wf, report, root):
    rel = wf.path.relative_to(root)
    for job_id, job, step in wf.steps():
        sources = [str(step.get("run", ""))]
        with_ = step.get("with") if isinstance(step.get("with"), dict) else {}
        if str(step.get("uses", "")).startswith("actions/github-script"):
            sources.append(str(with_.get("script", "")))
        for src in sources:
            m = INJECTION_RE.search(src)
            if m:
                report.add("error", "W060", rel, f"Untrusted `{m.group(1)}` is interpolated into a script (job `{job_id}`).",
                           "Pass it through `env:` and reference the environment variable instead.", line_of(wf.text, m.group(0)))


def check_template_vars(root, steps, review, posted, report):
    """GrantBirki/comment renders every posted file with Nunjucks; only `vars:` supplies values."""
    docs = {d.path.relative_to(root).as_posix(): d.text for d in steps.values()}
    if review is not None:
        docs[review.relative_to(root).as_posix()] = read(review)
    for relp, text in docs.items():
        if not posted.get(relp):
            continue
        clean = without_raw(text)
        defined = set(re.findall(r"\{%-?\s*(?:set|for)\s+([A-Za-z_]\w*)", clean))
        defined |= set(re.findall(r"\{%-?\s*for\s+[A-Za-z_]\w*\s*,\s*([A-Za-z_]\w*)", clean))
        used = set(NUNJUCKS_VAR_RE.findall(clean)) - defined - {"loop"}
        if "${{" in clean:
            report.add("error", "W072", relp, "`${{ ... }}` outside `{% raw %}` is mangled: posted step files are always rendered with Nunjucks.",
                       "Wrap Actions expressions in {% raw %}...{% endraw %}.", line_of(text, "${{"))
        for wf, vars_ in posted.get(relp, []):
            wrel = wf.path.relative_to(root).as_posix()
            if vars_ is None and used:
                report.add("error", "W070", relp, f"Uses {{{{ {sorted(used)[0]} }}}} but {wrel} posts it without `vars:`, so it renders empty.",
                           "Pass `vars:` (login, full_repo_name, ...) when posting this file.")
            elif vars_ is not None:
                missing = sorted(v for v in used if v not in vars_)
                if missing:
                    report.add("warning", "W071", relp, f"Variables {missing} are not passed by {wrel}; they render empty.",
                               "Add them to `vars:` or remove them.")


def check_steps(root, steps, review, report):
    for n, doc in sorted(steps.items()):
        rel = doc.path.relative_to(root)
        text = doc.text
        if PLACEHOLDER_RE.search(text):
            m = PLACEHOLDER_RE.search(text)
            report.add("error", "C008", rel, f"Unfilled placeholder '{m.group(0)}'.", "Replace every template placeholder.",
                       line_of(text, m.group(0)))
        if doc.heading_number is None:
            report.add("error", "C001", rel, "Missing `## Step N: <title>` heading.", f"Start the file with `## Step {n}: ...`.")
        elif doc.heading_number != n:
            report.add("warning", "C001", rel, f"Heading says Step {doc.heading_number} but the file is step {n}.",
                       "Make the heading number match the filename.")
        if doc.theory_count == 0:
            report.add("warning", "C002", rel, "No `### 📖 Theory:` section.",
                       "Add one short awareness-level theory section that the activity needs.")
        elif doc.theory_count > 1:
            report.add("info", "C002", rel, f"{doc.theory_count} Theory sections; the template uses exactly one.",
                       "Merge them, or split the step if it teaches two concepts.")
        if doc.theory_count and doc.theory_words > 400:
            report.add("warning", "C005", rel, f"Theory is {doc.theory_words} words; awareness-level theory is usually far shorter.",
                       "Keep only what the activity needs and link to GitHub Docs for depth (coherence).")
        elif doc.theory_count and doc.theory_words > 250:
            report.add("info", "C005", rel, f"Theory is {doc.theory_words} words (heuristic ceiling about 250).",
                       "Check every sentence is needed for this step's activity.")
        elif doc.theory_count and doc.theory_words < 15:
            report.add("warning", "C005", rel, f"Theory is only {doc.theory_words} words.", "Give the activity a real conceptual anchor.")
        acts = doc.activities
        if not acts:
            report.add("warning", "C003", rel, "No `### ⌨️ Activity` section.", "Add at least one hands-on activity.")
        if len(acts) > 3:
            report.add("warning", "C003", rel, f"{len(acts)} activities; steps should have one to three.", "Split the step.")
        numbered = [a.number for a in acts]
        if len(acts) == 1 and numbered[0] is not None:
            report.add("info", "C004", rel, "A lone activity is numbered.", "Use `### ⌨️ Activity: <title>`.")
        if len(acts) > 1 and numbered != list(range(1, len(acts) + 1)):
            report.add("info", "C004", rel, f"Activity numbering is {numbered}; numbering several activities helps orientation.",
                       "Use `Activity 1`, `Activity 2`, ... when a step has several.")
        step_has_trouble = any(a.has_trouble for a in acts)
        for a in acts:
            if a.emoji is None:
                report.add("info", "C004", rel, f"Activity heading at line {a.start} has no ⌨️ emoji.",
                           "Use `### ⌨️ Activity:` for consistent signaling.", a.start)
            if a.level == 2:
                report.add("info", "C004", rel, f"Activity heading at line {a.start} is a level-2 heading.",
                           "Use `###` so the step keeps one `##` heading.", a.start)
            if not a.title:
                report.add("warning", "C004", rel, f"Activity at line {a.start} has no title.", "Give it a verb + object title.", a.start)
            if not a.has_trouble:
                sev = "info" if step_has_trouble else "warning"
                report.add(sev, "C006", rel, f"Activity '{a.title or a.start}' has no `Having trouble? 🤷` block of its own.",
                           "Put likely mistakes and recovery hints right after each activity.", a.start)
            if a.instructions == 0:
                report.add("warning", "C007", rel, f"Activity '{a.title or a.start}' has no numbered instructions.",
                           "Write numbered `1.` steps.", a.start)
            if a.instructions > 12:
                report.add("warning", "C007", rel, f"Activity '{a.title}' has {a.instructions} instructions.",
                           "Split it into smaller activities (segmenting).", a.start)
            if a.max_depth > 2:
                report.add("warning", "C007", rel, f"Activity '{a.title}' nests instructions {a.max_depth} levels deep.",
                           "Keep instructions to two levels.", a.start)
            for ln, restarts in a.list_breaks:
                if restarts:
                    report.add("warning", "C009", rel, f"Line {ln} is not indented, so the numbered list restarts at 1 after it.",
                               "Indent content between instructions by three spaces.", ln)
                else:
                    report.add("info", "C009", rel, f"Line {ln} splits the numbered list (explicit numbers hide the restart).",
                               "Indent content between instructions by three spaces.", ln)
        if acts and not re.search(r"\bMona\b|share the next|next lesson|check your work", "\n".join(acts[-1].lines), re.IGNORECASE):
            report.add("info", "C010", rel, "The last activity does not tell the learner to wait for Mona's feedback.",
                       "End with: Wait a moment for Mona to check your work, provide feedback, and share the next lesson.")
        check_markup(root, rel, text, report)
    if review is not None:
        text = read(review)
        rel = review.relative_to(root)
        if PLACEHOLDER_RE.search(text):
            report.add("error", "C008", rel, "Unfilled placeholder in the review.", "Replace every template placeholder.")
        check_markup(root, rel, text, report)
        if not re.search(r"what'?s next", text, re.IGNORECASE):
            report.add("info", "C011", rel, "Review has no `What's next?` section.", "Point to the next exercise and docs.")
        if not re.search(r"<summary>[^<]*\?|check your understanding|reflect", text, re.IGNORECASE):
            report.add("info", "L005", rel, "Review has no retrieval or reflection prompt.",
                       "Add one or two recall questions with collapsible answers (retrieval practice).")


def check_markup(root, rel, text, report):
    lines = text.splitlines()
    mask = code_mask(lines)
    body = "\n".join(line for line, m in zip(lines, mask) if not m)
    for tag in IMG_TAG_RE.findall(body):
        src_m = re.search(ATTR_RE.format("src"), tag)
        alt_m = re.search(ATTR_RE.format("alt"), tag)
        src = src_m.group(1) if src_m else ""
        check_image(root, rel, src, alt_m.group(1) if alt_m else None, text, report)
        if not re.search(r"\b(width|height)\s*=", tag):
            report.add("info", "C013", rel, f"Image {src} has no width or height.", "Set a width so it does not dominate the comment.",
                       line_of(text, src))
    for alt, src in IMG_MD_RE.findall(body):
        check_image(root, rel, src, alt, text, report)
    for label, href in LINK_MD_RE.findall(body):
        if label.strip().lower() in VAGUE_LINK_TEXT:
            report.add("info", "C014", rel, f"Link text '{label}' does not describe its destination.",
                       "Use descriptive link text (accessibility).", line_of(text, f"[{label}]"))
        if rel.parts[0] == ".github" and not re.match(r"^(https?:|mailto:|#|/|\{\{|\.\./images/)", href):
            report.add("warning", "C015", rel, f"Relative link `{href}` resolves against the issue URL and breaks in comments.",
                       "Use https://github.com/{{ full_repo_name }}/... instead.", line_of(text, href))
    for idx, line in enumerate(lines, start=1):
        if mask[idx - 1]:
            continue
        if re.match(r"^\s+>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", line, re.IGNORECASE):
            report.add("warning", "C016", rel, "Indented GitHub alert will not render inside a list.",
                       "Use `> 💡 **Tip:** ...` style blockquotes inside lists.", idx)
        if re.search(r"\brepo\b", line) and not re.search(r"`[^`]*\brepo\b[^`]*`|/repo|repo=|\{\{", line):
            report.add("info", "C017", rel, "Shorthand 'repo'; GitHub Skills style spells out 'repository'.", "Write 'repository'.", idx)
            break


def check_image(root, rel, src, alt, text, report):
    if not src or src.startswith(("http://", "https://", "{{", "data:")):
        if alt is not None and not alt.strip() and "img.shields.io" not in src:
            report.add("warning", "C012", rel, f"Image {src[:60]} has empty alt text.", "Describe what the image shows.",
                       line_of(text, src) if src else None)
        return
    if alt is None or not alt.strip():
        report.add("warning", "C012", rel, f"Image {src} has no alt text.", "Describe what the image shows.", line_of(text, src))
    if rel.parts[0] == ".github":
        if not src.startswith("../images/"):
            report.add("error", "C018", rel, f"Image `{src}` is not referenced as ../images/<file>; it will not be rewritten.",
                       "Store it in .github/images and reference it as ../images/<file>.", line_of(text, src))
            return
        name = src[len("../images/"):].split("?")[0].split("#")[0]
        if re.search(r"[\s'\"()]", name):
            report.add("error", "C019", rel, f"Image name `{name}` has spaces, quotes or parentheses.", "Rename the file.")
        image = root / ".github" / "images" / name
        if not image.exists():
            report.add("error", "C020", rel, f"Image `{src}` does not exist in .github/images.", "Add the file or fix the path.",
                       line_of(text, src))
        elif not exact_case_exists(root / ".github" / "images", name):
            report.add("error", "C021", rel, f"Image `{src}` differs from the file name only by letter case; GitHub URLs are case-sensitive.",
                       "Match the file name's case exactly.", line_of(text, src))


def exact_case_exists(base: Path, relative: str) -> bool:
    """Path.exists() ignores case on Windows and macOS; GitHub does not."""
    current = base
    for part in Path(relative).parts:
        try:
            entries = {entry.name for entry in current.iterdir()}
        except OSError:
            return False
        if part not in entries:
            return False
        current = current / part
    return True


def check_readme(root, steps, report, template_repo):
    path = root / "README.md"
    if not path.exists():
        return
    text = read(path)
    if PLACEHOLDER_RE.search(text):
        m = PLACEHOLDER_RE.search(text)
        report.add("error", "C008", "README.md", f"Unfilled placeholder '{m.group(0)}'.", "Replace every template placeholder.",
                   line_of(text, m.group(0)))
    for label in ("Who is this for", "What you'll learn", "What you'll build", "Prerequisites", "How long"):
        if label.lower() not in text.lower():
            report.add("warning", "R001", "README.md", f"Welcome section is missing **{label}**.", "Follow the template welcome block.")
    badges = re.findall(r"\]\((https://github\.com/new\?[^)\s]+)\)", text)
    copy_badges = text.count("Copy%20Exercise")
    if copy_badges == 0 or not badges:
        report.add("error", "R002", "README.md", "No Copy Exercise button.", "Add the template's Copy Exercise badge.")
    else:
        if copy_badges > 1:
            report.add("warning", "R002", "README.md", "More than one Copy Exercise button.", "Keep exactly one.")
        q = {k: v[0] for k, v in parse_qs(urlparse(badges[0]).query).items()}
        owner, name = q.get("template_owner", ""), q.get("template_name", "")
        if q.get("owner") != "@me":
            report.add("warning", "R003", "README.md", "Copy Exercise link does not preselect the learner (`owner=%40me`).", "Add owner=%40me.")
        if name and q.get("name") != f"skills-{name}":
            report.add("warning", "R003", "README.md", f"Suggested copy name is '{q.get('name')}', expected 'skills-{name}'.",
                       "Set name=skills-<template_name>.")
        if not q.get("description", "").startswith("Exercise:"):
            report.add("info", "R003", "README.md", "Copy description does not start with 'Exercise:'.", "Use description=Exercise:+<Title>.")
        if "visibility" not in q:
            report.add("info", "R003", "README.md", "Copy link does not set visibility.", "Add visibility=public.")
        slug = template_repo or repo_slug_from_git(root)
        if slug and owner and name and f"{owner}/{name}".lower() != slug.lower():
            report.add("error", "R004", "README.md", f"Copy Exercise points to {owner}/{name}, but this repository is {slug}.",
                       "Fix template_owner and template_name.")
        elif slug and f"{owner}/{name}" != slug and f"{owner}/{name}".lower() == slug.lower():
            report.add("info", "R004", "README.md", "Copy Exercise owner/name differ from the repository only in case.", "Match the case exactly.")
    if "&copy;" not in text and "©" not in text:
        report.add("info", "R005", "README.md", "No copyright footer.", "End with the template footer (copyright, Code of Conduct, license).")
    objectives = re.search(r"In this exercise, you will:\s*\n((?:\s*\d+\.\s+.*\n?)+)", text)
    if objectives:
        items = re.findall(r"^\s*\d+\.\s+(.*)$", objectives.group(1), re.MULTILINE)
        if steps and len(items) != len(steps):
            report.add("info", "L001", "README.md", f"{len(items)} objectives listed for {len(steps)} steps.",
                       "Align one observable objective per step (constructive alignment).")
        for item in items:
            first = item.strip().lower()
            if first.startswith(VAGUE_VERBS):
                report.add("info", "L002", "README.md", f"Objective '{item.strip()[:60]}' is not observable.",
                           "Start with an observable verb: create, configure, review, explain, compare...")


def learning_heuristics(steps, report, root):
    if len(steps) >= 2 and 1 in steps:
        sizes = {n: sum(a.instructions for a in d.activities) for n, d in steps.items()}
        others = [v for n, v in sizes.items() if n != 1]
        if others and sizes[1] > 1.5 * statistics.median(others) and sizes[1] > 6:
            report.add("info", "L003", steps[1].path.relative_to(root),
                       f"Step 1 has {sizes[1]} instructions vs a median of {statistics.median(others):g} in later steps.",
                       "Make the first step the easiest to build confidence (early success).")


def readme_minutes(root: Path) -> int | None:
    """Minutes promised by the README 'How long' line, if it can be read."""
    path = root / "README.md"
    if not path.exists():
        return None
    m = re.search(r"How long\*?\*?:?(.*)", read(path), re.IGNORECASE)
    if not m:
        return None
    line = m.group(1).lower()
    num = re.search(r"(\d+)\s*(?:-\s*\d+\s*)?(minute|min|hour|hr)", line)
    if num:
        return int(num.group(1)) * (60 if num.group(2).startswith("h") else 1)
    if re.search(r"half an hour", line):
        return 30
    if re.search(r"\b(one|an|a)\s+hour", line):
        return 60
    return None


def estimate(steps, report, root):
    rows, total = [], 0.0
    for n, d in sorted(steps.items()):
        instr = sum(a.instructions for a in d.activities)
        minutes = d.total_words / READING_WPM + instr * MINUTES_PER_INSTRUCTION + MINUTES_FEEDBACK_WAIT
        total += minutes
        rows.append({"step": n, "words": d.total_words, "theory_words": d.theory_words,
                     "activities": len(d.activities), "instructions": instr, "est_minutes": round(minutes, 1)})
    promised = readme_minutes(root)
    report.metrics = {"steps": len(steps), "per_step": rows, "estimated_learner_minutes": round(total, 1),
                      "readme_promised_minutes": promised, "yaml_engine": YAML_ENGINE}
    if promised and total > promised * 1.25:
        report.add("warning", "L004", "README.md", f"README promises {promised} minutes; the content heuristic estimates about {total:.0f}.",
                   "Trim or split the exercise, or state a realistic time. Confirm with a walkthrough test or real learners.")
    elif total > 60:
        report.add("info", "L004", ".github/steps", f"Estimated learner time is about {total:.0f} minutes.",
                   "Many learners drop off after 30 to 45 minutes (exercise-creator observation). Consider splitting.")


def online_checks(root, report):
    if not shutil.which("git"):
        report.add("info", "O001", "-", "git not found; skipped online checks.")
        return
    wf_dir = root / ".github" / "workflows"
    texts = "\n".join(read(p) for p in wf_dir.glob("*.y*ml")) if wf_dir.is_dir() else ""
    refs = set(re.findall(r"skills/exercise-toolkit/[^@\s]+@([\w.\-]+)", texts))
    for ref in sorted(refs):
        if re.fullmatch(r"[0-9a-f]{40}", ref):
            if not shutil.which("gh"):
                report.add("info", "O001", ".github/workflows", f"Cannot verify commit pin {ref[:12]} without gh.")
                continue
            out = subprocess.run(["gh", "api", f"repos/skills/exercise-toolkit/commits/{ref}", "--jq", ".sha"],
                                 capture_output=True, text=True, timeout=30)
            if out.stdout.strip() != ref:
                report.add("error", "O002", ".github/workflows", f"exercise-toolkit commit {ref[:12]} was not found.",
                           "Pin a published release tag or an existing full commit SHA.")
            continue
        out = subprocess.run(["git", "ls-remote", "--tags", "https://github.com/skills/exercise-toolkit", f"refs/tags/{ref}"],
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and not out.stdout.strip():
            report.add("error", "O002", ".github/workflows", f"exercise-toolkit tag {ref} does not exist.", "Pin a published release tag.")
    if shutil.which("gh"):
        out = subprocess.run(["gh", "release", "view", "--repo", "skills/exercise-toolkit", "--json", "tagName", "--jq", ".tagName"],
                             capture_output=True, text=True, timeout=30)
        latest = out.stdout.strip()
        tags = {r for r in refs if not re.fullmatch(r"[0-9a-f]{40}", r)}
        if latest and tags and latest not in tags:
            report.add("info", "O003", ".github/workflows", f"exercise-toolkit {latest} is available (pinned: {', '.join(sorted(tags))}).",
                       "Review its release notes and upgrade every reference together.")


# --------------------------------------------------------------------------- output


def render(report: Report, fmt: str) -> str:
    order = sorted(report.findings, key=lambda f: (SEVERITIES.index(f.severity), f.path, f.line or 0))
    if fmt == "json":
        return json.dumps({"root": report.root, "metrics": report.metrics,
                           "summary": {LABELS[s]: report.count(s) for s in SEVERITIES},
                           "findings": [asdict(f) for f in order]}, indent=2)
    md = fmt == "markdown"
    out = [f"# Exercise validation: {report.root}" if md else f"Exercise validation: {report.root}"]
    out.append(("" if md else "") + "Summary: " + ", ".join(f"{LABELS[s]} {report.count(s)}" for s in SEVERITIES))
    for sev in SEVERITIES:
        items = [f for f in order if f.severity == sev]
        out.append("")
        out.append(f"## {LABELS[sev]} ({len(items)})" if md else f"{LABELS[sev].upper()} ({len(items)})")
        if not items:
            out.append("None")
        for f in items:
            loc = f"{f.path}:{f.line}" if f.line else f.path
            fix = f" Fix: {f.fix}" if f.fix else ""
            out.append(f"- [{f.rule}] `{loc}` {f.message}{fix}" if md else f"  [{f.rule}] {loc}: {f.message}{fix}")
    m = report.metrics
    if m.get("per_step"):
        out.append("")
        out.append("## Metrics" if md else "METRICS")
        out.append("| Step | Words | Theory words | Activities | Instructions | Est. minutes |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        for r in m["per_step"]:
            out.append(f"| {r['step']} | {r['words']} | {r['theory_words']} | {r['activities']} | {r['instructions']} | {r['est_minutes']} |")
        out.append(f"Estimated learner time: about {m['estimated_learner_minutes']:.0f} minutes (heuristic; confirm with a walkthrough test).")
    out.append(f"YAML engine: {m.get('yaml_engine', YAML_ENGINE)}")
    return "\n".join(out)


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Validate a GitHub Skills exercise repository.")
    ap.add_argument("repo", nargs="?", default=".", help="exercise repository root (default: .)")
    ap.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    ap.add_argument("--strict", action="store_true", help="exit 1 on important findings too")
    ap.add_argument("--online", action="store_true", help="verify toolkit tags and latest release (needs network)")
    ap.add_argument("--template-repo", help="OWNER/NAME the exercise is published as (default: git origin)")
    args = ap.parse_args(argv)
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    report = Report(root=str(root))
    steps, review, workflows = load(root, report)
    check_structure(root, steps, review, workflows, report)
    check_workflows(root, steps, review, workflows, report)
    check_steps(root, steps, review, report)
    check_readme(root, steps, report, args.template_repo)
    learning_heuristics(steps, report, root)
    estimate(steps, report, root)
    if args.online:
        online_checks(root, report)
    print(render(report, args.format))
    if report.count("error") or (args.strict and report.count("warning")):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
