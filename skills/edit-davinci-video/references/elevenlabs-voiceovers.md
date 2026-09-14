# ElevenLabs narration for performance and venue videos

Use when the user authorizes voiceover creation. The tested path was ElevenLabs REST plus local mixing and Resolve import; no ElevenLabs MCP was installed. An available MCP may be used instead after inspecting its actual capabilities and credential setup. Codex authentication is separate from ElevenLabs authentication.

## Credentials and generation

The companion repository includes `scripts/elevenlabs_client.py`. Set `ELEVENLABS_API_KEY` in the execution environment, or set `DAVINCI_ELEVENLABS_ENV_FILE` to the exact private environment file containing it. The helper prefers the direct environment variable. It reads the file as text; it never sources or executes it. Do not put real keys in this repository, command history, chat or generated reports.

For a Hermes profile, point to the active profile's file, such as `~/.hermes/profiles/PROFILE_NAME/.env`; updating a desktop profile may not update `~/.hermes/.env`. Check the selected file without displaying its value. An invalid key cannot be repaired through Resolve settings.

From the companion repository root:

```sh
export DAVINCI_ELEVENLABS_ENV_FILE="$HOME/.config/private/elevenlabs.env"
python3 scripts/elevenlabs_client.py inspect --output reports/voices.json
python3 scripts/elevenlabs_client.py generate \
  --voice VOICE_ID_FROM_INSPECTION \
  --text-file /absolute/path/narration/beat-01.txt \
  --output /absolute/path/narration/beat-01-v1.mp3 \
  --stability 0.4 --similarity 0.75 --style 0.08
```

The private file needs a line `ELEVENLABS_API_KEY=your_actual_key`, entered in a private editor. Protect it with restrictive filesystem permissions. Do not commit it. `inspect` reads available voices without generating speech. Account permissions and available voices can vary. The tested model was `eleven_multilingual_v2`; the helper accepts `--model` to select another verified model. MP3 generation uses `mp3_44100_128`. Decode/resample to stereo48k WAV for mixing.

`generate` is billable against the account. It refuses existing output files and reserves the path before requesting speech. A failed/uncertain request leaves an empty reservation: check the provider request history before deleting that placeholder and retrying. There are no automatic retries. A401 generally calls for credential correction;403 can mean missing permission/access;429 can mean throttling or quota. Do not repeatedly generate to diagnose authentication.

## Natural delivery and accurate description

- Write short conversational beats linked to visible events: arriving, entering, seeing the band, room details, audience interaction, closing.
- Introduce both the band and venue explicitly. Vary phrasing across versions; give each voice a coherent personality rather than changing speakers mid-sentence.
- Use contractions, specific observations and occasional pauses. Avoid filling every second or repeating generic praise.
- In the tested edits Laura (American female), Will (American male) and George (British male) were effective stock choices. Inspect current availability; names and IDs are not guaranteed. Stability roughly.38–.43, similarity.75, style.08 and speaker boost were useful starting points, not universal settings.
- Generate each beat separately at natural speed. Rephrase or reposition if it runs long rather than automatically speeding it up. Measure the actual duration and check overlap.
- Verify the person/action before narrating it. In our source review, an audience member playing tambourine was initially mistaken for the singer. The correction changed only that beat; separate footage genuinely showed the lead singer on the floor. Never infer identity from clothing, proximity to the stage or a single small thumbnail alone.
- Do not claim a song title without verification. Distinct source recordings may repeat a song.

## Mix against the band

Keep independent48k stereo stems: A1 performance mix, A2 original synchronized reference muted, A3 narration. Preserve real-time musical content and picture/audio offsets. Do not treat singing as removable speech or apply dialogue gates to the entire performance.

Tested starting points: narration approximately-17LUFS with-4dBTP headroom; individual performance excerpts approximately-16LUFS while preserving at least-3dBTP headroom. Under voice, reduce music about12dB with a.4s attack before the line and.85s recovery after it. Use the gentler gain when a loudness target would exceed peak headroom. These are starting points; audition the final mix and compare the reference.

For an offline gain envelope, take the minimum across overlapping speech windows. For window[a,b], attack A, recovery R and duck depth D:

`gain(t) = 1 - (1 - 10^(-D/20)) * min(clamp((t-a+A)/A,0,1), clamp((b+R-t)/R,0,1))`

Music should recover between lines so the band gets heard. Place commentary over weak/broken audio where editorially appropriate, but do not claim it repairs clipped or crackling source recordings. Our150s edits used eight beats totaling roughly55–59s, leaving about90s without narration. Scale the pattern to the requested duration.

At actual song joins, a.3s equal-power crossfade with.15s source handles on each side preserved picture/audio positioning. Check available handles; do not insert silence or shift the song to fake a crossfade. Same-take detail cuts retain continuous audio.

## Corrections and delivery

If only one line is wrong, preserve the original timeline/export, generate only the replacement beat, then adjust the voice stem and affected ducking window. Verify audio outside that interval is unchanged. Duplicate the native timeline and replace only the relevant stems; verify its picture and color state against the original.

When picture is fully approved, an audio-only export correction can copy the existing H.264 video stream and encode new AAC audio. Report that honestly as a preserved-picture/audio replacement, and maintain a matching editable timeline. Compare video stream hashes, duration, stream metadata and full decode; compare exported audio against the prepared mix.

Listen to each generated line and transitions. ASR can catch wrong words but is not a listening pass. Full decode, loudness readings, frame samples and correlation cannot prove the complete viewing/listening experience. State remaining review limits.

API reference: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
