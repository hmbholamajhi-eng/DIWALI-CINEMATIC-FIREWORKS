"""
Procedural soundtrack - no audio files needed.
Temple-bell tones for every diya, a drone pad, rocket whooshes, deep booms,
crackles and a golden finale. Built from the same timeline as the visuals.
"""
import math
import numpy as np
from config import *

SR = SAMPLE_RATE
TAU = 2 * math.pi
rng = np.random.default_rng(7)

PENTA = [261.63 * 2 ** (s / 12) for s in (0, 2, 4, 7, 9, 12, 14, 16, 19, 21)]


def _t(n):
    return np.arange(n) / SR


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode='same')


def bell(freq, dur=3.2, vol=0.3):
    n = int(SR * dur)
    t = _t(n)
    sig = np.zeros(n)
    for r, a, d in [(1, 1, 2.4), (2.01, .45, 1.6), (2.76, .3, 1.1),
                    (4.07, .18, .7), (5.4, .1, .5), (8.9, .05, .3)]:
        sig += a * np.sin(TAU * freq * r * t) * np.exp(-t / d)
    return sig * np.minimum(1, t / 0.004) * vol


def whoosh(dur, vol=0.25):
    n = int(SR * dur)
    nz = rng.standard_normal(n)
    a, b = lowpass(nz, 90), lowpass(nz, 7)
    u = np.linspace(0, 1, n)
    sig = a * (1 - u) * 6 + b * u * 1.2
    env = (u ** 1.6) * (1 - u ** 8)
    return sig * env * vol


def boom(dur=2.4, vol=0.9):
    n = int(SR * dur)
    t = _t(n)
    f = 36 + 80 * np.exp(-t * 16)
    ph = TAU * np.cumsum(f) / SR
    low = np.sin(ph) * np.exp(-t / 0.55)
    body = lowpass(rng.standard_normal(n), 28) * 7 * np.exp(-t / 0.28)
    crack = rng.standard_normal(n) * np.exp(-t / 0.035) * 0.55
    tail = lowpass(rng.standard_normal(n), 220) * 10 * np.exp(-t / 0.9) * 0.4
    return (low * 1.0 + body * 0.5 + crack + tail) * vol


def crackle(dur=1.6, vol=0.25, density=0.0025):
    n = int(SR * dur)
    t = _t(n)
    dens = density * np.exp(-t / 0.7)
    imp = (rng.random(n) < dens) * rng.standard_normal(n)
    k = np.exp(-np.arange(int(0.004 * SR)) / (0.0009 * SR))
    sig = np.convolve(imp, k, mode='same')
    sig = np.diff(sig, prepend=0)
    return sig * vol * 6


def sprinkle(dur, vol=0.05):
    n = int(SR * dur)
    u = np.linspace(0, 1, n)
    sig = np.diff(rng.standard_normal(n), prepend=0)
    sig = lowpass(sig, 3)
    return sig * np.sin(np.pi * u) ** 1.5 * vol


def chord_pad(freqs, dur=7.0, vol=0.12, attack=1.4):
    n = int(SR * dur)
    t = _t(n)
    sig = np.zeros(n)
    for f in freqs:
        sig += np.sin(TAU * f * t) + 0.5 * np.sin(TAU * f * 1.004 * t) + 0.25 * np.sin(TAU * f * 2 * t)
    env = np.minimum(1, t / attack) * np.exp(-t / (dur * 0.45))
    return sig * env * vol / max(1, len(freqs))


def drone(n):
    t = _t(n)
    sig = np.zeros(n)
    vib = 0.35 * np.sin(TAU * 0.11 * t)
    for f, a in [(65.41, 1), (98.0, .7), (130.81, .5), (196.0, .32), (261.63, .14)]:
        sig += a * np.sin(TAU * f * t + vib) + a * .6 * np.sin(TAU * f * 1.003 * t)
    rise = np.minimum(1, t / 5.0)
    swell = 1 + 0.9 * np.exp(-((t - T_TEXT - 1.5) / 3.0) ** 2)
    fade = np.clip((DURATION - t) / 2.5, 0, 1)
    return sig * rise * swell * fade * 0.045


