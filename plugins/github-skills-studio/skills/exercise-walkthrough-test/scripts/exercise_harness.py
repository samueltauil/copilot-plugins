#!/usr/bin/env python3
"""Test harness for walking through a GitHub Skills exercise as a learner.

Wraps the GitHub CLI (`gh`) so an agent can create a disposable learner copy,
observe Mona's comments and workflow runs, measure feedback latency, lint the
rendered comments, and clean up. UI fidelity is checked separately with Computer
Use; this script provides the ground truth about repository state.

Only the Python standard library and an authenticated `gh` are required.

Commands (run with --help for options):
  now                     print the current UTC timestamp (use before an action)
  preflight               check gh, auth scopes, template (and its commit) and owner
  create                  create a learner copy from the template (needs --yes)
  wait-start              wait for Step 0 to open the issue and post step 1
  status                  current step, enabled workflows, recent runs, comments
  comments                list exercise-issue comments (optionally full bodies)
  wait-step               after an action, wait for advance, failed check, error or no run
  lint-comments           check rendered comments for template and markup bugs
  timeline                chronological runs and comments with latencies
  runs                    recent workflow runs, optionally failed logs
  codespaces              list codespaces created for the learner copy
  cleanup                 archive or delete the copy, optionally its codespaces (needs --yes)

Exit status: 0 ok, 1 check failed or timeout, 2 usage or environment error,
3 confirmation required.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

BOT = "github-actions[bot]"
CLOCK_SKEW = timedelta(seconds=10)
STEP_RE = re.compile(r"^##\s+Step\s+(\d+)\b", re.MULTILINE)
RESULT_RE = re.compile(r"^##\s+Step\s+(\d+)\s+-\s+(Passed|Fail)", re.MULTILINE)
REVIEW_RE = re.compile(r"^##\s+Review\b", re.MULTILINE)
STEP_WORKFLOW_RE = re.compile(r"^Step \d+$")


class HarnessError(RuntimeError):
    pass


# --------------------------------------------------------------------------- utils


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_since(value: str | None) -> datetime | None:
    """Parse a user-supplied timestamp; it must carry a timezone so it compares with GitHub's UTC times."""
    if not value:
        return None
    try:
        parsed = parse_ts(value)
    except ValueError as exc:
        raise HarnessError(f"--since '{value}' is not an ISO timestamp; use the output of `now`") from exc
    if parsed.tzinfo is None:
        raise HarnessError(f"--since '{value}' has no timezone; use the output of `now` (UTC, ending in Z)")
    return parsed


def iso(dt: datetime | None) -> str | None:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def secs(a: datetime | None, b: datetime | None) -> float | None:
    return round((b - a).total_seconds(), 1) if a and b else None


