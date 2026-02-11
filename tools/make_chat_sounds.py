#!/usr/bin/env python3
"""
Generate ExNulla notification sounds (including a "voice-ish" chat alert) as WAV.
No external dependencies. Produces mono 44.1kHz 16-bit PCM WAV files.

Usage:
  python tools/make_chat_sounds.py
Outputs:
  assets/audio/*.wav
"""

from __future__ import annotations
import math
import os
import random
import wave
from pathlib import Path
from typing import List


SR = 44100


def _write_wav(path: Path, samples: List[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = bytearray()
    for x in samples:
        x = max(-1.0, min(1.0, x))
        v = int(x * 32767)
        pcm += v.to_bytes(2, byteorder="little", signed=True)

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm)


def _env(n: int, fade_in_s: float, fade_out_s: float) -> List[float]:
    fi = max(1, int(SR * fade_in_s))
    fo = max(1, int(SR * fade_out_s))
    e = [1.0] * n
    for i in range(min(fi, n)):
        e[i] *= i / fi
    for i in range(min(fo, n)):
        idx = n - 1 - i
        e[idx] *= i / fo
    return e


def _sine(freq_hz: float, dur_s: float, vol: float) -> List[float]:
    n = int(SR * dur_s)
    e = _env(n, 0.01, 0.02)
    out = []
    for i in range(n):
        t = i / SR
        out.append(math.sin(2 * math.pi * freq_hz * t) * vol * e[i])
    return out


def _silence(dur_s: float) -> List[float]:
    return [0.0] * int(SR * dur_s)


def _voiceish_chat(dur_s: float = 0.24, vol: float = 0.30) -> List[float]:
    """
    "Voice-ish" 'chaaat' vibe without TTS:
    - tiny noise burst for the 'ch'
    - harmonic + formant-like partials for the vowel
    """
    # consonant burst
    burst_n = int(SR * 0.035)
    burst = [(random.uniform(-1, 1) * 0.10) for _ in range(burst_n)]
    burst_env = _env(burst_n, 0.002, 0.02)
    burst = [burst[i] * burst_env[i] for i in range(burst_n)]

    # vowel body
    n = int(SR * dur_s)
    e = _env(n, 0.02, 0.06)

    f0 = 205.0  # "fundamental"
    # formant-ish partials (tuned to sound like an "aa" shape)
    f1 = 750.0
    f2 = 1350.0

    out = []
    for i in range(n):
        t = i / SR
        s = (
            0.70 * math.sin(2 * math.pi * f0 * t)
            + 0.35 * math.sin(2 * math.pi * f1 * t)
            + 0.22 * math.sin(2 * math.pi * f2 * t)
        )
        out.append(s * vol * e[i])

    return burst + out


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "assets" / "audio"

    # baseline ping
    ping = _sine(880, 0.12, 0.35) + _silence(0.03) + _sine(1320, 0.10, 0.35)
    _write_wav(out_dir / "exnulla-double-tone.wav", ping)

    # email-low
    email_low = _sine(660, 0.14, 0.35) + _silence(0.03) + _sine(990, 0.10, 0.35)
    _write_wav(out_dir / "exnulla-email-low.wav", email_low)

    # soft bg
    soft = _sine(880, 0.12, 0.20) + _silence(0.04) + _sine(1320, 0.10, 0.20)
    _write_wav(out_dir / "exnulla-soft-bg.wav", soft)

    # sharp focus
    sharp = _sine(1320, 0.10, 0.40) + _silence(0.02) + _sine(1760, 0.08, 0.40)
    _write_wav(out_dir / "exnulla-sharp-focus.wav", sharp)

    # single tone
    single = _sine(1000, 0.18, 0.35)
    _write_wav(out_dir / "exnulla-single-tone.wav", single)

    # voice-ish
    voice = _voiceish_chat()
    _write_wav(out_dir / "exnulla-voiceish-chat.wav", voice)

    print(f"Wrote WAVs to: {out_dir}")


if __name__ == "__main__":
    random.seed(7)
    main()