def _mix(buf, sig, start, pan=0.0, gain=1.0):
    i0 = int(start * SR)
    if i0 >= len(buf) or i0 < 0:
        return
    i1 = min(len(buf), i0 + len(sig))
    s = sig[:i1 - i0] * gain
    ang = (pan + 1) * math.pi / 4
    buf[i0:i1, 0] += s * math.cos(ang)
    buf[i0:i1, 1] += s * math.sin(ang)


def build():
    N = int(DURATION * SR)
    buf = np.zeros((N, 2), dtype=np.float64)
    r = np.random.default_rng(3)

    d = drone(N)
    buf[:, 0] += d
    buf[:, 1] += d

    # ---- diyas: soft bell per flame, melody walks up the pentatonic scale
    idx = 1
    for i, ((x, y, s), t) in enumerate(zip(DIYAS, DIYA_T)):
        idx = int(np.clip(idx + r.choice([-1, 1, 1, 2]), 0, len(PENTA) - 1))
        f = PENTA[0] / 2 if i == 0 else PENTA[idx]
        v = 0.55 if i == 0 else 0.22
        _mix(buf, bell(f, 3.6 if i == 0 else 2.6, v), t, (x - W / 2) / (W / 2) * 0.7)
        if i == 0:
            _mix(buf, bell(PENTA[4], 3.6, 0.2), t + 0.02, 0)

    # ---- rangoli: shimmering sprinkle + gentle phrase
    _mix(buf, sprinkle(T_RANG1 - T_RANG0 + 1, 0.07), T_RANG0 - 0.5, 0)
    phrase = [0, 2, 4, 2, 5, 4, 2, 0, 4, 5, 7, 5, 4, 2, 4, 2]
    t = T_RANG0
    for k in range(int((T_RANG1 - T_RANG0) / 1.2)):
        _mix(buf, bell(PENTA[phrase[k % len(phrase)]] / 2, 3.0, 0.2), t + k * 1.2, (-1) ** k * 0.4)

    # ---- fireworks
    for f in FIREWORKS:
        tb = f['t']
        pan = (f['x'] - W / 2) / (W / 2) * 0.8
        _mix(buf, whoosh(ROCKET_T, 0.22), tb - ROCKET_T, pan)
        size = f['size']
        _mix(buf, boom(2.4, 0.55 * min(1.4, size)), tb, pan)
        if f['kind'] in ('peony', 'willow') and f['crackle']:
            _mix(buf, crackle(1.8, 0.2), tb + 1.0, pan)
        if f['kind'] == 'willow':
            _mix(buf, crackle(2.2, 0.12, 0.0015), tb + 0.4, pan)
        if f['kind'] == 'heart':
            for j, fr in enumerate([PENTA[2], PENTA[4], PENTA[5], PENTA[7], PENTA[9]]):
                _mix(buf, bell(fr, 3.0, 0.3), tb + 0.15 + j * 0.16, 0)
            _mix(buf, chord_pad([PENTA[0], PENTA[2], PENTA[3]], 5.0, 0.12, 0.6), tb, 0)
        if f['kind'] == 'grand':
            _mix(buf, boom(3.2, 1.0), tb, 0)
            _mix(buf, crackle(3.0, 0.3, 0.004), tb + 0.3, 0)

    # ---- finale: golden chord and rising bell arpeggio as the title forms
    _mix(buf, chord_pad([PENTA[0], PENTA[2], PENTA[3], PENTA[5], PENTA[7]], 12.0, 0.5, 1.8), T_TEXT + 0.3, 0)
    for j, fr in enumerate([PENTA[5], PENTA[7], PENTA[8], PENTA[9], PENTA[7], PENTA[9]]):
        _mix(buf, bell(fr, 4.0, 0.26), T_TEXT + 1.6 + j * 0.28, ((-1) ** j) * 0.35)
    _mix(buf, bell(PENTA[9] * 2, 5.0, 0.2), T_TEXT + 3.4, 0)

    # ---- master: gentle soft-clip, fade in/out
    t = _t(N)
    master = np.clip(t / 1.2, 0, 1) * np.clip((DURATION - t) / 1.5, 0, 1)
    buf *= master[:, None]
    buf = np.tanh(buf * 1.1) * 0.92
    return (buf * 32767).astype(np.int16)
