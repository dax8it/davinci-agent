# Reusable performance-editing lessons

These are starting points learned in one live-band/venue project, not fixed settings for every video.

## Source review

Use Finder tags as user ratings; prioritize explicitly preferred colors/multiple tags. Read macOS metadata rather than relying on filenames; record which tags were actually present. Do not delete lower-rated sources to simplify selection. Inspect promising ranges at several timestamps and in motion. Identify who is singing, playing, dancing or joining from the crowd before writing narration.

Build a source manifest: absolute path, duration, rational fps, rotation/aspect, audio streams, tags, chosen start/end, visible action and confidence. Sources may mix landscape, portrait,24/30/60fps and variable frame rates. Preserve playback speed, fit/crop intentionally and make time mappings explicit for proxies.

## Venue arc and faster pacing

A useful venue/band sequence: exterior/sign → doorway → bar/room → band introduction → varied performances/instruments → food and audience → participation → exterior farewell. Keep each statement aligned with the actual scene. An audience tambourine player is not necessarily the lead singer; a guest singing a request is a separate event.

For a150s fast version, seven performance excerpts around21–22s each supported50–53 visible shots, typically2–3s per shot. Picture-only venue cutaways and same-take detail cuts increased pace while retaining continuous music. A meaningful floor interaction benefited from holds up to7s. Do not force this exact length or shot count onto a30s promo.

Keep synchronized punch-ins modest (roughly1.08–1.14 in the tested portrait footage), and check heads, hands and instruments. Never place prominent singing from another take over mismatched music as if synchronized. A claim of more songs requires actual song identification, not just more filenames.

## Cooler, richer color

Use the user's finished reference and compare equivalent frames. Preserve stage blues/purples and avoid overly warm room tones. Create local color versions so a change does not silently propagate to other timelines. These ASC CDL values were tested as starting points on one set of footage:

| Profile | Slope RGB | Offset RGB | Power RGB | Saturation |
| --- | --- | --- | --- | --- |
| Cool stage | 1.055 1.07 1.11 | -.022 -.022 -.022 | 1.03 1.03 1.03 | 1.08 |
| Cool hazy stage | 1.12 1.14 1.18 | -.04 -.04 -.04 | 1.015 1.015 1.015 | 1.07 |
| Cool venue | 1.035 1.065 1.10 | -.018 -.018 -.018 | 1.015 1.015 1.015 | 1.08 |

For Resolve `SetCDL`, pass these as strings with `NodeIndex='1'`. Color management, camera encoding and exposure affect the result. Inspect scopes/skin/LED highlights, retain shadow detail and adjust shot by shot. These values are not a universal LUT or a guaranteed match on HDR/log media.

## Save, verify, deliver

Before assembly, save/export a backup and refuse colliding timeline/output names. Read each appended clip's source, start and duration back. Keep original audio as a muted reference, with music and voice on independent tracks. A one-time menu launcher can run the guarded operation and write a receipt; retire it once complete.

On failure, inspect the exact partially created timeline. Resume only when its ID/name/ranges match what the operation expects. Test getters on the active timeline when comparing track enable state. Preserve earlier versions and user changes.

Useful export checks include frame count, dimensions, rational fps, audio format, full-file decode, frames spanning every shot and final fade, plus zero-lag audio correlation against the prepared mix. Native success flags alone are insufficient. Watch and listen to the actual output for motion, sync, transitions and intelligibility. Report the full export directory and filename every time.