def gh(*args: str, check: bool = True) -> str:
    if not shutil.which("gh"):
        raise HarnessError("GitHub CLI (gh) not found. Install it from https://cli.github.com/")
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and proc.returncode != 0:
        raise HarnessError(f"gh {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def gh_json(*args: str):
    out = gh(*args)
    return json.loads(out) if out.strip() else None


def gh_lines(*args: str) -> list:
    return [json.loads(line) for line in gh(*args).splitlines() if line.strip()]


def emit(data, as_json: bool, text: str | None = None):
    if as_json:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(text if text is not None else json.dumps(data, indent=2, default=str))


# --------------------------------------------------------------------------- model


def find_issue(repo: str, title_text: str = "Exercise") -> dict | None:
    """Mirror find-exercise-issue.yml: newest issue (any state) whose title contains the text."""
    issues = gh_json("issue", "list", "-R", repo, "--state", "all", "--limit", "50",
                     "--json", "number,title,state,url,createdAt") or []
    matches = [i for i in issues if title_text in i["title"]]
    matches.sort(key=lambda i: i["createdAt"], reverse=True)
    return matches[0] if matches else None


def comments(repo: str, number: int, html: bool = False) -> list[dict]:
    accept = ["-H", "Accept: application/vnd.github.full+json"] if html else []
    raw = gh_lines("api", *accept, f"repos/{repo}/issues/{number}/comments", "--paginate", "--jq", ".[] | tojson")
    out = []
    for c in raw:
        body = c.get("body") or ""
        steps = [int(n) for n in STEP_RE.findall(body)]
        results = RESULT_RE.findall(body)
        out.append({
            "id": c["id"],
            "author": c["user"]["login"],
            "created_at": c["created_at"],
            "updated_at": c["updated_at"],
            "url": c["html_url"],
            "kind": classify(body, steps, results),
            "step": steps[0] if steps else (int(results[0][0]) if results else None),
            "body": body,
            "body_html": c.get("body_html"),
        })
    return out


def classify(body: str, steps: list[int], results: list) -> str:
    if results:
        return "result-pass" if results[0][1] == "Passed" else "result-fail"
    if steps:
        return "step-content"
    if REVIEW_RE.search(body):
        return "review"
    low = body.lower()
    if "watch your progress" in low:
        return "watching"
    if "let's see if i have some feedback" in low or "looks like you are making progress" in low:
        return "checking"
    if "preparing content for step" in low:
        return "step-finished"
    if "let's do a quick review" in low:
        return "lesson-review"
    if "you finished the exercise" in low:
        return "finished"
    if "made a mistake or skipped a step" in low:
        return "mistake"
    return "other"


def workflows(repo: str) -> list[dict]:
    data = gh_json("api", f"repos/{repo}/actions/workflows", "--paginate") or {}
    return [{"name": w["name"], "path": w["path"], "state": w["state"], "id": w["id"]} for w in data.get("workflows", [])]


def runs(repo: str, limit: int = 20) -> list[dict]:
    return gh_json("run", "list", "-R", repo, "--limit", str(limit), "--json",
                   "databaseId,workflowName,event,status,conclusion,createdAt,updatedAt,url,headBranch,displayTitle") or []


def current_step(wfs: list[dict]) -> int | None:
    active = sorted(int(m.group(1)) for w in wfs if w["state"] == "active"
                    for m in [re.match(r"^Step (\d+)$", w["name"])] if m)
    return active[0] if active else None


# --------------------------------------------------------------------------- commands


def cmd_now(args):
    print(iso(utcnow()))
    return 0


def template_info(template: str) -> dict:
    tpl = gh_json("api", f"repos/{template}")
    sha = gh("api", f"repos/{template}/commits/{tpl['default_branch']}", "--jq", ".sha").strip()
    return {"full_name": tpl["full_name"], "is_template": tpl["is_template"], "visibility": tpl["visibility"],
            "default_branch": tpl["default_branch"], "head_sha": sha}


def cmd_preflight(args):
    report, ok = {}, True
    report["gh_version"] = gh("--version").splitlines()[0]
    user = gh_json("api", "user")
    report["user"] = user["login"]
    headers = gh("api", "-i", "user")
    scope_line = next((line for line in headers.splitlines() if line.lower().startswith("x-oauth-scopes:")), "")
    scopes = [s.strip() for s in scope_line.split(":", 1)[1].split(",")] if scope_line else []
    report["token_scopes"] = scopes or "fine-grained or unknown"
    if scopes:
        for needed in ("repo", "workflow"):
            if needed not in scopes:
                ok = False
                report.setdefault("problems", []).append(f"missing '{needed}' scope: gh auth refresh -h github.com -s {needed}")
        if "delete_repo" not in scopes:
            report.setdefault("notes", []).append("no 'delete_repo' scope: cleanup can archive but not delete "
                                                  "(gh auth refresh -h github.com -s delete_repo)")
        if "codespace" not in scopes:
            report.setdefault("notes", []).append("no 'codespace' scope: codespaces cannot be listed or deleted "
                                                  "(gh auth refresh -h github.com -s codespace)")
    if args.template:
        report["template"] = template_info(args.template)
        if not report["template"]["is_template"]:
            ok = False
            report.setdefault("problems", []).append(f"{args.template} is not marked as a template repository")
        report.setdefault("notes", []).append(
            f"copies are made from {report['template']['default_branch']} at {report['template']['head_sha'][:12]}; "
            "compare it with the reviewed commit (git rev-parse HEAD)")
    if args.owner and args.owner != report["user"]:
        org = subprocess.run(["gh", "api", f"user/memberships/orgs/{args.owner}"], capture_output=True, text=True)
        if org.returncode != 0:
            ok = False
            report.setdefault("problems", []).append(f"you are not a member of organization '{args.owner}'")
        else:
            report["owner"] = {"org": args.owner, "role": json.loads(org.stdout).get("role")}
    report["ok"] = ok
    emit(report, True)
    return 0 if ok else 1


def cmd_create(args):
    tpl = template_info(args.template)
    if args.visibility == "public" and tpl["visibility"] != "public":
        raise HarnessError(f"refusing to make a public copy of the {tpl['visibility']} template {args.template}; "
                           "use --visibility private (or internal) so its content stays private")
    stamp = utcnow().strftime("%Y%m%d-%H%M")
    template_name = args.template.split("/", 1)[1]
    name = args.name or f"skills-{template_name}-wt-{stamp}"
    repo = f"{args.owner}/{name}"
    command = ["repo", "create", repo, "--template", args.template, f"--{args.visibility}"]
    if not args.yes:
        emit({"confirmation_required": True, "repo": repo, "command": "gh " + " ".join(command),
              "template_commit": tpl["head_sha"],
              "consequence": f"creates a {args.visibility} repository {repo} from {args.template}@{tpl['head_sha'][:12]} "
                             "and starts the exercise workflows"
                             + ("; private and internal copies use the owner's Actions minutes" if args.visibility != "public" else "")},
             True)
        return 3
    started = utcnow()
    gh(*command)
    emit({"repo": repo, "url": f"https://github.com/{repo}", "visibility": args.visibility,
          "template_commit": tpl["head_sha"], "requested_at": iso(started)}, True)
    return 0


def cmd_wait_start(args):
    deadline = time.monotonic() + args.timeout
    repo_info = gh_json("api", f"repos/{args.repo}")
    created = parse_ts(repo_info["created_at"])
    issue, step1 = None, None
    while time.monotonic() < deadline:
        issue = issue or find_issue(args.repo, args.title_text)
        if issue:
            cs = comments(args.repo, issue["number"])
            step1 = next((c for c in cs if c["author"] == BOT and c["kind"] == "step-content"), None)
            if step1:
                break
        failed = [r for r in runs(args.repo, 5) if r["workflowName"] == "Step 0" and r["conclusion"] == "failure"]
        if failed:
            emit({"outcome": "error", "reason": "Step 0 failed", "run": failed[0]["url"]}, True)
            return 1
        time.sleep(args.interval)
    if not step1:
        emit({"outcome": "timeout", "issue": issue, "waited_s": args.timeout,
              "hint": "Check the Actions tab: is Actions enabled for this owner, and did Step 0 trigger on push?"}, True)
        return 1
    issue_at = parse_ts(issue["createdAt"])
    step1_at = parse_ts(step1["created_at"])
    emit({"outcome": "started", "issue": issue["url"], "issue_number": issue["number"],
          "repo_created_at": iso(created), "issue_after_s": secs(created, issue_at),
          "step1_after_s": secs(created, step1_at),
          "readme_promise_met": (secs(created, step1_at) or 999) <= 20,
          "first_step": step1["step"], "step1_comment": step1["url"]}, True)
    return 0


def cmd_status(args):
    issue = find_issue(args.repo, args.title_text)
    wfs = workflows(args.repo)
    rs = runs(args.repo, args.limit)
    cs = comments(args.repo, issue["number"]) if issue else []
    bot = [c for c in cs if c["author"] == BOT]
    posted = sorted({c["step"] for c in bot if c["kind"] == "step-content" and c["step"]})
    last_result = next((c for c in reversed(bot) if c["kind"] in ("result-pass", "result-fail")), None)
    data = {
        "repo": args.repo,
        "issue": issue,
        "current_step": current_step(wfs),
        "steps_posted": posted,
        "review_posted": any(c["kind"] == "review" for c in bot),
        "finished": any(c["kind"] == "finished" for c in bot) or bool(issue and issue["state"] == "CLOSED"),
        "last_result": {"step": last_result["step"], "kind": last_result["kind"], "url": last_result["url"]} if last_result else None,
        "workflows": [{k: w[k] for k in ("name", "path", "state")} for w in wfs],
        "recent_runs": [{k: r[k] for k in ("workflowName", "event", "status", "conclusion", "createdAt", "url")} for r in rs],
        "last_comments": [{k: c[k] for k in ("id", "author", "kind", "step", "created_at", "updated_at", "url")} for c in cs[-args.last:]],
    }
    if args.json:
        emit(data, True)
        return 0
    lines = [f"Repository: https://github.com/{args.repo}",
             f"Issue: {issue['url'] if issue else 'not found'} ({issue['state'] if issue else '-'})",
             f"Active step workflow: {data['current_step']}",
             f"Steps posted: {posted or 'none'}   Review posted: {data['review_posted']}   Finished: {data['finished']}",
             "Workflows:"]
    lines += [f"  {w['name']:<10} {w['state']:<18} {w['path']}" for w in wfs]
    lines.append("Recent runs:")
    lines += [f"  {r['createdAt']}  {r['workflowName']:<10} {r['event']:<14} {r['status']:<11} {r['conclusion'] or '-':<9} {r['url']}" for r in rs]
    lines.append("Last comments:")
    lines += [f"  #{c['id']} {c['created_at']} {c['author']:<20} {c['kind']:<14} step={c['step']}" for c in cs[-args.last:]]
    print("\n".join(lines))
    return 0


def cmd_comments(args):
    issue = find_issue(args.repo, args.title_text)
    if not issue:
        raise HarnessError("exercise issue not found")
    cs = comments(args.repo, issue["number"])
    since = parse_since(args.since)
    if since:
        cs = [c for c in cs if parse_ts(c["updated_at"]) >= since]
    if not args.full:
        for c in cs:
            c["body"] = (c["body"][:400] + "...") if len(c["body"]) > 400 else c["body"]
    for c in cs:
        c.pop("body_html", None)
    if args.json:
        emit(cs, True)
        return 0
    for c in cs:
        print(f"--- #{c['id']} {c['created_at']} (updated {c['updated_at']}) {c['author']} [{c['kind']}] {c['url']}")
        print(c["body"])
    return 0


def step_runs(repo: str, since: datetime, workflow: str | None) -> list[dict]:
    """Runs of the step workflow under test (or of any `Step N` workflow) that the action could have started.

    A small lookback absorbs clock skew, but runs that had already completed before `since` are excluded so an
    earlier attempt (for example a previous negative test) is never attributed to this action.
    """
    out = []
    for r in runs(repo, 50):
        if parse_ts(r["createdAt"]) < since - CLOCK_SKEW:
            continue
        if r["status"] == "completed" and parse_ts(r["updatedAt"]) < since:
            continue
        name = r.get("workflowName") or ""
        if (workflow and name == workflow) or (not workflow and STEP_WORKFLOW_RE.match(name)):
            out.append(r)
    return out


def cmd_wait_step(args):
    since = parse_since(args.since) or utcnow()
    workflow = args.workflow or (f"Step {args.step}" if args.step is not None else None)
    issue = find_issue(args.repo, args.title_text)
    if not issue:
        raise HarnessError("exercise issue not found")
    timeout = args.timeout if args.timeout is not None else (90 if args.expect == "none" else 420)
    started = time.monotonic()
    broken_since = None
    rs = []

    def result(outcome, ok_for, **extra):
        emit({"outcome": outcome, "expected": args.expect, "workflow": workflow or "any Step N",
              "runs": [{k: r[k] for k in ("workflowName", "event", "status", "conclusion", "url")} for r in rs], **extra}, True)
        return 0 if args.expect in ok_for else 1

    while time.monotonic() - started < timeout:
        cs = [c for c in comments(args.repo, issue["number"]) if c["author"] == BOT and parse_ts(c["updated_at"]) >= since]
        nxt = [c for c in cs if (c["kind"] == "step-content" and (args.step is None or c["step"] == args.step + 1))
               or c["kind"] in ("review", "finished")]
        fail = [c for c in cs if c["kind"] == "result-fail" and (args.step is None or c["step"] == args.step)]
        rs = step_runs(args.repo, since, workflow)
        if nxt:
            first = min(nxt, key=lambda c: c["created_at"])
            return result("advanced", ("pass", "any"), posted=first["kind"], step=first["step"], comment=first["url"],
                          feedback_after_s=secs(since, parse_ts(first["created_at"])))
        done = [r for r in rs if r["status"] == "completed"]
        if fail and done:
            return result("failed-check", ("fail", "any"), comment=fail[-1]["url"],
                          feedback_after_s=secs(since, parse_ts(fail[-1]["updated_at"])), feedback=fail[-1]["body"][:1500])
        broken = [r for r in done if r["conclusion"] in ("failure", "startup_failure")]
        if broken and not fail:
            # Give Mona's results comment time to land after the run fails.
            broken_since = broken_since or time.monotonic()
            if time.monotonic() - broken_since > args.grace:
                return result("workflow-error", (), run=broken[0]["url"],
                              hint="The step workflow failed without learner feedback. Inspect with: runs --failed-logs")
        time.sleep(args.interval)
    pending = [r for r in rs if r["status"] != "completed"]
    if args.expect == "none" and not pending and all(r["conclusion"] == "skipped" for r in rs):
        return result("ignored", ("none",), waited_s=timeout,
                      hint="No graded run and no new step: learners get no reply here, so Having trouble must cover it.")
    return result("timeout", (), waited_s=timeout,
                  hint="No feedback: check that the action matches the step trigger (event, branch, paths) "
                       "and that the step workflow is enabled.")


def cmd_lint_comments(args):
    issue = find_issue(args.repo, args.title_text)
    if not issue:
        raise HarnessError("exercise issue not found")
    problems = []
    for c in comments(args.repo, issue["number"], html=True):
        if c["author"] != BOT:
            continue
        body, html = c["body"], c["body_html"] or ""
        prose = re.sub(r"<(pre|code)\b.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", prose)
        where = f"comment {c['id']} ({c['kind']}, step {c['step']})"
        if re.search(r"\{\{|\{%", text):
            problems.append({"where": where, "url": c["url"], "issue": "unrendered template syntax ({{ or {%) visible to the learner"})
        if re.search(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", text):
            problems.append({"where": where, "url": c["url"], "issue": "GitHub alert did not render (indented or inside a list)"})
        for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
            if not src.startswith(("http://", "https://")):
                problems.append({"where": where, "url": c["url"], "issue": f"relative image {src} will not load"})
        for href in re.findall(r'<a[^>]+href="([^"]+)"', html):
            if href.startswith("../"):
                problems.append({"where": where, "url": c["url"], "issue": f"relative link {href} resolves against the issue URL"})
        for path in sorted(set(re.findall(r"/blob/[^/]+/(\.github/images/[^?\s\"')]+)", body))):
            ok = subprocess.run(["gh", "api", f"repos/{args.repo}/contents/{path}", "--silent"], capture_output=True).returncode == 0
            if not ok:
                problems.append({"where": where, "url": c["url"], "issue": f"image {path} not found in the repository"})
    emit({"issue": issue["url"], "problems": problems, "ok": not problems}, True)
    return 0 if not problems else 1


def cmd_timeline(args):
    issue = find_issue(args.repo, args.title_text)
    events = []
    for r in runs(args.repo, args.limit):
        events.append((r["createdAt"], "run", f"{r['workflowName']} [{r['event']}] -> {r['conclusion'] or r['status']} "
                       f"({secs(parse_ts(r['createdAt']), parse_ts(r['updatedAt']))}s) {r['url']}"))
    if issue:
        for c in comments(args.repo, issue["number"]):
            edited = c["updated_at"] != c["created_at"]
            events.append((c["created_at"], "comment", f"{c['author']} {c['kind']}{' (edited later)' if edited else ''} "
                           f"step={c['step']} {c['url']}"))
            if edited:
                events.append((c["updated_at"], "edit", f"{c['author']} {c['kind']} step={c['step']} {c['url']}"))
    events.sort()
    if args.json:
        emit([{"at": a, "type": t, "detail": d} for a, t, d in events], True)
    else:
        print("\n".join(f"{a}  {t:<8} {d}" for a, t, d in events))
    return 0


def cmd_runs(args):
    rs = runs(args.repo, args.limit)
    emit(rs, True)
    if args.failed_logs:
        failed = [r for r in rs if r["conclusion"] == "failure"]
        if failed:
            log = gh("run", "view", str(failed[0]["databaseId"]), "-R", args.repo, "--log-failed", check=False)
            print("\n--- failed log (last 120 lines) ---")
            print("\n".join(log.splitlines()[-120:]))
    return 0


def list_codespaces(repo: str) -> list[dict]:
    out = gh("codespace", "list", "--repo", repo, "--json", "name,displayName,state,createdAt,lastUsedAt,machineName")
    return json.loads(out) if out.strip() else []


def cmd_codespaces(args):
    emit({"repo": args.repo, "codespaces": list_codespaces(args.repo),
          "note": "Stopped codespaces still use storage; delete them when the test is over."}, True)
    return 0


def cmd_cleanup(args):
    command = ["repo", "archive", args.repo, "--yes"] if args.mode == "archive" else ["repo", "delete", args.repo, "--yes"]
    try:
        spaces = list_codespaces(args.repo)
        spaces_error = None
    except HarnessError as exc:
        spaces, spaces_error = [], str(exc)
    plan = {
        "repository": f"{'archive (read-only)' if args.mode == 'archive' else 'permanently delete'} {args.repo}",
        "codespaces_found": [s["name"] for s in spaces],
        "codespaces_action": "delete" if args.delete_codespaces else "keep (they keep using storage until deleted)",
    }
    if spaces_error:
        plan["codespaces_unknown"] = f"could not list codespaces ({spaces_error}); add the 'codespace' scope to check"
    if not args.yes:
        emit({"confirmation_required": True, "command": "gh " + " ".join(command), "plan": plan}, True)
        return 3
    deleted = []
    if args.delete_codespaces:
        for space in spaces:
            gh("codespace", "delete", "--codespace", space["name"], "--force")
            deleted.append(space["name"])
    proc = subprocess.run(["gh", *command], capture_output=True, text=True)
    if proc.returncode != 0:
        hint = " Run: gh auth refresh -h github.com -s delete_repo" if "delete_repo" in proc.stderr else ""
        raise HarnessError(proc.stderr.strip() + hint)
    retained = [s["name"] for s in spaces if s["name"] not in deleted]
    emit({"repo": args.repo, "action": args.mode, "done": True, "codespaces_deleted": deleted,
          "codespaces_retained": retained, **({"codespaces_unknown": plan["codespaces_unknown"]} if spaces_error else {})}, True)
    return 0


# --------------------------------------------------------------------------- cli


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def repo_cmd(name, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("--repo", required=True, help="learner copy OWNER/NAME")
        p.add_argument("--title-text", default="Exercise", help="text find-exercise-issue matches (default: Exercise)")
        return p

    sub.add_parser("now", help="print current UTC time")
    p = sub.add_parser("preflight", help="check gh, scopes, template (and its commit) and owner")
    p.add_argument("--template", help="template repository OWNER/NAME")
    p.add_argument("--owner", help="account or organization that will own the learner copy")
    p = sub.add_parser("create", help="create a learner copy from the template")
    p.add_argument("--template", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--name", help="default: skills-<template>-wt-<timestamp>")
    p.add_argument("--visibility", required=True, choices=("public", "private", "internal"),
                   help="must be approved by the user; public copies of non-public templates are refused")
    p.add_argument("--yes", action="store_true", help="the user approved creating this repository")
    p = repo_cmd("wait-start", "wait for the exercise to start")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=5)
    p = repo_cmd("status", "show exercise state")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--last", type=int, default=6)
    p.add_argument("--json", action="store_true")
    p = repo_cmd("comments", "list exercise issue comments")
    p.add_argument("--since", help="ISO timestamp with timezone; only comments created or updated after it")
    p.add_argument("--full", action="store_true", help="print full bodies")
    p.add_argument("--json", action="store_true")
    p = repo_cmd("wait-step", "wait for the result of a learner action")
    p.add_argument("--since", help="UTC timestamp taken just before the action (output of `now`)")
    p.add_argument("--step", type=int, help="the step being completed; runs are matched to its `Step N` workflow")
    p.add_argument("--workflow", help="workflow name to watch (default: `Step <step>`)")
    p.add_argument("--expect", choices=("pass", "fail", "any", "none"), default="pass",
                   help="pass: advances; fail: graded failure; none: action is filtered out and nothing happens")
    p.add_argument("--timeout", type=int, help="seconds (default 420, or 90 with --expect none)")
    p.add_argument("--interval", type=int, default=8)
    p.add_argument("--grace", type=int, default=30, help="seconds to wait for feedback after the step run fails")
    repo_cmd("lint-comments", "check rendered comments")
    p = repo_cmd("timeline", "chronological runs and comments")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--json", action="store_true")
    p = repo_cmd("runs", "recent workflow runs")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--failed-logs", action="store_true")
    repo_cmd("codespaces", "list codespaces for the learner copy")
    p = repo_cmd("cleanup", "archive or delete the learner copy")
    p.add_argument("--mode", choices=("archive", "delete"), default="archive")
    p.add_argument("--delete-codespaces", action="store_true", help="also delete the copy's codespaces")
    p.add_argument("--yes", action="store_true", help="the user approved this cleanup")

    args = ap.parse_args(argv)
    handler = globals()["cmd_" + args.cmd.replace("-", "_")]
    try:
        return handler(args)
    except HarnessError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (KeyError, ValueError, TypeError, OSError) as exc:
        print(f"error: unexpected {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
