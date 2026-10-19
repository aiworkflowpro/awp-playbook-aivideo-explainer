# Step 03: Narration & segments

Video: 12:11

> **Who**: the main agent
> **In**: the voiceover (or script), `plan/context.md`, `plan/materials.md`, the user's requests
> **Out**: `audio/voiceover.wav`, `audio/words.json`, `audio/captions.srt`,
> `plan/narration-logic.md`, `plan/segments.md`, `handoff/03-narration-and-segments.md`

## Goal

Lock the narration, then cut it into segments. This is the core step: everything after it is
handed to sub-agents, and all of them work from what is decided here.

A film has two tracks, the voice and the picture, and one must hold still: the voice. Tighten
pauses, cut slips and repeats, time every word, finish the captions, lock it. From here the voice
is the clock: things on screen hang on words. If it moves later, cutting one word shifts
everything after it and every shot is redone.

Then cut it twice: by meaning into segments of about three minutes, each one idea; and by breath
into beats of roughly 1.5-4 seconds, each one change on screen. Write what each segment must make
the viewer understand and feel. How it is staged is left to whoever builds it.

Read first: `references/captions.md`, `templates/segments.md`, sections 1-2 of `references/quality-standard.md`.

## Do

1. **Read it as a script first.** Is the message clear, the hook in place, does every setup pay
   off? Something real should happen in the first 15 seconds: no greeting, no subscribe request.
   If it is weak, tell the user now, before the lock; pictures cannot rescue it. Do not rewrite
   the narration yourself.
2. **Cut the recording.** A read script usually needs only shorter silences. Free talk also loses
   verbal tics, restarts, repeats and on-screen chatter. Work from an edit list (one line per
   piece, anchored to a phrase, not a time); snap cuts to the quietest point, round to whole
   frames, add 12-25 ms fades. Show the user the list if content (not just silence) goes. A
   recorded voice is only cut, never regenerated. Fill removed silence with room tone.
3. **Transcribe the final audio** with a time on every word, and again if the audio ever changes:

   ```bash
   python3 <skill-folder>/scripts/transcribe_words.py audio/voiceover.wav --out-dir audio/
   ```

4. Word times can be off by almost half a second after a pause: check each sentence's first word
   against the waveform onset.
5. **Finish the captions now**: proof `words.json` against the audio word by word, at least two
   passes (`references/captions.md`), then rebuild the SRT from the proofed words:

   ```bash
   python3 <skill-folder>/scripts/transcribe_words.py --from-words audio/words.json --out-dir audio/
   ```

6. Add the voiceover, `words.json` and SRT to `plan/materials.md`; copy `voiceover.wav` and
   `words.json` into `app/public/` and set `VOICEOVER` in `app/src/film.config.ts`. Never edit the
   copies. **Lock it.** Changing the locked voice is the user's decision and redoes this step.
7. `plan/narration-logic.md`: the film's argument in one sentence, the big blocks, and the order
   inside each (question, answer, example, conclusion), pointing at sentences.
8. **Segments, by meaning.** One complete argument each, never cut by length alone; about three
   minutes (`config.json`), merge anything under 1.5 minutes into a neighbor. A film of three
   minutes or less is one segment. Per segment (`templates/segments.md`): word range and length,
   **goal** (what the viewer should understand, and why it matters), **feeling** (an effect, not a
   picture), argument order, presenter (large / corner / hidden / builder decides), and what is on
   screen in its first and last frames.
9. **Needs, not staging.** No candidate visuals, no "put a card here", no search terms. Whatever
   is written here gets built literally, and every segment starts to look the same.
10. **Entry and exit are the only agreement between segments.** By default both return to the bare
    stage with the presenter in the agreed position. If something must carry across a boundary,
    write what and who designs it (by default the earlier segment).
11. **Beats, by breath.** Cut at punctuation and real pauses; record only id, start, word range
    and sentence. Check each cut against the waveform gap: a cut on a word time alone can land
    inside a word.

## Pass when

- The script check was done; weaknesses were told to the user before the lock.
- `words.json` read back matches the audio; captions were proofed twice and rebuilt.
- Every edit seam was listened to.
- Segments are contiguous, end on topic boundaries, run about three minutes, and have the entries
  above. Every beat has a word range and sits on a pause.
- `plan/segments.md` contains no staging (search it for "card", "show", "animate", "3D").

## Hand off

`handoff/03-narration-and-segments.md`: what was cut, the proofing passes, final length, then one
row per segment (time, what to understand, what to feel, beats). If content was removed or
reordered, the user's yes goes into "User's requests". Next: Step 04.
