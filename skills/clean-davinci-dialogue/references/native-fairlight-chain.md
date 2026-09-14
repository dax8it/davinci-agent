# Native Fairlight Voice Chain

Build on original dialogue or a known derivative with its existing processing accounted for. Preserve edit points and verified sync. No binary preset is bundled; create an inspectable local chain using the settings below and save it under a generic name such as `Dialogue Cleanup`.

## Signal path and adjustable starting settings

1. Reduce noise on the dialogue track before adding substantial gain. Voice Isolation is a Studio feature and is not assumed available in Resolve 19 Free. If verified available for a spoken-only segment, start conservatively and increase only while checking quiet consonants and tails. An amount of 75 is an optional trial setting, not a required value. Identify unavailable features instead of silently claiming equivalent processing.
2. Use a gentle downward expander for remaining pause noise. An optional starting shape is ratio 1.3:1, range about 10 dB, attack 1.4 ms, hold 1.5 ms, and release 93 ms. Derive the threshold from the actual noise floor and quietest wanted speech.
3. For compression, try ratio 2.7:1, attack 24 ms, hold 0, and release 50 ms. Adjust threshold, knee, and wet/dry balance while listening. Set makeup gain from measured output loudness; there is no fixed gain boost for all recordings.
4. Put peak protection after track makeup gain. A bus dynamics limiter can provide intermediate protection, but verify final true peak with the actual render. If available, a dedicated true-peak limiter near the end of the output chain is useful. Start with a ceiling around -2 dBTP, then adjust to retain encoding headroom.
5. Keep routing and bus gain explicit. Start faders at a known value and calibrate from a rendered pass. Avoid processing a baked dialogue file twice.

Use approximately -16 LUFS and true peak below -1.5 dBTP as initial voice-only working targets unless the user specifies different delivery requirements. Measure the encoded result; knob values do not certify loudness or peak compliance. Do not apply voice settings to unrelated music or sound effects.

## Control and preset creation

Discover the capabilities of the available Resolve MCP or scripting API. Use supported operations for media identity, timeline positions, effect availability, preset discovery, rendering, and saving. Tool names differ between integrations. Use native Fairlight controls when supported automation cannot expose the needed dynamics or effect parameters.

Open the dialogue track's Dynamics panel to configure and save a dynamics preset. A separate dialog may own the name field; inspect the current window rather than reusing coordinates or handles. Verify that the saved preset appears and recalls the intended values.

A dynamics preset does not include the whole voice chain. To save track and bus configuration, use Fairlight's Presets Library and the Fairlight Configuration Presets category where available. Save a new, generically named local preset; inspect any update or replacement prompt before overwriting an existing one. Do not assume a full configuration is safe to recall over a timeline containing music and sound effects.

Test full preset recall in a disposable voice-only timeline. Inspect noise reduction, dynamics, limiters, routing, and fader levels. Read values back after editing effects; numeric entry and mouse gestures may behave differently between versions.

## Verification

Render a QC pass and measure integrated loudness, true peak, and the same quiet source-time windows used before processing. Listen to quiet speech, word endings, and speech-to-pause transitions for truncation, pumping, or artifacts. Compare original and processed waveforms to verify duration and latency compensation. Preserve linked picture, source coverage, and measured sync offsets.

Retain a recoverable preparation timeline with the editable chain and original media. If a rendered-audio derivative is requested or needed for measured playback problems, export full-coverage 48 kHz, 24-bit PCM WAV, verify it, and bypass the processing already baked into the working copy. Keep measurements and project backups with the user's project, outside any public skill distribution.
