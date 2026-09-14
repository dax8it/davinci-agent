# DaVinci Resolve 19.1 editing skills

Reusable Codex skills for live band performances, venue showcases and narrated promos, adapted from **Alex's DaVinci Editing Skills**. Tested on **DaVinci Resolve 19.1.4.11 Free for macOS** during real timeline assembly and delivery. Other builds and fresh installations still require a capability audit.

These are agent instructions plus small helper scripts. They do not install an MCP server, unlock Studio features, or connect a model to Resolve by themselves.

## Start here

1. [Download and install DaVinci Resolve **19.1.4 Free for Mac**](docs/download-resolve-19.1.4.md), using the illustrated guide to find the **21 Mar 2025** entry on Blackmagic Support. Then clone or download this repository to your Mac.
2. From its root, run `python3 scripts/install_skills.py` to install all four sibling skill folders into `$CODEX_HOME/skills` (default `~/.codex/skills`). Identical installs are skipped; differing installs are refused so they can be reviewed and backed up.
3. Open your project in Resolve and install the read-only menu entry:
   ```sh
   python3 scripts/install_menu_audit.py --project 'Your Project Name'
   ```
4. In Resolve, choose **Workspace → Scripts → Codex - Resolve 19 read-only audit**. If the entry is missing, reopen the menu or restart Resolve after saving your work.
5. Ask Codex to read the newly generated JSON/log in `reports/`, confirm the actual project/timeline/fps and available operations, then perform your requested edit on a recoverable copy.

Keep this checkout at the same path after installing the menu entry. The entry uses its absolute path. See [Resolve 19.1 setup](docs/resolve-19.1-quickstart.md) for details and the Console fallback.

## Included skills

| Skill | Use |
| --- | --- |
| `edit-davinci-video` | Main performance/venue workflow: selects, pacing, camera coverage, framing, color, narration and delivery |
| `clean-davinci-dialogue` | Spoken intros, interviews and banter; not blanket processing of music |
| `first-cut-davinci-dialogue` | Spoken edits checked against words and waveforms |
| `smooth-davinci-audio-cuts` | Appropriate audio joins while preserving sync |

## Guides

- [Download the right Resolve version (with screenshot)](docs/download-resolve-19.1.4.md)
- [Resolve 19.1 quick start and capability limits](docs/resolve-19.1-quickstart.md)
- [ElevenLabs voiceovers](docs/elevenlabs.md): credentials, voice selection, generation, natural phrasing and music ducking
- [Performance editing recipes](skills/edit-davinci-video/references/performance-recipes.md): source review, fast cuts, cooler grades, versioned corrections
- [Example prompts](examples/prompts.md)
- [What was actually verified](docs/verification.md)
- [Original sources, license and changes](ATTRIBUTION.md)

The package contains no footage, generated voices, API keys, Resolve projects or machine-specific production scripts. Create a project brief with your own source/export/backup paths. Never blindly rerun an assembly script after a partial failure.

## Requirements and checks

Core skill installation and the ElevenLabs client use Python 3.9+ standard library. Resolve runs the audit internally in Lua. FFmpeg/FFprobe are useful for media inspection/mixing/export checks; NumPy is useful for offline stem mixing. ElevenLabs requires a working account/key and available voice/model; generation consumes its credits. An MCP integration is optional and was not used in the tested workflow.

For repository checks only:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
```

Tests use mocked Resolve/ElevenLabs objects; they do not edit an open project or generate paid speech. End-to-end verification on your installation is still necessary.

## Credits

Original workflows by **Alex (@The_Alex)**, distributed by **Forward Future**. See the [original article and demos](https://forwardfuture.com/alexs-davinci-editing-skills) and [original GitHub repository](https://github.com/Forward-Future/alexs-davinci-editing-skills). Original MIT notices are retained. This independent adaptation is not endorsed by Blackmagic Design, OpenAI or ElevenLabs.
