# Sources and adaptation history

## Original skills

- Creator: **Alex (@The_Alex)**.
- Publisher: **Forward Future**.
- Original article / demos: https://forwardfuture.com/alexs-davinci-editing-skills
- Original GitHub: https://github.com/Forward-Future/alexs-davinci-editing-skills
- Installation: https://github.com/Forward-Future/alexs-davinci-editing-skills#installation
- Adapted snapshot: commit `fc9b3b180a6999cf746ada36be8dc42a2f366f27`.
- License: MIT. Original copyright and permission notice are retained in the root LICENSE and each skill's LICENSE.

The source URLs were checked September 14, 2026. The article points to the same GitHub skills; it is credited and linked, not copied or relicensed. Source media, demos, trademarks and third-party products retain their respective rights.

## This adaptation

Prepared for dax8it using Codex during a live-band and venue-promo editing project. Added or revised:

- Resolve 19.1.4 Free/macOS capability limits and internal Lua access.
- Read-only audit, project identity guards and a reusable Scripts-menu installer.
- Performance/music continuity, same-take camera detail cuts, mixed-frame-rate handling and vertical delivery.
- Natural ElevenLabs narration through REST, profile-specific credential selection, independent voice/music stems and controlled ducking.
- Cooler/richer grade starting points, reference comparison and local color versions.
- Backup, duplicate, partial-failure recovery, source-identity correction and actual-export verification practices.

Removed assumptions that dialogue treatment applies to songs, that all outputs should be square/4K, or that universal fades/keyboard remaps/external scripting apply to every setup. No upstream certification of Resolve19 compatibility is implied.

## Technical references

- Blackmagic's locally installed SDK: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt`. Consult the version installed with your build.
- Blackmagic forum discussion of external scripting: https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=204977
- ElevenLabs Text-to-Speech API: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- ElevenLabs authentication: https://elevenlabs.io/docs/api-reference/authentication

The ElevenLabs helper is independent client code, not the official MCP server. Its documented API request uses a voice ID, model ID and voice settings. Live production used `eleven_multilingual_v2`; verify availability for your account before using it.

## Download-card screenshot

`docs/images/resolve-19.1.4-free-download.png` was supplied by the user on September 14, 2026, showing the DaVinci Resolve 19.1.4 Free download card dated March 21, 2025 on the [official Blackmagic Support Center](https://www.blackmagicdesign.com/support/). Included as a visual identification aid at the user's request. Blackmagic Design retains rights to its website content and trademarks; the repository's MIT license does not relicense this screenshot.
