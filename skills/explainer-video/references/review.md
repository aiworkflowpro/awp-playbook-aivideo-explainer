# How to review a cut

Read when a builder reviews its own stills (Steps 04-05), when the main agent checks seams
(Step 06), and for the polish and second pass (Step 07). The aim: before any viewer sees it, find
what looks fake, cannot be read, cannot be followed or sounds wrong, then find better ideas.

## Watch first; code only checks hard faults

Passing checks and scores do not tell you whether a film is good: a model can rate ten dimensions
highly and the film still plays like a slide deck. So taste is not scored. In this order:

1. **The whole film once, like a viewer**, without pausing. Then write where you were hooked,
   drifted, did not understand, were pulled out, or felt it was cheap.
2. **Contact sheets and full-size frames**, to find where each feeling came from. Report only what
   you confirmed.
3. **Side by side with something better**: a film you admire, the reference, or your own earlier
   version, at the same kind of moment.
4. **A verdict in sentences**: "good enough", or "fix these three things, because...". When notes
   conflict, emotion beats story, and story beats rhythm.

Code decides whether the film is **correct**, never whether it is good: `scripts/check_render.py`
and FFmpeg for format, frame rate, loudness, true peak, black or frozen stretches, dead silence,
single-frame flashes (list the suspect times, then look at each), and caption timing. Frame
numbers, times and colors are measured, never asked of a model.

A model watching video samples frames, so motion can look like a jump and a slow pan like none.
Judge smoothness and freezes from frame-to-frame data, and reproduce any reported problem on
stills or by measurement before fixing it.

## Where defects hide

Settled frames lie. Look hardest at mid-entrance and mid-exit, the frames either side of a cut, and
the joins between segments built in parallel. Log defects by kind so you can find the rest of
their kind:

| Kind | Examples |
|---|---|
| Overlap | something that belongs inside shows outside; text cut by a card; things passing through each other |
| Tilt | a settled object crooked or wobbling |
| Crop | text cut by an edge or an address bar |
| Empty | a large area with nothing in it for a long time |
| Jump | something appearing or vanishing in one frame; the presenter jumping |
| Text | too small, missing characters, typos, font not loaded |
| Sound | wrong-material effects, clipping, audible seams, dead silence |
| Sameness | several segments in a row staged alike; one composition held too long. A defect only on the whole film (Step 07) |

## What to look at on stills

Each round, look at the **whole segment as a strip** (one or two frames per beat, in time order)
regenerated from the current code with the same frame numbers; a strip mixing two rounds fools you.
Ask: is the subject full or empty? Readable at phone width? Several frames with nearly the same
composition (held too long)? Is it obvious where to look? Does it stand next to the reference moment?

## Finding better ideas

Reviewing is not only finding faults. After a straight watch, answer:

1. **Which beat is the most ordinary?** The one you remember least, the one that would fit any film.
2. **If you could redo only three, which, and as what?** Pick where a redo would help the viewer
   most, with two or three alternative ideas each, one sentence on what they would see and feel.
3. **Where is it held too long, empty or repeating?** A builder looks inside its segment; the
   polish looks across segments.

## Fixing

- A problem in two or more places may live in the shared layer: fix it there once.
- Better ideas and sameness go to the polish. If a whole segment must be rebuilt, ask the user first.
- Take a before and after still of every fix; write a reason for anything left.
- After the whole film is re-rendered, watch once more for regressions. The new version is not
  automatically better; when in doubt, compare section by section without knowing which is which.

## When it is done

Every flagged hard fault is intentional or fixed, the second watch finds no new high or medium
problems, and the user signs off.
