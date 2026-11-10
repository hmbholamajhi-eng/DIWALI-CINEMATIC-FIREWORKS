"""
Diwali Cinematic - shared configuration & the master timeline.
Everything (visuals + audio) is driven by this one script, so the film is
frame-perfect and always plays exactly the same way.
"""
import math
import random

# ---------------------------------------------------------------- canvas
W, H = 720, 1280              # internal render size (9:16 reel format)
HZ = 640                      # horizon line (sky above, courtyard floor below)
DURATION = 60.0               # seconds
FPS = 30                      # export fps
SAMPLE_RATE = 44100

BRAND = "HM BHOLA"

# ---------------------------------------------------------------- courtyard
RC = (W // 2, 930)            # rangoli centre
RANGOLI_R = 290               # rangoli half-width in pixels
SQ = 0.46                     # perspective squash of the floor
RING_RX = 338                 # diya ring half-width

# ---------------------------------------------------------------- timeline (seconds)
T_FIRST_DIYA = 2.8
T_RANG0, T_RANG1 = 12.0, 28.5
T_TEXT = 41.0                 # grand finale burst -> "HAPPY DIWALI" forms
ROCKET_T = 1.25               # rocket flight time

# ---------------------------------------------------------------- palette
GOLD = (255, 200, 61)
SAFFRON = (255, 138, 31)
RED = (230, 57, 70)
PINK = (255, 20, 147)
CYAN = (0, 212, 255)
BLUE = (0, 82, 255)
CREAM = (255, 243, 176)
WHITE = (255, 255, 255)
PURPLE = (150, 70, 255)
GREEN = (60, 220, 140)


def diya_layout():
    """Diyas in the order they are lit: (x, y, scale)."""
    cx, cy = RC
    rx = RING_RX
    ry = rx * SQ * 1.05
    L = [(360, 1190, 1.45),            # the very first diya
         (215, 1202, 1.45), (505, 1202, 1.45),
         (80, 1220, 1.5), (640, 1220, 1.5)]
    ring = []
    n = 22
    for i in range(n):
        a = math.pi / 2 + 2 * math.pi * i / n
        x = cx + rx * math.cos(a)
        y = cy + ry * math.sin(a)
        sc = 0.8 + 0.5 * (y - (cy - ry)) / (2 * ry)
        d = abs(((a - math.pi / 2 + math.pi) % (2 * math.pi)) - math.pi)
        ring.append((d, x, y, sc))
    ring.sort()
    for d, x, y, sc in ring:
        L.append((x, y, sc))
    back = [(40 + 80 * i, 708, 0.62) for i in range(9)]
    back.sort(key=lambda p: abs(p[0] - 360))
    return L + back


def diya_times(n):
    """Slow, breathing start -> gradually quickening cascade."""
    T = [T_FIRST_DIYA]
    for i in range(1, n):
        u = (i - 1) / max(1, n - 2)
        T.append(4.6 + 12.4 * (0.5 * u + 0.5 * (1 - (1 - u) ** 1.5)))
    return T


def make_fireworks():
    rnd = random.Random(11)
    F = []

    def add(t, x, y, kind, cols, size=1.0, crackle=False):
        if kind != 'grand':
            y -= 115          # keep bursts clear of the temple silhouette
        F.append(dict(t=t, x=x, y=y, kind=kind, cols=cols, size=size, crackle=crackle))

    add(28.7, 360, 560, 'peony', [GOLD, SAFFRON], 1.0, True)
    add(31.0, 215, 470, 'ring', [CYAN, CREAM], 0.9)
    add(31.7, 510, 430, 'peony', [SAFFRON, GOLD], 1.0, True)
    add(33.3, 360, 380, 'willow', [GOLD, CREAM], 1.1)
    add(34.6, 175, 540, 'peony', [PINK, CREAM], 0.9)
    add(35.1, 548, 505, 'peony', [CYAN, BLUE], 0.9)
    add(36.6, 360, 470, 'heart', [RED, PINK], 1.0)       # the heart moment

    pals = [[GOLD, SAFFRON], [CYAN, CREAM], [PINK, CREAM], [SAFFRON, RED],
            [BLUE, CYAN], [GOLD, CREAM], [PURPLE, PINK], [GREEN, CREAM]]
    kinds = ['peony', 'ring', 'willow', 'peony']
    t = 37.9
    i = 0
    while t < 40.2:
        add(t, rnd.randint(120, 600), rnd.randint(330, 560), kinds[i % 4],
            pals[rnd.randrange(len(pals))], rnd.uniform(.85, 1.05), rnd.random() < .5)
        t += 0.55
        i += 1

    add(T_TEXT, 360, 300, 'grand', [GOLD, SAFFRON, CREAM], 1.35, True)

    t = 44.2
    side = 0
    while t < 57.0:
        x = rnd.randint(70, 190) if side % 2 == 0 else rnd.randint(530, 650)
        add(t, x, rnd.randint(300, 540), kinds[rnd.randrange(4)],
            pals[rnd.randrange(len(pals))], rnd.uniform(.75, .95), rnd.random() < .4)
        t += rnd.uniform(1.0, 1.6)
        side += 1
    F.sort(key=lambda f: f['t'])
    return F


DIYAS = diya_layout()
DIYA_T = diya_times(len(DIYAS))
FIREWORKS = make_fireworks()
