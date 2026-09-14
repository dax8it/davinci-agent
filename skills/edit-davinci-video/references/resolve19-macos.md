# Resolve 19 on macOS

These four skills are workflow instructions. `agents/openai.yaml` supplies display metadata; neither it nor Codex OAuth connects to Resolve or unlocks Studio features. A model choice affects reasoning, not Resolve licensing. No API key, paid transcription service, MCP server, or background listener is required for the internal console workflow.

## Connection

Resolve 19 Free supports in-process scripting in **Workspace > Console > Lua**. Use the existing `resolve` object or `app:GetResolve()`. This route was verified locally on **19.1.4.11 Free**. External scripting is a Studio feature; environment variables cannot enable it in Free. UIManager-based scripts also require Studio in 19.1. Use short scoped scripts and native controls, not a persistent polling loop that can block imports or editing.

For Studio, use an available configured integration only after verifying the connection. Local scripting is sufficient; network access is unnecessary here. Missing settings or null `scriptapp('Resolve')` results do not justify licensing changes, binary patches, downgrades, or open ports.

The installed vendor SDK is the method reference:

`/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt`

The correct Python library on this installation is:

`/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so`

The suggested `Contents/Libraries/libFusion.dylib` does not exist here. [probe_external.py](../scripts/probe_external.py) configures only its process and bounds connection time. It does not edit `.zshrc`; desktop processes need not inherit interactive shell settings. Module import alone is not a live connection.

## Read-only audit

On this workspace, prefer the verified **Workspace > Scripts > Codex - Resolve 19 read-only audit** menu entry. It writes a fresh audit plus render-queue status without requiring Console to be visible. The companion repository's `scripts/install_menu_audit.py --project 'Your Project Name'` installs this read-only entry; see its Resolve19.1 quick-start guide. Installed skill folders alone do not install the menu entry. Console activation is unreliable through the current UI bridge; do not paste into an unverified window. Scripts in the personal `Fusion/Scripts/Utility` folder are supported by the installed SDK and were live verified on this Free build.

Inspect current UI before acting so a user action or import dialog is not interrupted. Open the requested project and **Workspace > Console**, select **Lua**, and execute using actual absolute paths:

```lua
dofile('/absolute/path/edit-davinci-video/scripts/inspect_resolve.lua')({expected_project='Your Project Name', output_path='/absolute/project/reports/new-audit.json'})
```

The output directory must exist; choose a new report filename. [inspect_resolve.lua](../scripts/inspect_resolve.lua) reads project identity, media pool, timeline inventory, active tracks/items, and render format/codec options. It fails on a project-name mismatch, records getter errors and scan truncation, and performs no project saves, edits, imports, exports, renders, or timeline creation. It writes only the requested JSON snapshot. Project fps is not timeline fps when no timeline exists. Ingest snapshots are provisional.

An agent with native computer-use access can execute the console command. Otherwise provide that exact one-line action to the user. Read the console result and JSON; pasting a command is not success. Do not paste Python into Lua or depend on a separate Python runtime for Free.

## Capability distinctions

| Operation | Resolve 19 route | Verification |
| --- | --- | --- |
| Project, timeline, media, tracks | Internal Lua getters; Studio external API where connected | Actual returned data, errors and completeness |
| Save/export/duplicate | SDK documents SaveProject, ExportProject, DuplicateTimeline and Timeline.Export | Within authorized scope, inspect returned identity and actual backup; DRP/DRT does not back up source media |
| Clip assembly/properties | Documented MediaPool/Timeline APIs or native UI | Test needed operation on a recoverable version; read actual ranges afterward |
| Fairlight effects/parameters | Native UI | Read controls and audition/render; no invented general plugin API |
| Audio transitions | Native UI and Transition Inspector | Every intended seam, type, frame duration, handles; no assumed transition API |
| Word timings | Separate local ASR/alignment or authorized provider | Actual per-word output mapped to source, not implied by Codex OAuth |
| Waveform/loudness/metadata | Fairlight and local FFmpeg/FFprobe | Execute and inspect output |
| Preview/export | Discover codecs, then Deliver or supported API | Actual render, metadata, moving-picture checks and listening |
| Studio-only effects | Only where verified licensed | Never assume Voice Isolation or AI dialogue tools in Free |

SDK method presence means documented, not tested. Report `documented/not tested`, `UI required`, `unavailable`, and `live verified` accurately. Empty/nil/false results, missing media and partial scans must remain visible. A successful render is not a watch-through or listening pass.

## Frame and media handling

Preserve fractional fps, source time bases, audio sample offsets and drop-frame conventions. Source frames, absolute timeline frames and marker offsets are distinct units. Validate endpoint conventions for each editing API before cutting; do not mix inclusive and exclusive ends. Inspect retimes and variable-frame-rate sources before deriving constant-fps mappings.

Never modify Resolve's database directly. Interchange is a fallback for a new identified timeline and can omit grades, Fusion, transitions, audio automation or sync. Preserve the original and document/verify what round-trips; do not reconstruct a working timeline through lossy interchange merely to avoid a UI step.

Primary sources: [Alex's installation notes](https://github.com/Forward-Future/alexs-davinci-editing-skills#installation), the installed Blackmagic SDK, and [Blackmagic staff on external scripting](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=204977).


Observed19.1 getter detail: track-enable getters returned false for inactive timelines. During authorized timeline comparisons, set the inspected timeline current before comparing enable state. The read-only audit only reads active timeline tracks.
