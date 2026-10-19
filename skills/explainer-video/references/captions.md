# Captions

Read in Step 03 (captions are finished there) and Step 07 (exported there). Three rules:

1. **Captions are never burned into the picture.** They are a separate track (SRT or the
   platform's format). A wrong word in burned-in captions means redoing the video; a track can be
   fixed any time. The only exception is an explicit request from the user or the platform.
2. **Captions are finished before the edit**, in Step 03, right after the voice is locked. Every
   word anchor is built on the same transcript; proofed late, every cut was timed against
   unproofed text.
3. **The word-level transcript is both the clock and the caption track.** `audio/words.json` gives
   every word a start and an end. The picture hangs on those words; the SRT is generated from them,
   so they cannot drift apart.

## Make the transcript

Transcribe the **final** voiceover with a time on every word:

```bash
python3 <skill-folder>/scripts/transcribe_words.py audio/voiceover.wav --out-dir audio/
```

The script runs openai-whisper or whisper.cpp (`config.json` or `--engine`) and writes `words.json`
and `captions.srt`. If you already have word timings from another tool, convert them to this shape
and skip transcription:

```json
{ "source": "voiceover.wav", "duration": 312.48,
  "words": [ { "text": "One", "start": 0.12, "end": 0.31 } ] }
```

If the user films themselves, the audio of the final cut of that recording is the clock.

## Proof it

- At least two passes against the final audio, word by word. Pass 1: listen while reading the
  words and fix every misheard one. Pass 2: names, numbers, product and technical terms, and words
  that sound alike.
- Fix text in `words.json`, keeping each word's times; if a word was split or merged wrongly, split
  or merge the entry and share out its times.
- Word times can be off by almost half a second, most often at the first word after a pause. Move
  sentence-initial words to the waveform onset.
- Note the passes and changes in the Step 03 handoff, then rebuild the SRT:

```bash
python3 <skill-folder>/scripts/transcribe_words.py --from-words audio/words.json --out-dir audio/
```

## Caption style

Defaults in `config.json`, changeable for the platform: at most 42 characters per line, one line;
a new caption at a sentence end, a pause over 0.6 s, or after 6 s; none shorter than about 0.8 s
unless the speech is; numbers as spoken.

## Delivery

In Step 07 export the format the platform asks for from the same SRT and spot-check a few lines.
Do not transcribe again. If a check fails, fix `words.json`, rebuild, and re-check anything
anchored to the changed words.
