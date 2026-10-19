#!/usr/bin/env python3
"""Step 01 preflight: check the tools an explainer film needs, and say how to install what is missing.

    python3 preflight.py                    # check tools, print a report
    python3 preflight.py --json             # the same, as JSON
    python3 preflight.py --project my-film  # also report where a film left off (progress.md, handoff/)

Required: Node.js 18+ (with npm and npx), ffmpeg and ffprobe, git, Python 3.11+.
Optional: a local Whisper for word-level transcription (openai-whisper or whisper.cpp).
Nothing is installed, downloaded or rendered. Exit code 0 when every required tool is found, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent

HINTS: dict[str, dict[str, str]] = {
    "node": {
        "macos": "brew install node",
        "linux": "install Node.js 18+ from https://nodejs.org or your package manager (e.g. sudo apt install nodejs npm)",
        "windows": "winget install OpenJS.NodeJS.LTS",
    },
    "ffmpeg": {
        "macos": "brew install ffmpeg",
        "linux": "sudo apt install ffmpeg (or your distribution's package)",
        "windows": "winget install Gyan.FFmpeg",
    },
    "git": {
        "macos": "xcode-select --install (or brew install git)",
        "linux": "sudo apt install git",
        "windows": "winget install Git.Git",
    },
    "python": {
        "macos": "brew install python@3.12",
        "linux": "install Python 3.11+ from your package manager",
        "windows": "winget install Python.Python.3.12",
    },
    "whisper": {
        "macos": "pipx install openai-whisper  (or: brew install whisper-cpp, then download a ggml model)",
        "linux": "pipx install openai-whisper  (or build whisper.cpp from https://github.com/ggml-org/whisper.cpp)",
        "windows": "pipx install openai-whisper  (or a whisper.cpp release from https://github.com/ggml-org/whisper.cpp)",
    },
}


def os_key() -> str:
    s = platform.system().lower()
    if s == "darwin":
        return "macos"
    if s.startswith("win"):
        return "windows"
    return "linux"


def run_version(cmd: list[str]) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = (r.stdout or r.stderr or "").strip().splitlines()
    return out[0].strip() if out else ""


def major_version(text: str | None) -> int | None:
    if not text:
        return None
    m = re.search(r"(\d+)\.(\d+)", text)
    return int(m.group(1)) if m else None


def load_config() -> dict[str, Any]:
    p = SKILL_DIR / "config.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def check_tools() -> list[dict[str, Any]]:
    key = os_key()
    results: list[dict[str, Any]] = []

    def add(name: str, required: bool, found: bool, version: str | None, note: str = "", hint_key: str | None = None) -> None:
        hint = "" if found else HINTS.get(hint_key or name, {}).get(key, "")
        results.append({"tool": name, "required": required, "ok": found, "version": version or "", "note": note, "install": hint})

    node_v = run_version(["node", "--version"])
    node_major = major_version(node_v)
    node_ok = node_major is not None and node_major >= 18
    add("node", True, node_ok, node_v, "" if node_ok or node_v is None else "Node.js 18 or newer is needed", "node")
    for tool in ("npm", "npx"):
        v = run_version([tool, "--version"])
        add(tool, True, v is not None, v, "comes with Node.js", "node")

    for tool in ("ffmpeg", "ffprobe"):
        v = run_version([tool, "-version"])
        add(tool, True, v is not None, v, "", "ffmpeg")

    git_v = run_version(["git", "--version"])
    add("git", True, git_v is not None, git_v, "", "git")

    py_ok = sys.version_info >= (3, 11)
    add("python", True, py_ok, platform.python_version(), "" if py_ok else "Python 3.11 or newer is needed", "python")

    cfg = load_config().get("transcribe", {})
    cpp_bin = cfg.get("whisper_cpp_binary") or "whisper-cli"
    ow = shutil.which("whisper")
    cpp = shutil.which(cpp_bin)
    engines = []
    if ow:
        engines.append("openai-whisper")
    if cpp:
        engines.append(f"whisper.cpp ({cpp_bin})")
    note = "found: " + ", ".join(engines) if engines else "needed only if you have no word-level timings yet"
    if cpp and not cfg.get("whisper_cpp_model") and not ow:
        note += "; set transcribe.whisper_cpp_model in config.json to a ggml model file"
    add("whisper", False, bool(engines), "", note, "whisper")

    template = SKILL_DIR.parent.parent / "template"
    if (template / "package.json").is_file():
        installed = (template / "node_modules" / ".bin").is_dir()
        results.append({"tool": "remotion template", "required": False, "ok": True,
                        "version": "", "install": "",
                        "note": "dependencies installed" if installed else "Step 02 copies template/ into the film as app/ and runs npm install there"})
    return results


def resume_state(project: Path) -> dict[str, Any]:
    state: dict[str, Any] = {"project": str(project)}
    progress = project / "progress.md"
    state["progress_md"] = progress.is_file()
    if progress.is_file():
        rows = [ln for ln in progress.read_text(encoding="utf-8").splitlines() if ln.startswith("| ") and not ln.startswith("| Step") and not set(ln) <= set("|- ")]
        state["progress_rows"] = rows
    handoff = project / "handoff"
    pages = sorted(handoff.glob("*.md")) if handoff.is_dir() else []
    state["handoff_pages"] = [p.name for p in pages]
    state["latest_handoff"] = pages[-1].name if pages else None
    if pages:
        m = re.match(r"(\d{2})", pages[-1].name)
        state["resume_hint"] = f"read handoff/{pages[-1].name}; continue from step {m.group(1)} or the next one" if m else ""
    else:
        state["resume_hint"] = "no handoff pages yet: a new film; finish Step 01, then go on to Step 02"
    return state


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="print JSON instead of a table")
    ap.add_argument("--project", help="film folder to inspect when resuming (reads progress.md and handoff/)")
    a = ap.parse_args()

    tools = check_tools()
    missing = [t for t in tools if t["required"] and not t["ok"]]
    report: dict[str, Any] = {"os": os_key(), "ok": not missing, "tools": tools}
    if a.project:
        report["resume"] = resume_state(Path(a.project).expanduser().resolve())

    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Preflight ({report['os']})")
        for t in tools:
            mark = "ok  " if t["ok"] else ("MISS" if t["required"] else "--  ")
            req = "required" if t["required"] else "optional"
            line = f"  [{mark}] {t['tool']:<18} {req:<9} {t['version']}"
            print(line.rstrip())
            if t["note"]:
                print(f"         {t['note']}")
            if t["install"]:
                print(f"         install: {t['install']}")
        if a.project:
            r = report["resume"]
            print(f"\nResume: {r['project']}")
            print(f"  progress.md: {'yes' if r['progress_md'] else 'no'}")
            for row in r.get("progress_rows", []):
                print(f"    {row}")
            print(f"  latest handoff: {r['latest_handoff'] or '-'}")
            print(f"  {r['resume_hint']}")
        print("\nAll required tools found." if not missing else f"\nMissing required tools: {', '.join(t['tool'] for t in missing)}. Install them, then run again.")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
