# Waveform and word-timing audit

Check waveforms **against a word-timed transcript**, so cuts preserve complete words and thoughts while keeping the edit tight. This is a joint signal-and-language check, not two independent spot checks. Use it before a first dialogue cut and after assembling the joins. On an existing edit, reuse verified evidence and recheck joins affected by changed source ranges, timing, processing, or fades. A visual-only pass does not authorize recutting unrelated dialogue.

This reference applies to spoken edits. Performance camera switching uses continuous music and musical cues; do not infer missing words or unwanted silence from singing or instrumental passages.

## Establish a common clock

- Obtain per-word start/end times for the actual chosen delivery, using word-level transcription or alignment. Sentence captions alone are insufficient. Retain the source words and take context, including abandoned starts that recognition may omit. Treat timestamps as estimates and record doubtful or contradictory alignment.
- Map word times to the correct source audio samples and timeline frames. Preserve fractional frame rates, clip in-points, source offsets, retimes, OBS restart sections, and any latency compensation in processed audio. Never apply original source timestamps directly to a ripple-edited timeline. Do not assume an audio file's imported frame units equal the timeline rate.
- Inspect the original and processed dialogue waveforms in the same time windows. If processing changes alignment, correct or account for it before placing cuts. Do not mistake a gate suppressing a quiet consonant for a genuine gap in the original speech.

## Inspect every proposed join before trimming

Read and hear the surrounding phrase while viewing the waveform with word spans on the same time axis. Expand the context when a take restart or sentence meaning is unclear. Use a spectrogram to resolve quiet consonants, fricatives, and decaying syllables when waveform amplitude is ambiguous.

For each join, check these separately:

1. **Outgoing completeness:** find the last intended word and its actual final phoneme in the signal. Keep its quiet tail or stop release, even when the transcript's end time is earlier. Ensure the eventual fade does not truncate or audibly suppress it. Do not extend into the next discarded word.
2. **Incoming completeness and immediacy:** locate the first intended word's actual onset, including quiet initial consonants. Scan forward from the proposed clip head through any idle noise, preparatory breath, or leftover false start. Start at the nearest safe preceding video frame; do not add several blank frames as generic safety padding. A loud vowel or recognizer emission can occur after the word has already begun.
3. **Thought and pause:** assess the outgoing and incoming phrases together. Preserve enough space for intelligibility, emphasis, and a completed thought; remove retake dead time and unnecessary hesitation. Do not merge unrelated fragments or erase a meaningful pause because its waveform is quiet. Do not stretch every pause to a fixed duration. For tight dialogue edits, keep any deliberate rhetorical space with the outgoing thought or continuous shot where appropriate, while avoiding an idle lead-in after the next shot begins. Preserve the required aligned cuts across synced layers.

The transcript explains which sounds and thoughts belong; the waveform shows where those sounds actually occur. Neither alone proves the cut is safe. Agreement between multiple recognizers, a universal dB threshold, or a fixed millisecond padding rule is not sufficient.

## Verify the assembled, processed result

Apply the same editorial boundaries to all synced layers, preserving source offsets. Check each assembled join again after the chosen processing and dialogue fade are applied. Compare the intended words with the retained source coverage and the resulting signal; audition at normal speed for clipped syllables, clicks, a rushed thought, a repeated fragment, or dead air. A crossfade can smooth a click but cannot restore missing speech.

Record every outgoing and incoming edge, including heads that already start in silence. A practical project-local CSV or JSON record contains:

- join ID and current timeline frame/timecode;
- outgoing/incoming source IDs, source ranges, and word text with word times;
- observed phoneme end/onset, chosen cut frames, and retained pause;
- processed-waveform/fade check, normal-speed audition status, and any ambiguity;
- repair and before/after positions when an edit changes timing.

Compare the expected join list with the recorded checks before handing off the first cut. Recheck affected neighbors after repairs or ripple edits, and confirm there are no unintended gaps or sync shifts. Do not mark a join passed merely because a detector found nothing to change.

If word-level alignment or direct listening is unavailable, complete the supported inspection, identify the exact missing verification, and provide targeted audition material when useful. Do not silently substitute sentence timestamps, claim a full listening pass, or guarantee that no clipped words remain based only on automated analysis.
