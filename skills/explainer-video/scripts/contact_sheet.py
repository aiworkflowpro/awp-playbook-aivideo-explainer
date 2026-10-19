#!/usr/bin/env python3
"""Step 04 references: contact sheets from your own reference clips, one sheet per shot.

    python3 contact_sheet.py references/ --out references/sheets/
    python3 contact_sheet.py references/some-clip.mp4 --out references/sheets/ --threshold 0.25

For every video, ffmpeg scene detection cuts it into shots (shots shorter than the minimum are
merged into the one before). From each shot it takes 8 frames, evenly spaced from 3% to 93% of
the shot, writes the source time code in the top-left corner of each, and tiles them 4 x 2 into
one image. A sheet shows how a shot moves without playing it, so an agent can read staging,
timing and structure.

Output:
  <out>/<video-stem>/shot-001.jpg, shot-002.jpg, ...
  <out>/<video-stem>/index.json   (start, end and frame times of every shot)
  <out>/index.json                (all videos)

Use clips you are allowed to study. Sheets are for learning staging, not for copying the look.
Needs ffmpeg and ffprobe. Settings default to contact_sheet in config.json.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
FRAMES = 8
COLS, ROWS = 4, 2


def load_config() -> dict[str, Any]:
    try:
        return json.loads((SKILL_DIR / "config.json").read_text(encoding="utf-8")).get("contact_sheet", {})
    except (OSError, json.JSONDecodeError):
        return {}


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=False)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def scene_cuts(path: Path, threshold: float) -> list[float]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-an",
                        "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True, check=False)
    return [float(m) for m in re.findall(r"pts_time:\s*([0-9.]+)", r.stderr)]


def shots_from_cuts(cuts: list[float], total: float, min_len: float) -> list[tuple[float, float]]:
    edges = [0.0] + [c for c in sorted(cuts) if 0.0 < c < total] + [total]
    shots: list[list[float]] = []
    for a, b in zip(edges, edges[1:]):
        if b - a <= 0:
            continue
        if shots and (b - a < min_len or shots[-1][1] - shots[-1][0] < min_len):
            shots[-1][1] = b
        else:
            shots.append([a, b])
    return [(a, b) for a, b in shots]


def timecode(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def grab(path: Path, t: float, width: int, out: Path, with_text: bool) -> bool:
    vf = f"scale={width}:-2"
    if with_text:
        tc = timecode(t).replace(":", r"\:")
        vf += (f",drawtext=text='{tc}':x=8:y=8:fontsize={max(14, width // 24)}"
               ":fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=4")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.3f}",
                        "-i", str(path), "-frames:v", "1", "-vf", vf, str(out)],
                       capture_output=True, text=True, check=False)
    return r.returncode == 0 and out.is_file()


def sheet_for_shot(path: Path, start: float, end: float, width: int, out: Path, state: dict[str, bool]) -> list[float]:
    span = end - start
    times = [start + span * (0.03 + i * (0.90 / (FRAMES - 1))) for i in range(FRAMES)]
    with tempfile.TemporaryDirectory(prefix="sheet-") as td:
        tmp = Path(td)
        for i, t in enumerate(times):
            frame = tmp / f"f{i:02d}.png"
            if state["text"] and not grab(path, t, width, frame, True):
                state["text"] = False  # drawtext unavailable in this ffmpeg build: carry on without time codes
                print("note: drawtext failed, sheets will have no time codes", file=sys.stderr)
            if not state["text"] and not grab(path, t, width, frame, False):
                raise RuntimeError(f"could not read a frame at {t:.2f}s")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1",
                        "-i", str(tmp / "f%02d.png"), "-vf", f"tile={COLS}x{ROWS}:padding=4:margin=4",
                        "-frames:v", "1", "-q:v", "3", str(out)], check=True)
    return [round(t, 3) for t in times]


def collect(inp: Path) -> list[Path]:
    if inp.is_file():
        return [inp]
    return sorted(p for p in inp.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXT)


def main() -> int:
    cfg = load_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="a reference video, or a folder of them (not searched recursively)")
    ap.add_argument("--out", required=True, help="output folder, e.g. references/sheets/")
    ap.add_argument("--threshold", type=float, default=float(cfg.get("scene_threshold", 0.3)), help="scene change score 0-1 (default %(default)s); lower finds more cuts")
    ap.add_argument("--min-shot", type=float, default=float(cfg.get("min_shot_seconds", 0.5)), help="shots shorter than this many seconds are merged (default %(default)s)")
    ap.add_argument("--width", type=int, default=int(cfg.get("frame_width", 480)), help="width of each frame in pixels (default %(default)s)")
    ap.add_argument("--max-shots", type=int, default=0, help="stop after this many shots per video (0 = all)")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print(f"error: {tool} not found; run preflight.py for the install command", file=sys.stderr)
            return 1
    inp = Path(a.input).expanduser()
    if not inp.exists():
        print(f"error: not found: {inp}", file=sys.stderr)
        return 1
    videos = collect(inp)
    if not videos:
        print(f"error: no videos ({', '.join(sorted(VIDEO_EXT))}) in {inp}", file=sys.stderr)
        return 1

    out_root = Path(a.out).expanduser()
    out_root.mkdir(parents=True, exist_ok=True)
    state = {"text": True}
    summary: list[dict[str, Any]] = []
    for video in videos:
        total = duration(video)
        if total <= 0:
            print(f"skip: cannot read duration of {video.name}", file=sys.stderr)
            continue
        shots = shots_from_cuts(scene_cuts(video, a.threshold), total, a.min_shot)
        if a.max_shots > 0:
            shots = shots[: a.max_shots]
        vdir = out_root / video.stem
        vdir.mkdir(parents=True, exist_ok=True)
        entries: list[dict[str, Any]] = []
        for n, (s, e) in enumerate(shots, 1):
            sheet = vdir / f"shot-{n:03d}.jpg"
            try:
                times = sheet_for_shot(video, s, e, a.width, sheet, state)
            except (RuntimeError, subprocess.CalledProcessError) as err:
                print(f"skip: {video.name} shot {n}: {err}", file=sys.stderr)
                continue
            entries.append({"shot": n, "sheet": sheet.name, "start": round(s, 3), "end": round(e, 3),
                            "start_tc": timecode(s), "frame_times": times})
        (vdir / "index.json").write_text(json.dumps({"video": video.name, "duration": round(total, 3), "shots": entries}, indent=1) + "\n", encoding="utf-8")
        summary.append({"video": video.name, "shots": len(entries), "folder": str(vdir)})
        print(f"{video.name}: {len(entries)} sheets -> {vdir}")
    (out_root / "index.json").write_text(json.dumps({"videos": summary}, indent=1) + "\n", encoding="utf-8")
    return 0 if summary else 1


if __name__ == "__main__":
    sys.exit(main())
