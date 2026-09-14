---
name: clean-davinci-dialogue
description: Clean and level dialogue in DaVinci Resolve 19 for interviews, podcasts, tutorials, voiceovers and spoken event segments while preserving editable processing and sync. Treat speech separately from music, ambience and effects.
---

# DaVinci Dialogue Cleanup

## Resolve 19 access

Read [the Resolve 19 macOS profile](../edit-davinci-video/references/resolve19-macos.md) before inspection or editing. In Resolve Free, use the verified in-process Lua console and native UI; installing skills does not install an MCP server. Respect the current project brief and refresh live state after user activity.

## Choose the audio scope

Identify the intended dialogue, interview, narration or other spoken segment/track first. Do not apply a speech gate, Voice Isolation, speech loudness target, or silence removal across music, singing, applause, crowd reactions, or reverberation tails. Never ripple-delete time as part of cleanup. Preserve other sound roles and established picture/audio sync.

## Prepare and verify

1. Inspect source identity, channel layout, existing processing, source ranges, and signed audio offsets. Preserve the original media and a recoverable working version before changing sound.
2. Prefer editable native Fairlight EQ and Dynamics. Read [native-fairlight-chain.md](references/native-fairlight-chain.md) for adjustable voice-only starting settings. Studio-only processors must not be assumed available in Free. Use visible controls and read settings back; Resolve 19's documented API does not expose general Fairlight plugin-parameter control.
3. Measure actual speech, quiet word onsets, tails, and the same noise windows before and after processing. Reduce noise conservatively before raising level; do not sacrifice consonants or room naturalness to a low meter reading.
4. Use approximately -16 LUFS and below -1.5 dBTP only as provisional voice-only working targets. The final program target depends on the brief and delivery platform. Measure the actual encoded output instead of predicting it from fader values.
5. Keep effects live by default. If the user requests baked audio, or measured playback problems require it, render a separate full-coverage 48 kHz, 24-bit PCM WAV with a versioned filename. Preserve channel layout and duration, measure content alignment/latency, retain the original and editable chain, and bypass processing already baked into the derivative. Do not force a bounce of every imported clip.
6. For requested dialogue trimming, use [waveform and word timing](../first-cut-davinci-dialogue/references/waveform-word-timing.md). Cleanup alone does not establish safe edit points. Music review uses musical phrases and listening, not a speech detector.
7. Audition a short before/after and affected transitions. Distinguish measurements from listening; if direct listening is unavailable, provide the comparison for user review and report that limitation. Save verified settings and measurements beside the project.
