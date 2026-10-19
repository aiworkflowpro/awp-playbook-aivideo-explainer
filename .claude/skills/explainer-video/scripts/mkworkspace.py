#!/usr/bin/env python3
"""Steps 04-05 workspaces: freeze the shared layer, then give each segment its own clean workspace.

    python3 mkworkspace.py --project app --freeze      # mark the committed shared layer as the base
    python3 mkworkspace.py --project app s02            # a workspace for segment s02
    python3 mkworkspace.py --project app s02 --dry-run  # only print what would happen

Why: a segment builder must start from the shared layer alone, never from main (main already
holds other segments, and a builder that sees their code drifts toward them).

With git (recommended):
  --freeze   points the `shared` branch at the current commit (the working tree must be clean).
  sNN        adds a git worktree on a new branch `segment/sNN`, made from `shared`, at
             <repo-parent>/<repo-name>-segments/sNN (change with --root). node_modules is linked
             from the main project, so no second npm install.
Without git:
  --freeze   copies the project to <project>-shared (skipping node_modules, out, .git).
  sNN        copies that snapshot to <root>/sNN and links node_modules.

In both cases the segment folder src/segments/sNN/ is seeded from src/segments/_template/ (the
token __SEGMENT_ID__ in its files becomes sNN) unless it already exists. Prints JSON.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SKIP = {"node_modules", "out", ".git", "build", "dist", ".cache"}
TOKEN = "__SEGMENT_ID__"


def git(args: list[str], cwd: Path, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def repo_root(project: Path) -> Path | None:
    if not shutil.which("git"):
        return None
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=project, capture_output=True, text=True, check=False)
    return Path(r.stdout.strip()).resolve() if r.returncode == 0 and r.stdout.strip() else None


def branch_exists(root: Path, name: str) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{name}"],
                          cwd=root, capture_output=True, check=False).returncode == 0


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])


def link_node_modules(src_project: Path, dst_project: Path, actions: list[str], dry: bool) -> None:
    nm, target = src_project / "node_modules", dst_project / "node_modules"
    if nm.is_dir() and not target.exists():
        actions.append(f"link {target} -> {nm}")
        if not dry:
            try:
                os.symlink(nm, target, target_is_directory=True)
            except OSError:
                actions.append("could not link node_modules (Windows without symlink rights?); run npm install in the workspace")
    elif not nm.is_dir():
        actions.append("no node_modules in the main project yet; run npm install there first, then link or install in the workspace")


def seed_segment(project: Path, seg: str, actions: list[str], dry: bool) -> Path:
    seg_dir = project / "src" / "segments" / seg
    tmpl = project / "src" / "segments" / "_template"
    if seg_dir.exists():
        actions.append(f"segment folder exists: {seg_dir}")
        return seg_dir
    if not tmpl.is_dir():
        actions.append(f"no {tmpl}; create {seg_dir} yourself")
        return seg_dir
    actions.append(f"seed {seg_dir} from _template")
    if not dry:
        shutil.copytree(tmpl, seg_dir)
        for f in seg_dir.rglob("*"):
            if f.is_file():
                try:
                    text = f.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if TOKEN in text:
                    f.write_text(text.replace(TOKEN, seg), encoding="utf-8")
    return seg_dir


def freeze(project: Path, root: Path | None, dry: bool) -> dict[str, Any]:
    actions: list[str] = []
    if root:
        dirty = git(["status", "--porcelain"], root)
        if dirty:
            raise RuntimeError("commit the shared layer first; the working tree has changes:\n" + dirty)
        head = git(["rev-parse", "--short", "HEAD"], root)
        actions.append(f"branch shared -> {head}")
        if not dry:
            git(["branch", "-f", "shared", "HEAD"], root)
        return {"mode": "git", "frozen": "shared", "commit": head, "actions": actions}
    snap = project.with_name(project.name + "-shared")
    actions.append(f"snapshot {project} -> {snap}")
    if not dry:
        if snap.exists():
            shutil.rmtree(snap)
        copy_tree(project, snap)
    return {"mode": "copy", "frozen": str(snap), "actions": actions}


def make_segment(project: Path, root: Path | None, seg: str, base: str, out_root: Path | None, dry: bool) -> dict[str, Any]:
    actions: list[str] = []
    if root:
        rel = project.relative_to(root)
        wt_root = out_root or root.parent / f"{root.name}-segments"
        wt = (wt_root / seg).resolve()
        branch = f"segment/{seg}"
        if not branch_exists(root, base):
            raise RuntimeError(f"no '{base}' branch; run with --freeze first (after committing the shared layer)")
        if wt.exists():
            actions.append(f"workspace exists: {wt}")
        elif branch_exists(root, branch):
            actions.append(f"git worktree add {wt} {branch}")
            if not dry:
                git(["worktree", "add", str(wt), branch], root)
        else:
            actions.append(f"git worktree add -b {branch} {wt} {base}")
            if not dry:
                wt_root.mkdir(parents=True, exist_ok=True)
                git(["worktree", "add", "-b", branch, str(wt), base], root)
        ws_project = wt / rel
        link_node_modules(project, ws_project, actions, dry)
        seg_dir = seed_segment(ws_project, seg, actions, dry)
        return {"mode": "git", "segment": seg, "branch": branch, "base": base, "workspace": str(wt),
                "project": str(ws_project), "segment_dir": str(seg_dir), "actions": actions}
    snap = project.with_name(project.name + "-shared")
    src = snap if snap.is_dir() else project
    if src is project:
        actions.append("no frozen snapshot found; copying the project as it is (run --freeze first next time)")
    ws_root = out_root or project.parent / "segments"
    ws = (ws_root / seg).resolve()
    if ws.exists():
        actions.append(f"workspace exists: {ws}")
    else:
        actions.append(f"copy {src} -> {ws}")
        if not dry:
            ws_root.mkdir(parents=True, exist_ok=True)
            copy_tree(src, ws)
    link_node_modules(project, ws, actions, dry)
    seg_dir = seed_segment(ws, seg, actions, dry)
    return {"mode": "copy", "segment": seg, "base": str(src), "workspace": str(ws), "project": str(ws),
            "segment_dir": str(seg_dir), "actions": actions}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("segment", nargs="?", help="segment id, e.g. s02")
    ap.add_argument("--project", required=True, help="the Remotion project folder (usually app)")
    ap.add_argument("--freeze", action="store_true", help="mark the current shared layer as the base for all segments")
    ap.add_argument("--base", default="shared", help="branch the segment starts from (default: shared)")
    ap.add_argument("--root", help="folder for workspaces (default: <repo-name>-segments next to the repo)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    a = ap.parse_args()

    project = Path(a.project).expanduser().resolve()
    if not (project / "package.json").is_file():
        print(f"error: {project} has no package.json; point --project at the Remotion app", file=sys.stderr)
        return 1
    if not a.freeze and not a.segment:
        print("error: give a segment id (e.g. s02) or --freeze", file=sys.stderr)
        return 1
    if a.segment and not re.fullmatch(r"s\d{2}", a.segment):
        print("error: segment ids look like s01, s02, ...", file=sys.stderr)
        return 1

    root = repo_root(project)
    out_root = Path(a.root).expanduser().resolve() if a.root else None
    result: dict[str, Any] = {"dry_run": a.dry_run}
    try:
        if a.freeze:
            result["freeze"] = freeze(project, root, a.dry_run)
        if a.segment:
            result["workspace"] = make_segment(project, root, a.segment, a.base, out_root, a.dry_run)
    except (RuntimeError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
