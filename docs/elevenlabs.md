# ElevenLabs setup and voiceovers

Read the complete [voiceover workflow](../skills/edit-davinci-video/references/elevenlabs-voiceovers.md), also shipped inside the installed visual-editing skill.

It covers private credential selection (including Hermes profiles), the portable REST helper, voice/model inspection, generation without automatic paid retries, natural phrasing, separate background and narration stems, ducking, audio-only corrections and delivery checks. It applies to explainers, tutorials, product videos, events and other narrated edits; the live-band mix is a worked example. An ElevenLabs MCP is optional; the tested production workflow used REST directly.

Quick verification from this repository:

```sh
export DAVINCI_ELEVENLABS_ENV_FILE="$HOME/.config/private/elevenlabs.env"
python3 scripts/elevenlabs_client.py inspect --output reports/voices.json
```

Then choose a returned voice ID, write a short script to a text file and follow the generation example in the workflow. Listen to a short result before generating a whole batch. No real key or generated voice files are included here.
