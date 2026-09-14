---
name: first-cut-davinci-dialogue
description: Select and tighten interviews, podcasts, tutorials, talking heads and other spoken material in DaVinci Resolve using word timings, waveforms and listening. Preserve meaning and synchronized layers; use edit-davinci-video for general visual assembly.
---

# DaVinci Dialogue First Cut

## Resolve 19 access

Read [the Resolve 19 macOS profile](../edit-davinci-video/references/resolve19-macos.md) before inspection or editing. In Resolve Free, use the verified in-process Lua console and native UI; installing skills does not install an MCP server. Respect the current project brief and refresh live state after user activity.

## Scope for spoken edits

This skill edits speech. Preserve complete thoughts, speaker intent and the requested instructional or narrative order. Do not treat lyrics, instrumental space, audience response, count-ins, sustained notes, or intentional musical repetition as failed dialogue takes. A live performance camera switch is a picture edit over continuous audio; it does not require a cut in the master audio. Use `edit-davinci-video` for performance structure and venue coverage.

## Dialogue workflow

1. Inspect the active project and timeline, source ranges, existing manual edits, track locks, targeting, and sync offsets. Preserve a recoverable version before structural changes. Keep unrelated music and effects outside the edit.
2. Review complete spoken thoughts and select usable deliveries. Remove abandoned or redundant speech only within the requested scope; retain meaningful pauses, interaction, and context. Do not automatically choose the last take.
3. Obtain word-level timings aligned to the original source and inspect the waveform at every proposed join. Read [waveform-word-timing.md](references/waveform-word-timing.md). ASR and forced alignment are estimates. Check incoming and outgoing phonemes and surrounding context before trimming. Sentence timestamps or silence detection alone are insufficient.
4. Check sound preparation with `clean-davinci-dialogue` only where needed. Existing usable audio does not require a forced cleanup render. Keep live editable effects unless a derivative is requested or needed for measured playback problems.
5. For an authorized removal of spoken time, cut all participating synchronized layers at the same timeline frame and preserve source offsets. Check selected/locked tracks before ripple operations and verify every affected boundary afterward. This requirement does not apply to picture-only performance camera switches.
6. Use `smooth-davinci-audio-cuts` for the actual dialogue seams. A centered two-frame Cross Fade 0 dB is an optional speech starting point, adjusted by listening and available handles. Keep continuous music beds uncut. Do not change global shortcut or transition preferences by default.
7. Audit both edges of every changed join against the assembled signal; preserve quiet consonants and word tails without restoring discarded fragments. Maintain a project-local join record with source IDs/ranges, timeline frames, word/phoneme evidence, fade, and audition status. Recheck neighboring joins after ripple changes.
8. Listen at normal speed before calling a cut audibly verified. If listening or word alignment is unavailable, finish supported inspection, provide review material, and mark unresolved edges explicitly. Save the edit and identify the working timeline.

Do not apply dialogue pacing to music or unrelated visual sequences or rebuild the user's existing edit merely to impose a workflow order.
