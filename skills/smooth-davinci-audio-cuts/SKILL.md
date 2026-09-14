---
name: smooth-davinci-audio-cuts
description: Inspect and smooth audio joins in DaVinci Resolve 19 while preserving sync, musical continuity, and manual edits. Use for short dialogue crossfades or selected music, ambience and effects transitions, with fade shape and duration matched to the material.
---

# DaVinci Audio Crossfades

## Resolve 19 access

Read [the Resolve 19 macOS profile](../edit-davinci-video/references/resolve19-macos.md) before inspection or editing. In Resolve Free, use the verified in-process Lua console and native UI; installing skills does not install an MCP server. Respect the current project brief and refresh live state after user activity.

## Choose which seams need a fade

A picture-only cut, B-roll insertion or switch between synchronized cameras normally leaves the chosen dialogue, music or ambience bed continuous. Do not cut that master, fade every camera scratch track, or introduce a music transition merely because picture changes.

For dialogue, a centered **Cross Fade 0 dB, two frames** is a starting option, not a project-wide rule. For a change of song excerpt, audio recording, or venue sequence, choose handles, shape, and duration from the actual musical phrase and ambience. Equal-power fades can help uncorrelated material but can produce a bump with correlated recordings. Overlapping microphones can cause comb filtering or doubled transients; check polarity, phase, sync, and mono compatibility rather than blindly stacking them.

## Apply and verify

1. Inspect the current timeline, selected seams, track locks, source handles, existing transitions, and master audio. Preserve a recoverable version before a batch.
2. Use native Effects and Transition Inspector controls on Resolve 19 Free. The shipped SDK has no documented general API for adding/reading audio transitions. Do not invent methods or infer success from a shortcut.
3. Prefer setting the requested transitions directly. Inspect the active keyboard preset before using a shortcut. Change a shortcut or global Standard transition duration only if requested or necessary within the authorized task. Explain that the global duration also affects video transitions; do not silently remap Shift+D.
4. Select only the intended audio edit points. Exclude actual gaps, continuous music, unrelated effects, and unwanted outer edges. A batch is appropriate only after confirming the selection and current default transition. Restore temporary selection/linking state.
5. Inspect every required seam for actual type, exact frame duration, centered alignment where intended, and sufficient handles. Use the frame field rather than rounded seconds. Do not move an established cut or ripple the timeline merely to manufacture handles. Report unresolved seams by track and timecode.
6. For dialogue, use the [word-timing join record](../first-cut-davinci-dialogue/references/waveform-word-timing.md) to protect initial/final phonemes. For music, preserve the attack, beat, note tail, phrase, and room continuity. Audition the assembled transition and recheck sync. A fade cannot restore missing speech or a clipped musical attack.
7. Save within the authorized edit and distinguish transition readback, waveform analysis, and actual listening. A shortcut-configuration test alone may be undone on a disposable edit point; do not undo unrelated user actions.
