# 2026-02-10 — Day 4
## Restream Removal → Multi-RTMP → Streamer.bot Stabilization

---

## Executive Summary

Day 4 was not our cleanest execution, but we moved from a brittle multi-service setup
(Restream + OBS docks + mixed chat routing) to a more deterministic stack:

OBS → Multi-RTMP plugin → Native platform outputs  
Streamer.bot → Combined Chat + Chat Sounds  
PowerToys → Window control  

We also generated a full intro bumper **purely from code**.

---

# 1. Why We Removed Restream

### Problems Observed

- Extra failure surface (additional hop in stream path)
- OBS Restream chat dock became fuzzy / unreadable
- Resizing caused rendering artifacts
- Added configuration complexity
- Harder to debug signal path

### Decision

Remove Restream from the pipeline and stream directly from OBS using multiple RTMP outputs.

---

# 2. Multi-RTMP Plugin

Plugin:
https://github.com/sorayuki/obs-multi-rtmp

### Install

1. Download Windows installer matching OBS version.
2. Install.
3. Restart OBS.
4. Tools → Multiple Output

### Result

Single OBS instance pushing:
- Twitch
- Kick
- (Future platforms optional)

No middle relay.

---

# 3. Combined Chat Strategy (Streamer.bot)

Key realization:
Streamer.bot already includes a combined chat window.

### What Worked

- Connect Twitch + Kick in Streamer.bot.
- Use Streamer.bot Chat window as operator view.
- No dependency on OBS dock for monitoring.

### Optional On-Stream Chat Strategy

Maintain a global buffer variable:

- Append new chat line
- Trim to last N lines
- Push entire buffer into OBS text source

Overwrite expected.

---

# 4. Chat Sounds (Headphone Notification)

Goal:
Immediate audible cue for new chat message.

### Implementation

Trigger:
- Twitch → Chat Message
- Kick → Chat Message

Action:
- Sounds → Play Sound
- Output device: Default system device

### Important

Headphones must be default Windows output device.
Avoid OBS monitoring until stable.

---

# 5. Always-On-Top Chat Window

Streamer.bot does not reliably enforce always-on-top.

Solution:
Microsoft PowerToys

- Install PowerToys
- Use "Always On Top" hotkey to pin chat window

This ensures chat stays visible during gameplay or coding.

---

# 6. Intro Video From Code

We generated a 7 second, 1080x1080 intro bumper using:

- Python (Pillow) for frame generation
- ffmpeg for encoding

This is deterministic and reproducible.

See:
tools/video/render_intro.py

Encoding:

ffmpeg -y -framerate 30 -i frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  exnulla_intro.mp4

---

# 7. Artifacts Added to Repo

- overlays/5min-countdown.html
- overlays/15min-countdown.html
- tools/video/render_intro.py
- assets/audio/sfx/*
- docs/ops/2026-02-10_day-4_restreeam_to_multirtmp_streamerbot.md

---

# Status

Stream path stabilized.
Chat consolidated.
Notifications functional.
Intro asset reproducible.

Not pretty.
But forward progress.

