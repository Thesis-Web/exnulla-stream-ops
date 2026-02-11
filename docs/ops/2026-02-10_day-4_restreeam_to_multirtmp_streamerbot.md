# 2026-02-10 — Day 4: Restream Removal → Multi-RTMP → Streamer.bot Stabilization

## Executive summary

Day 4 was not our cleanest execution, but we moved from a brittle multi-service setup
(Restream + OBS docks + mixed chat routing) to a more deterministic stack:

- OBS → Multi-RTMP plugin → native platform outputs
- Streamer.bot → combined chat + chat sounds
- PowerToys → always-on-top operator view

We also generated a full intro bumper **from code** (Python frames → ffmpeg MP4).

## Progress log

- Removed Restream from the streaming path.
- Switched to Multi-RTMP from inside OBS.
- Consolidated chat monitoring inside Streamer.bot.
- Added a headset chime on every new chat message.
- Pinned chat window using PowerToys Always On Top.
- Generated intro video deterministically (code-only pipeline).

## 1. Why we removed Restream

### Problems observed

- Added an extra hop in the stream path.
- OBS Restream dock was fuzzy/unreadable.
- Resizing caused rendering artifacts.
- Debugging signal path was harder than direct RTMP outputs.

### Decision

Remove Restream and stream directly from OBS using multiple RTMP outputs.

## 2. Multi-RTMP plugin

Plugin releases:

- [sorayuki/obs-multi-rtmp](https://github.com/sorayuki/obs-multi-rtmp)

### Install

1. Download the Windows installer matching your OBS version.
2. Install and restart OBS.
3. Open `Tools → Multiple Output`.

### Result

Single OBS instance pushing to multiple platforms without a relay.

## 3. Combined chat strategy (Streamer.bot)

Key realization: Streamer.bot already includes a combined chat window.

### What worked

- Connect Twitch + Kick in Streamer.bot.
- Use the built-in chat window as operator view.
- Remove dependency on OBS Restream dock.

## 4. Chat sounds (headphone notification)

Goal: Audible cue in headset for every new chat message.

### Implementation

Trigger on:

- Twitch → Chat Message
- Kick → Chat Message

Then run:

- Sounds → Play Sound
- Output device: default system device

Ensure headphones are set as Windows default output.

## 5. Always-on-top chat window

Solution: Microsoft PowerToys.

- Install PowerToys.
- Use Always On Top hotkey to pin Streamer.bot chat window.

Releases:

- [microsoft/PowerToys](https://github.com/microsoft/PowerToys/releases)

## 6. Intro video from code

We generated a 7-second, 1080×1080 intro bumper using:

- Python (Pillow) for frame generation
- ffmpeg for encoding

See:

`tools/video/render_intro.py`

Encode:

```bash
ffmpeg -y -framerate 30 -i frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  exnulla_intro.mp4
```

Preview:

```bash
mpv exnulla_intro.mp4
```

## 7. Artifacts added to repo

- docs/ops/2026-02-10_day-4_restreeam_to_multirtmp_streamerbot.md
- tools/video/render_intro.py
- overlays/5min-countdown.html
- overlays/15min-countdown.html
- assets/audio/sfx/*

## Status

- Stream path stabilized
- Chat consolidated
- Notifications functional
- Intro asset reproducible
