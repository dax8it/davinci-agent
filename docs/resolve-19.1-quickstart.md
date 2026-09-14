# Resolve 19.1 on macOS

## What connects to what

Codex reads the four SKILL.md folders. A local UI tool or a person invokes a script inside Resolve. Resolve's internal Lua API inspects or edits the project. ElevenLabs separately generates narration files, which are imported into Resolve. Model choice does not change Resolve licensing or API access.

The tested build is **19.1.4.11 Free**, not a guarantee for every 19.1 release. External scripting is a Studio capability; adding RESOLVE_SCRIPT_API or PYTHONPATH to `.zshrc` does not enable it in Free. The desktop app may not inherit shell startup variables anyway. No shell-profile edit or external listener is required for this workflow.

## Install and inspect

Run from the repository root:

```sh
python3 scripts/install_skills.py
python3 scripts/install_menu_audit.py --project 'Your Project Name'
```

The skill installer uses `$CODEX_HOME/skills`, normally `~/.codex/skills`. Keep the four names and sibling structure. Ask the agent to list them after refreshing its skill discovery or starting a new turn/session. If a same-named skill differs, the installer refuses replacement: compare it, preserve the existing folder in a backup location, then install the reviewed version.

The menu installer creates:

`~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/Codex - Resolve 19 read-only audit.lua`

It points to this checkout and the project name you supplied. It only reads Resolve state and writes local JSON/log/render-status files. By default they go into this repository's ignored `reports/` directory. Override with `--reports '/absolute/path/to/reports'`. Use `--dest` only when installing to a different script directory intentionally.

Open the intended project, then **Workspace → Scripts → Codex - Resolve 19 read-only audit**. Check the newest log for `success=true`; inspect the JSON for project/timeline identity, fps, media paths, errors and truncated scans. Do not infer success from a click or an installed SDK. A project with no active timeline is valid; the audit does not invent or create one.

If the menu is unavailable, open **Workspace → Console**, select **Lua**, create the output directory and run this with your real absolute paths:

```lua
dofile('/absolute/path/davinci-agent/skills/edit-davinci-video/scripts/inspect_resolve.lua')({expected_project='Your Project Name',output_path='/absolute/path/reports/new-audit.json'})
```

Console activation was intermittent through our UI bridge. The Scripts menu reliably executed commands in the tested sessions. Do not blindly paste into a window whose identity cannot be verified. Native UI indices change; obtain a fresh snapshot before each menu action. Read the new execution receipt afterward.

## Start an authorized edit

1. Create a brief naming project, sources, reference, output folder, backup folder, aspect ratio, fps, desired length and audio/voice requirements.
2. Inspect sources: frame rates, orientation metadata, durations, source availability and Finder tags if the user used them to rate clips. Store source selections by file and exact time range. Color tags guide selection; they do not identify songs or people.
3. Save the project and export a recoverable DRP/DRT before structural edits. Work on a clearly named new timeline or duplicate. A backup references media; it does not contain all source files.
4. Use the installed SDK and audited capabilities to prepare a bounded Lua operation. Guard project identity, target timeline ID/name, source paths and export filename. Keep read-only launchers read-only; give an editing operation its own explicit launcher.
5. Execute through the Scripts menu. Check logs and resulting ranges/tracks/grades before rendering. After a partial failure, inspect what already exists and recover by exact identity. Do not blindly rerun or overwrite a completed output.
6. Render to a new versioned filename. Verify the file, not only the job status. Report its exact absolute directory to the user. Retire completed one-time editing launchers.

## Tested API details and limits

- Native internal Lua successfully saved/exported projects, built/duplicated timelines, imported sources, appended clips, set track routing/framing/local CDL versions, added a Fusion closing fade and rendered H.264/AAC.
- For `AppendToTimeline` on this build, a 3600-frame range used `startFrame=0, endFrame=3600`. Verify returned duration/start every time; do not generalize this observed exclusive-end behavior to other APIs/builds.
- `GetIsTrackEnabled` returned misleading false values for inactive timelines. During an authorized comparison, set each timeline current before reading enable state. The read-only audit only inspects track details for the current timeline and does not switch it.
- Use local color versions: `AddVersion(name,0)`, `LoadVersionByName(name,0)`, check `GetCurrentVersion`, then `SetCDL`. Remote grades could affect other uses of a clip.
- Mixed 24/30/60fps sources retain real-time playback. Distinguish 23.976 from24 and29.97 from30. Some media required a CFR proxy; preserve source-time mapping and verify audio sync rather than reinterpreting fps.
- UIManager is restricted in this19.1 build; avoid depending on it in Free. Fairlight controls beyond the SDK may require UI/manual operation. Do not promise Studio-only voice isolation or AI tools.
- Never edit the Resolve database, application binaries or license behavior. No persistent background polling script is needed.

See [verification scope](verification.md) and the skill's [Resolve profile](../skills/edit-davinci-video/references/resolve19-macos.md).
