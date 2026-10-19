#!/usr/bin/env python3
"""Step 03 clock: word-level timings (words.json) and captions (captions.srt) from a voiceover.

    python3 transcribe_words.py audio/voiceover.wav --out-dir audio/
    python3 transcribe_words.py audio/voiceover.wav --out-dir audio/ --engine whisper-cpp --model ggml-small.en.bin
    python3 transcribe_words.py --from-words audio/words.json --out-dir audio/   # rebuild the SRT after proofreading

Runs a Whisper installed on this machine, never a paid API:
  openai-whisper  the `whisper` command (pipx install openai-whisper)
  whisper.cpp     the `whisper-cli` command plus a ggml model file (set transcribe.whisper_cpp_model in config.json)
`--engine auto` (the default) uses openai-whisper if found, then whisper.cpp.

words.json shape (the clock every segment hangs on):
  {"source": "voiceover.wav", "duration": 312.48, "words": [{"text": "Hello", "start": 0.21, "end": 0.48}, ...]}
Times are seconds. Proofread the text against the final script; keep the times.

Captions: one line of at most 42 characters, a new cue at a sentence end, at a pause longer than
0.6 s or after 6 s, and no cue shorter than 0.8 s (all set in config.json). Captions are a
separate track, never burned into the picture.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent

INSTALL_HINT = (
    "No local Whisper found. Install one of:\n"
    "  pipx install openai-whisper\n"
    "  whisper.cpp: https://github.com/ggml-org/whisper.cpp (then set transcribe.whisper_cpp_model in config.json)\n"
    "Or, if you already have word-level timings from another tool, convert them to the words.json shape\n"
    "and run: transcribe_words.py --from-words words.json --out-dir audio/"
)


def load_config() -> dict[str, Any]:
    try:
        return json.loads((SKILL_DIR / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def fail(msg: str, code: int = 1) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return code


def probe_duration(path: Path) -> float | None:
    exe = shutil.which("ffprobe")
    if not exe:
        return None
    r = subprocess.run(
        [exe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=False,
    )
    try:
        return round(float(r.stdout.strip()), 3)
    except ValueError:
        return None


def clean_word(text: str) -> str:
    return " ".join(text.split())


def run_openai_whisper(audio: Path, model: str, language: str | None, tmp: Path) -> list[dict[str, Any]]:
    exe = shutil.which("whisper")
    if not exe:
        raise RuntimeError("the `whisper` command (openai-whisper) was not found")
    cmd = [exe, str(audio), "--model", model, "--word_timestamps", "True",
           "--output_format", "json", "--output_dir", str(tmp), "--verbose", "False"]
    if language:
        cmd += ["--language", language]
    print("running: " + " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)
    out = tmp / (audio.stem + ".json")
    data = json.loads(out.read_text(encoding="utf-8"))
    words: list[dict[str, Any]] = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []) or []:
            text = clean_word(str(w.get("word", "")))
            if text:
                words.append({"text": text, "start": round(float(w["start"]), 3), "end": round(float(w["end"]), 3)})
    return words


def run_whisper_cpp(audio: Path, binary: str, model: str | None, language: str | None, tmp: Path) -> list[dict[str, Any]]:
    exe = shutil.which(binary)
    if not exe:
        raise RuntimeError(f"the `{binary}` command (whisper.cpp) was not found")
    if not model or not Path(model).expanduser().is_file():
        raise RuntimeError("whisper.cpp needs a ggml model file: pass --model PATH or set transcribe.whisper_cpp_model in config.json")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is needed to convert the audio to 16 kHz mono for whisper.cpp")
    wav = tmp / "input-16k.wav"
    subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(audio),
                    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)], check=True)
    base = tmp / "out"
    cmd = [exe, "-m", str(Path(model).expanduser()), "-f", str(wav), "-ml", "1", "-sow", "-oj", "-of", str(base)]
    if language:
        cmd += ["-l", language]
    print("running: " + " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)
    data = json.loads((tmp / "out.json").read_text(encoding="utf-8", errors="replace"))
    words: list[dict[str, Any]] = []
    for item in data.get("transcription", []):
        raw = str(item.get("text", ""))
        text = clean_word(raw)
        if not text:
            continue
        off = item.get("offsets", {})
        start, end = float(off.get("from", 0)) / 1000.0, float(off.get("to", 0)) / 1000.0
        if words and not raw.startswith(" "):
            # whisper.cpp may split one word into pieces; a piece without a leading space joins the previous word
            words[-1]["text"] += text
            words[-1]["end"] = round(end, 3)
            continue
        words.append({"text": text, "start": round(start, 3), "end": round(end, 3)})
    return words


def build_cues(words: list[dict[str, Any]], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    max_chars = int(cfg.get("max_chars_per_line", 42))
    max_sec = float(cfg.get("max_seconds", 6))
    pause = float(cfg.get("pause_break_seconds", 0.6))
    min_sec = float(cfg.get("min_seconds", 0.8))
    cues: list[dict[str, Any]] = []
    cur: dict[str, Any] | None = None
    for w in words:
        text = str(w["text"]).strip()
        if not text:
            continue
        start, end = float(w["start"]), float(w["end"])
        if cur is not None:
            joined = cur["text"] + " " + text
            if len(joined) > max_chars or start - cur["end"] > pause or end - cur["start"] > max_sec:
                cues.append(cur)
                cur = None
        if cur is None:
            cur = {"text": text, "start": start, "end": end}
        else:
            cur["text"] += " " + text
            cur["end"] = end
        if text.endswith((".", "?", "!", "...")):
            cues.append(cur)
            cur = None
    if cur is not None:
        cues.append(cur)
    for i, c in enumerate(cues):
        if c["end"] - c["start"] < min_sec:
            limit = cues[i + 1]["start"] if i + 1 < len(cues) else c["start"] + min_sec
            c["end"] = max(c["end"], min(c["start"] + min_sec, limit))
    return cues


def srt_time(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues: list[dict[str, Any]], path: Path) -> None:
    lines: list[str] = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_time(c['start'])} --> {srt_time(c['end'])}", c["text"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_words(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict) or not isinstance(data.get("words"), list):
        raise ValueError('expected {"words": [{"text", "start", "end"}, ...]}')
    out: list[dict[str, Any]] = []
    prev = -1.0
    for i, w in enumerate(data["words"]):
        try:
            item = {"text": str(w["text"]), "start": float(w["start"]), "end": float(w["end"])}
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"word {i} is missing text/start/end") from e
        if item["end"] < item["start"]:
            raise ValueError(f"word {i} ({item['text']!r}) ends before it starts")
        if item["start"] < prev - 0.001:
            raise ValueError(f"word {i} ({item['text']!r}) starts before the previous word")
        prev = item["start"]
        out.append(item)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", nargs="?", help="voiceover audio (wav, mp3, m4a, ...)")
    ap.add_argument("--out-dir", required=True, help="folder for words.json and captions.srt (usually audio/)")
    ap.add_argument("--engine", choices=["auto", "openai-whisper", "whisper-cpp"], help="default: transcribe.engine in config.json")
    ap.add_argument("--model", help="openai-whisper model name (e.g. small, medium) or whisper.cpp ggml model path")
    ap.add_argument("--language", help="language code, e.g. en (default: detect)")
    ap.add_argument("--from-words", metavar="WORDS_JSON", help="skip transcription: validate this words.json and rebuild captions.srt from it")
    a = ap.parse_args()

    cfg = load_config()
    tcfg, ccfg = cfg.get("transcribe", {}), cfg.get("captions", {})
    out_dir = Path(a.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    if a.from_words:
        src = Path(a.from_words).expanduser()
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
            words = validate_words(data)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            return fail(f"{src}: {e}")
        target = out_dir / "words.json"
        if target.resolve() != src.resolve():
            target.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        if not a.audio:
            return fail("give an audio file, or --from-words words.json")
        audio = Path(a.audio).expanduser()
        if not audio.is_file():
            return fail(f"audio not found: {audio}")
        engine = a.engine or tcfg.get("engine") or "auto"
        cpp_bin = tcfg.get("whisper_cpp_binary") or "whisper-cli"
        if engine == "auto":
            if shutil.which("whisper"):
                engine = "openai-whisper"
            elif shutil.which(cpp_bin):
                engine = "whisper-cpp"
            else:
                print(INSTALL_HINT, file=sys.stderr)
                return 1
        language = a.language or tcfg.get("language")
        try:
            with tempfile.TemporaryDirectory(prefix="transcribe-") as td:
                tmp = Path(td)
                if engine == "openai-whisper":
                    words = run_openai_whisper(audio, a.model or tcfg.get("openai_whisper_model") or "small", language, tmp)
                else:
                    words = run_whisper_cpp(audio, cpp_bin, a.model or tcfg.get("whisper_cpp_model"), language, tmp)
        except RuntimeError as e:
            print(INSTALL_HINT, file=sys.stderr)
            return fail(str(e))
        except subprocess.CalledProcessError as e:
            return fail(f"transcription failed (exit {e.returncode})")
        if not words:
            return fail("no words came back; check the audio")
        data = {"source": audio.name, "duration": probe_duration(audio) or words[-1]["end"], "words": words}
        (out_dir / "words.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    cues = build_cues(words, ccfg)
    write_srt(cues, out_dir / "captions.srt")
    print(json.dumps({"words": len(words), "cues": len(cues),
                      "words_json": str(out_dir / "words.json"), "captions_srt": str(out_dir / "captions.srt"),
                      "last_word_end": words[-1]["end"] if words else None}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
