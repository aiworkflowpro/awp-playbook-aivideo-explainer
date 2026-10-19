#!/usr/bin/env python3
"""Steps 06-07 hard-fault check: one page on what is wrong with a render. Not whether it is good.

    python3 check_render.py out/film.mp4 --out review/check-first-cut.md
    python3 check_render.py deliver/master.mp4 --out deliver/check-master.md --strict

One ffprobe call and one ffmpeg pass (nothing is re-encoded) check:
  spec          frame rate, size, codecs, audio present
  black         blackdetect: black stretches longer than black_min_seconds
  freeze        freezedetect: the picture standing still longer than freeze_min_seconds
  loudness      ebur128 with true peak: integrated LUFS and true peak against the target
  silence       silencedetect: the sound dropping out longer than silence_min_seconds
  one-frame     a picture that jumps in on one frame and out on the next (a flash or a stray frame)

Thresholds and targets default to config.json (format, loudness, check_render).
A finding is a place to look, not a verdict: a held frame or a black fade can be on purpose.
Taste, pacing and ideas are judged by watching (references/review.md), never by this script.
Exit code 0, or with --strict 1 when there are findings.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent


def load_config() -> dict[str, Any]:
    try:
        return json.loads((SKILL_DIR / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def tc(t: float) -> str:
    m, s = divmod(max(0.0, t), 60)
    return f"{int(m)}:{s:05.2f}"


def probe(video: Path) -> dict[str, Any]:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)],
                       capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "ffprobe failed")
    return json.loads(r.stdout)


def rate(s: str | None) -> float:
    if not s or s == "0/0":
        return 0.0
    if "/" in s:
        n, d = s.split("/", 1)
        return float(n) / float(d) if float(d) else 0.0
    return float(s)


def analyse(video: Path, has_audio: bool, c: dict[str, Any]) -> str:
    vf = (f"blackdetect=d={c['black']}:pix_th=0.10,"
          f"freezedetect=n=-60dB:d={c['freeze']},"
          f"select='gt(scene,{c['glitch']})',showinfo")
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-vf", vf]
    if has_audio:
        cmd += ["-af", f"ebur128=peak=true,silencedetect=n={c['silence_db']}dB:d={c['silence']}"]
    else:
        cmd += ["-an"]
    cmd += ["-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return r.stderr


def parse(log: str, fps: float, duration: float) -> dict[str, Any]:
    black = [(float(a), float(b)) for a, b in re.findall(r"black_start:\s*([0-9.]+)\s+black_end:\s*([0-9.]+)", log)]
    fs = [float(x) for x in re.findall(r"freezedetect\.freeze_start:\s*([0-9.]+)", log)]
    fe = [float(x) for x in re.findall(r"freezedetect\.freeze_end:\s*([0-9.]+)", log)]
    freeze = [(s, fe[i] if i < len(fe) else duration) for i, s in enumerate(fs)]
    ss = [float(x) for x in re.findall(r"silence_start:\s*(-?[0-9.]+)", log)]
    se = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", log)]
    silence = [(max(0.0, s), se[i] if i < len(se) else duration) for i, s in enumerate(ss)]

    summary = log[log.rfind("Summary:"):] if "Summary:" in log else ""
    m_i = re.search(r"I:\s*(-?[0-9.]+|-inf)\s*LUFS", summary)
    m_tp = re.search(r"True peak:\s*Peak:\s*(-?[0-9.]+|-inf)\s*dBFS", summary, re.S)
    lufs = float(m_i.group(1)) if m_i and m_i.group(1) != "-inf" else None
    tp = float(m_tp.group(1)) if m_tp and m_tp.group(1) != "-inf" else None

    jumps = sorted(float(x) for x in re.findall(r"pts_time:\s*([0-9.]+)", log))
    frame = 1.0 / fps if fps else 1 / 60
    one_frame: list[float] = []
    for a, b in zip(jumps, jumps[1:]):
        if 0 < b - a <= frame * 1.5 and (not one_frame or a - one_frame[-1] > frame * 2):
            one_frame.append(a)
    return {"black": black, "freeze": freeze, "silence": silence, "lufs": lufs, "true_peak": tp, "one_frame": one_frame}


def main() -> int:
    cfg = load_config()
    fmt, loud, cr = cfg.get("format", {}), cfg.get("loudness", {}), cfg.get("check_render", {})
    res = fmt.get("review_resolution", [1920, 1080])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="the rendered file")
    ap.add_argument("--out", required=True, help="Markdown report path")
    ap.add_argument("--fps", type=float, default=float(fmt.get("fps", 60)), help="expected frame rate (default %(default)s)")
    ap.add_argument("--width", type=int, default=int(res[0]), help="expected width (default %(default)s)")
    ap.add_argument("--height", type=int, default=int(res[1]), help="expected height (default %(default)s)")
    ap.add_argument("--lufs", type=float, default=float(loud.get("integrated_lufs", -14)), help="target integrated loudness (default %(default)s)")
    ap.add_argument("--tp", type=float, default=float(loud.get("true_peak_dbtp", -1)), help="true peak ceiling in dBTP (default %(default)s)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when there are findings")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print(f"error: {tool} not found; run preflight.py for the install command", file=sys.stderr)
            return 1
    video = Path(a.video).expanduser()
    if not video.is_file():
        print(f"error: not found: {video}", file=sys.stderr)
        return 1

    try:
        info = probe(video)
    except (RuntimeError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    vs = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    au = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    if not vs:
        print("error: no video stream", file=sys.stderr)
        return 1
    duration = float(info.get("format", {}).get("duration") or vs.get("duration") or 0)
    fps = rate(vs.get("avg_frame_rate") or vs.get("r_frame_rate"))
    w, h = int(vs.get("width", 0)), int(vs.get("height", 0))
    tol = float(loud.get("tolerance_lu", 1))
    th = {"black": cr.get("black_min_seconds", 0.5), "freeze": cr.get("freeze_min_seconds", 2.0),
          "silence": cr.get("silence_min_seconds", 1.0), "silence_db": cr.get("silence_db", -50),
          "glitch": cr.get("glitch_scene_score", 0.35)}

    print(f"checking {video.name} ({tc(duration)}) ...", file=sys.stderr)
    r = parse(analyse(video, au is not None, th), fps, duration)

    findings: list[str] = []
    spec_rows = [
        ("Frame rate", f"{a.fps:g}", f"{fps:.3f}".rstrip("0").rstrip("."), abs(fps - a.fps) < 0.01),
        ("Size", f"{a.width}x{a.height}", f"{w}x{h}", (w, h) == (a.width, a.height)),
        ("Video codec", "h264 / hevc / prores", str(vs.get("codec_name")), True),
        ("Audio", "present", f"{au.get('codec_name')} {au.get('sample_rate')} Hz" if au else "none", au is not None),
    ]
    for name, want, got, ok in spec_rows:
        if not ok:
            findings.append(f"{name}: expected {want}, got {got}")
    if au is not None:
        if r["lufs"] is None or abs(r["lufs"] - a.lufs) > tol:
            findings.append(f"Loudness: {r['lufs']} LUFS, target {a.lufs:g} +/- {tol:g}")
        if r["true_peak"] is not None and r["true_peak"] > a.tp:
            findings.append(f"True peak: {r['true_peak']} dBTP, ceiling {a.tp:g}")
    for s, e in r["black"]:
        findings.append(f"Black {tc(s)}-{tc(e)} ({e - s:.2f} s)")
    for s, e in r["freeze"]:
        findings.append(f"Freeze {tc(s)}-{tc(e)} ({e - s:.2f} s)")
    for s, e in r["silence"]:
        findings.append(f"Silence {tc(s)}-{tc(e)} ({e - s:.2f} s)")
    for t in r["one_frame"]:
        findings.append(f"One-frame jump at {tc(t)} (frame {round(t * (fps or a.fps))})")

    lines = [
        f"# Hard-fault check: {video.name}",
        "",
        f"Checked {datetime.now().strftime('%Y-%m-%d %H:%M')} · length {tc(duration)} · "
        f"**{len(findings)} finding{'s' if len(findings) != 1 else ''}**",
        "",
        "This page checks whether the file is correct, not whether the film is good. Every finding is a",
        "place to look; a held frame or a fade to black may be on purpose. Judge by watching.",
        "",
        "## Spec",
        "",
        "| Check | Expected | Got | |",
        "|---|---|---|---|",
    ]
    lines += [f"| {n} | {want} | {got} | {'ok' if ok else 'CHECK'} |" for n, want, got, ok in spec_rows]
    lines += ["", "## Loudness", ""]
    if au is None:
        lines.append("No audio stream.")
    else:
        lines.append(f"- Integrated: {r['lufs']} LUFS (target {a.lufs:g} +/- {tol:g})")
        lines.append(f"- True peak: {r['true_peak']} dBTP (ceiling {a.tp:g})")

    def section(title: str, items: list[tuple[float, float]], note: str) -> None:
        lines.extend(["", f"## {title}", "", note, ""])
        lines.extend([f"- {tc(s)} - {tc(e)} ({e - s:.2f} s)" for s, e in items] or ["None."])

    section("Black", r["black"], f"Black stretches of {th['black']} s or longer.")
    section("Freeze", r["freeze"], f"Picture unchanged for {th['freeze']} s or longer.")
    section("Silence", r["silence"], f"Sound below {th['silence_db']} dB for {th['silence']} s or longer.")
    lines.extend(["", "## One-frame jumps", "", "A picture that changes on one frame and changes back on the next.", ""])
    lines.extend([f"- {tc(t)} (frame {round(t * (fps or a.fps))})" for t in r["one_frame"]] or ["None."])
    lines.extend(["", "## Findings", ""])
    lines.extend([f"- {f}" for f in findings] or ["None."])

    out = Path(a.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(out), "findings": len(findings)}, indent=2))
    return 1 if (a.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
