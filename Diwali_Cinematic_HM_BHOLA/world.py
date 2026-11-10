"""
The whole visual world. Pipeline per frame:
 albedo scene (sky, floor, rangoli, diya bodies)
 -> multiplied by a dynamic lightmap (diyas + firework flashes)
 -> additive layers (glow, stars, fireworks) -> skyline -> flames -> title
 -> bloom -> camera move -> vignette, grain, fade.
"""
import math
import random
import numpy as np
import pygame
from config import *

BA = pygame.BLEND_RGB_ADD
BM = pygame.BLEND_RGB_MULT
BS = pygame.BLEND_RGB_SUB


def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------------ sprites
def radial(size, power=2.0, color=(255, 255, 255)):
    r = size / 2
    y, x = np.mgrid[0:size, 0:size]
    d = np.sqrt((x - r + .5) ** 2 + (y - r + .5) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** power
    arr = np.zeros((size, size, 3), np.uint8)
    for i, c in enumerate(color):
        arr[..., i] = (a * c).astype(np.uint8)
    return pygame.surfarray.make_surface(arr.swapaxes(0, 1)).convert()


def star_sprite(size=96, color=(255, 230, 160)):
    r = size / 2
    y, x = np.mgrid[0:size, 0:size]
    x = (x - r + .5) / r
    y = (y - r + .5) / r
    core = np.exp(-(x * x + y * y) * 16)
    h = np.exp(-(y / 0.05) ** 2) * np.clip(1 - np.abs(x), 0, 1) ** 2
    v = np.exp(-(x / 0.05) ** 2) * np.clip(1 - np.abs(y), 0, 1) ** 2
    a = np.clip(core + h + v, 0, 1)
    arr = np.zeros((size, size, 3), np.uint8)
    for i, c in enumerate(color):
        arr[..., i] = (a * c).astype(np.uint8)
    return pygame.surfarray.make_surface(arr.swapaxes(0, 1)).convert()


def vgrad(w, h, stops):
    ys = np.linspace(0, 1, h)
    arr = np.zeros((w, h, 3), np.float32)
    for ch in range(3):
        col = np.interp(ys, [s[0] for s in stops], [s[1][ch] for s in stops])
        arr[:, :, ch] = col[None, :]
    return pygame.surfarray.make_surface(arr.astype(np.uint8)).convert()


FLAME_PTS = []
for i in range(0, 13):
    u = (i / 12) ** 1.0
    hw = 0.5 * math.sin(math.pi * max(u, 0.04) ** 0.62) * (1 - 0.15 * u)
    FLAME_PTS.append((hw, u))


# ------------------------------------------------------------------ static art
def build_sky():
    sky = vgrad(W, HZ + 2, [(0, (12, 10, 50)), (.5, (40, 24, 95)), (.82, (110, 50, 90)), (1, (170, 72, 45))])
    return sky


def build_moon():
    s = pygame.Surface((260, 260), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 244, 214), (130, 130), 34)
    pygame.draw.circle(s, (0, 0, 0, 0), (146, 120), 31)
    return s


def build_floor():
    h = H - HZ
    f = vgrad(W, h, [(0, (125, 98, 90)), (1, (92, 70, 70))])
    vx, vy = W / 2, HZ - 140
    line = (66, 48, 52)
    for xb in range(-2400, 3200, 150):
        pygame.draw.line(f, line, (vx, vy - HZ), (xb, h), 2)
    for k in range(1, 15):
        y = int(h * (k / 15) ** 2.1)
        pygame.draw.line(f, line, (0, y), (W, y), 2)
    return f


def build_skyline():
    surf = pygame.Surface((W, HZ + 8), pygame.SRCALPHA)
    rnd = random.Random(4)
    far = (16, 10, 32)
    near = (6, 4, 13)
    windows = []
    x = -10
    while x < W:
        w = rnd.randint(28, 64)
        h = rnd.randint(18, 58)
        pygame.draw.rect(surf, far, (x, HZ - h, w, h + 8))
        if rnd.random() < .35:
            pygame.draw.circle(surf, far, (x + w // 2, HZ - h), w // 3)
        x += w + rnd.randint(-6, 2)

    def bldg(x, w, h, dome=False):
        pygame.draw.rect(surf, near, (x, HZ - h, w, h + 8))
        if dome:
            pygame.draw.ellipse(surf, near, (x + w * .15, HZ - h - w * .32, w * .7, w * .64))
            pygame.draw.rect(surf, near, (x + w / 2 - 1, HZ - h - w * .32 - 14, 2, 14))
        for yy in range(HZ - h + 10, HZ - 10, 16):
            for xx in range(x + 8, x + w - 8, 14):
                if rnd.random() < .55:
                    windows.append((xx, yy, 5, 7, rnd.uniform(3, 34), rnd.uniform(0, 6.28)))

    bldg(0, 92, 118, True)
    bldg(90, 70, 72)
    bldg(158, 62, 96, True)
    bldg(226, 56, 60)
    bldg(500, 56, 64)
    bldg(560, 64, 98, True)
    bldg(626, 70, 72)
    bldg(690, 40, 120, True)

    def shikhara(cx, by, w, h):
        L, R = [], []
        n = 24
        for i in range(n + 1):
            u = i / n
            hw = w / 2 * (1 - u) ** 0.62 * (1 + 0.07 * math.sin(u * 38))
            L.append((cx - hw, by - h * u))
            R.append((cx + hw, by - h * u))
        pygame.draw.polygon(surf, near, L + R[::-1])
        pygame.draw.ellipse(surf, near, (cx - w * .11, by - h - w * .045, w * .22, w * .09))
        pygame.draw.rect(surf, near, (cx - 1.5, by - h - w * .17, 3, w * .14))
        pygame.draw.circle(surf, near, (int(cx), int(by - h - w * .19)), max(3, int(w * .03)))

    pygame.draw.rect(surf, near, (128, HZ - 8, 464, 16))
    pygame.draw.rect(surf, near, (150, HZ - 18, 420, 14))
    pygame.draw.rect(surf, near, (205, HZ - 76, 310, 60))
    shikhara(360, HZ - 76, 150, 170)
    shikhara(272, HZ - 76, 86, 100)
    shikhara(448, HZ - 76, 86, 100)
    for cx in (226, 494):
        pygame.draw.ellipse(surf, near, (cx - 24, HZ - 104, 48, 56))
        pygame.draw.rect(surf, near, (cx - 1, HZ - 118, 2, 16))
    # glowing temple arches
    for xx in range(222, 500, 30):
        windows.append((xx, HZ - 62, 11, 26, rnd.uniform(5, 18), rnd.uniform(0, 6.28)))
    return surf, windows


def build_footer():
    f = pygame.font.SysFont('segoeui,arial,dejavusans,verdana', 22)
    a = f.render('Made with ', True, (225, 225, 238))
    b = f.render(BRAND, True, CYAN)
    hs = 26
    w = a.get_width() + hs + 8 + b.get_width()
    s = pygame.Surface((w, 34), pygame.SRCALPHA)
    s.blit(a, (0, 4))
    pts = []
    for i in range(40):
        t = i / 40 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((a.get_width() + 4 + hs / 2 + x * hs / 36, 16 + y * hs / 36))
    pygame.draw.polygon(s, RED, pts)
    s.blit(b, (a.get_width() + hs + 8, 4))
    return s


def build_corner_brand():
    """Create a compact gold HM BHOLA watermark for both video corners."""
    font = pygame.font.SysFont('segoeui,arial,dejavusans,verdana', 18, bold=True)
    label = font.render(BRAND, True, (255, 222, 154))
    pad_x, pad_y = 13, 8
    width = label.get_width() + pad_x * 2 + 10
    height = label.get_height() + pad_y * 2
    tag = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = tag.get_rect()
    pygame.draw.rect(tag, (18, 10, 24, 205), rect, border_radius=9)
    pygame.draw.rect(tag, (231, 177, 78, 235), rect, width=1, border_radius=9)
    pygame.draw.circle(tag, GOLD, (pad_x + 2, height // 2), 3)
    tag.blit(label, (pad_x + 11, pad_y - 1))
    return tag


# ------------------------------------------------------------------ rangoli
class Rangoli:
    def __init__(s):
        R = RANGOLI_R
        s.w, s.h = 2 * R, int(2 * R * SQ)
        S = 1200
        c = S // 2
        flat = pygame.Surface((S, S), pygame.SRCALPHA)
        MAROON = (74, 10, 40)

        def circ(r, col):
            pygame.draw.circle(flat, col, (c, c), int(r))

        def dots(n, r, rad, cols, off=0):
            for k in range(n):
                a = math.radians(off + 360 * k / n)
                pygame.draw.circle(flat, cols[k % len(cols)], (int(c + r * math.cos(a)), int(c + r * math.sin(a))), rad)

        def petal(r0, r1, deg, width, layers):
            a = math.radians(deg)
            ca, sa = math.cos(a), math.sin(a)
            nx, ny = -sa, ca
            for col, k in layers:
                rr0 = r0 + (r1 - r0) * (1 - k) * .35
                rr1 = r0 + (r1 - r0) * (.5 + .5 * k)
                L, Rr = [], []
                n = 16
                for i in range(n + 1):
                    u = i / n
                    r = rr0 + (rr1 - rr0) * u
                    off = width * k / 2 * math.sin(math.pi * u ** .75)
                    px, py = c + r * ca, c + r * sa
                    L.append((px + nx * off, py + ny * off))
                    Rr.append((px - nx * off, py - ny * off))
                pygame.draw.polygon(flat, col, L + Rr[::-1])

        circ(592, GOLD)
        circ(584, MAROON)
        dots(72, 560, 9, [CYAN, CREAM])
        for k in range(24):
            petal(440, 548, k * 15, 40, [(PINK if k % 2 == 0 else SAFFRON, 1.0), (CREAM, .5)])
        dots(24, 500, 7, [GOLD], off=7.5)
        circ(434, GOLD)
        circ(424, MAROON)
        for k in range(16):
            petal(215, 405, k * 22.5, 66, [((230, 30, 120), 1.0), (SAFFRON, .72), (GOLD, .46), (CREAM, .2)])
        for k in range(16):
            petal(215, 330, k * 22.5 + 11.25, 28, [(BLUE, 1.0), (CYAN, .55)])
        dots(16, 414, 8, [CREAM], off=11.25)
        circ(222, RED)
        circ(212, CREAM)
        circ(204, (0, 50, 150))
        dots(36, 188, 6, [GOLD, CREAM])
        for k in range(12):
            petal(40, 172, k * 30, 56, [(SAFFRON, 1.0), (GOLD, .62), (CREAM, .3)])
        for k in range(12):
            petal(40, 120, k * 30 + 15, 30, [(PINK, 1.0), (CREAM, .5)])
        circ(66, RED)
        circ(52, GOLD)
        circ(38, CREAM)
        circ(24, PINK)
        circ(10, WHITE)

        sc = pygame.transform.smoothscale(flat, (s.w, s.h))
        s.surf = sc.copy()
        s.rgb = pygame.surfarray.array3d(sc).astype(np.int16)
        s.alpha = pygame.surfarray.array_alpha(sc).astype(np.int16)
        X, Y = np.meshgrid(np.arange(s.w), np.arange(s.h), indexing='ij')
        dx = (X - s.w / 2) / (s.w / 2)
        dy = (Y - s.h / 2) / (s.h / 2)
        r = np.hypot(dx, dy)
        th = np.arctan2(dy, dx)
        rn = np.random.default_rng(5)
        o = r + .07 * (th / (2 * math.pi) + .5) + .07 * rn.random((s.w, s.h))
        s.order = o / o.max()
        s.last_p = -1.0
        s.pos = (RC[0] - s.w // 2, RC[1] - s.h // 2)
        s.fresh = None
        s.p = 0.0

    def update(s, t):
        p = smooth((t - T_RANG0) / (T_RANG1 - T_RANG0)) * 1.06
        s.p = p
        if t < T_RANG0 or abs(p - s.last_p) < .002:
            return
        s.last_p = p
        mask = s.order <= p
        fresh = mask & (s.order > p - .045)
        s.fresh = fresh
        a = pygame.surfarray.pixels_alpha(s.surf)
        a[:] = np.where(mask, s.alpha, 0)
        del a
        c = pygame.surfarray.pixels3d(s.surf)
        c[:] = np.clip(s.rgb + fresh[..., None] * np.array([140, 115, 70], np.int16), 0, 255)
        del c

    def draw(s, f, t):
        if t >= T_RANG0:
            f.blit(s.surf, s.pos)


# ------------------------------------------------------------------ diyas
class Diya:
    def __init__(s, x, y, sc, t_on, i):
        s.x, s.y, s.sc, s.t_on = x, y, sc, t_on
        s.ph = random.Random(i * 7 + 1).random() * 6.28
        s.dia = int(round(95 * sc / 4)) * 4
        s.gdia = int(round(70 * sc / 2)) * 2

    def g(s, t):
        return smooth((t - s.t_on) / 1.5) if t >= s.t_on else 0.0

    def flick(s, t):
        return 0.9 + .1 * math.sin(t * 13 + s.ph) + .05 * math.sin(t * 23 + s.ph * 2)

    def body(s, f, t):
        x, y, k = s.x, s.y, s.sc
        lit = s.g(t)
        E = pygame.draw.ellipse
        E(f, (8, 6, 10), (int(x - 27 * k), int(y + 4 * k), int(54 * k), int(14 * k)))
        E(f, (176, 84, 44), (int(x - 23 * k), int(y - 8 * k), int(46 * k), int(24 * k)))
        E(f, (120, 52, 28), (int(x - 23 * k), int(y + 2 * k), int(46 * k), int(14 * k)))
        E(f, (214, 118, 62), (int(x - 23 * k), int(y - 13 * k), int(46 * k), int(13 * k)))
        oc = (60, 28, 12) if lit < .01 else (int(100 + 140 * lit), int(60 + 90 * lit), int(14 + 20 * lit))
        E(f, oc, (int(x - 18 * k), int(y - 11.5 * k), int(36 * k), int(8 * k)))
        for i in range(-2, 3):
            pygame.draw.circle(f, (226, 170, 60), (int(x + i * 8 * k), int(y + 7 * k)), max(1, int(1.5 * k)))

    def flame(s, f, t, glow_sprite):
        g = s.g(t)
        if g <= 0:
            return
        k = s.sc
        fl = s.flick(t)
        x = s.x
        y = s.y - 11 * k
        h = 36 * k * g * fl
        w = 13 * k * g
        sway = math.sin(t * 7 + s.ph) * 2.4 * k * g
        glow = glow_sprite(s.gdia, int(round(8 * g * fl)))
        if glow:
            f.blit(glow, (int(x - s.gdia / 2), int(y - h * .45 - s.gdia / 2)), special_flags=BA)
        for col, sc_w, sc_h in (((255, 110, 20), 1.0, 1.0), ((255, 185, 55), .66, .8),
                                ((255, 240, 160), .38, .55), ((255, 255, 235), .18, .32)):
            pts = [(x + sway * u * u + hw * 1.05 * w * sc_w * (1 if side else -1), y - u * h * sc_h)
                   for side in (0, 1) for hw, u in (FLAME_PTS if side == 0 else FLAME_PTS[::-1])]
            pygame.draw.polygon(f, col, pts)
        dt_ = t - s.t_on
        if 0 <= dt_ < .7:
            return dt_


# ------------------------------------------------------------------ fireworks
class Fireworks:
    def __init__(s):
        s.sched = sorted(FIREWORKS, key=lambda f: f['t'] - ROCKET_T)
        s.next = 0
        s.rockets = []
        s.parts = []
        s.flashes = []
        s.shake = 0.0
        s.rng = random.Random(99)
        s.fx = pygame.Surface((W, H)).convert()
        s.fx.fill((0, 0, 0))

    def add_spark(s, x, y, vx, vy, life, col, grav=0, drag=1.0, size=1):
        s.parts.append([x, y, vx, vy, life, life, col[0], col[1], col[2], drag, grav, size, 0, x, y])

    def shell(s, kind, x, y, k, cols, crackle, t):
        rng = s.rng

        def mk(c):
            j = rng.uniform(.85, 1.1)
            return (min(255, int(c[0] * j)), min(255, int(c[1] * j)), min(255, int(c[2] * j)))

        def add(vx, vy, life, col, drag, grav, size=2, crack=0):
            s.parts.append([x, y, vx, vy, life, life, col[0], col[1], col[2], drag, grav, size, crack, x, y])

        if kind == 'peony':
            for i in range(int(150 * k)):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(.88, 1.0) * 300 * k
                c = mk(cols[0] if rng.random() < .55 else cols[-1])
                add(math.cos(a) * v, math.sin(a) * v, rng.uniform(1.8, 2.6), c, 1.25, 70, 2,
                    1 if crackle and rng.random() < .3 else 0)
            for i in range(int(55 * k)):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(.3, .5) * 300 * k
                add(math.cos(a) * v, math.sin(a) * v, rng.uniform(1.4, 2.0), mk(CREAM), 1.4, 60, 2)
        elif kind == 'ring':
            for i in range(int(90 * k)):
                a = 6.2832 * i / int(90 * k)
                add(math.cos(a) * 250 * k, math.sin(a) * 250 * k, 2.4, mk(cols[0]), 1.2, 50, 2)
            for i in range(int(56 * k)):
                a = 6.2832 * i / int(56 * k) + .1
                add(math.cos(a) * 140 * k, math.sin(a) * 140 * k, 2.2, mk(cols[-1]), 1.2, 50, 2)
            for i in range(24):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(20, 90)
                add(math.cos(a) * v, math.sin(a) * v, 1.4, mk(WHITE), 1.5, 30, 1)
        elif kind == 'willow':
            for i in range(int(110 * k)):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(110, 280) * k
                add(math.cos(a) * v, math.sin(a) * v, rng.uniform(3.0, 4.2), mk(cols[0]), 1.5, 150, 2)
            for i in range(30):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(40, 230) * k
                add(math.cos(a) * v, math.sin(a) * v, rng.uniform(2.0, 3.0), mk(cols[-1]), 1.6, 140, 1)
        elif kind == 'heart':
            for scale, col_i, n in ((15.5, 0, 130), (8.8, 1, 70)):
                for i in range(int(n)):
                    th = 6.2832 * i / n
                    hx = 16 * math.sin(th) ** 3
                    hy = 13 * math.cos(th) - 5 * math.cos(2 * th) - 2 * math.cos(3 * th) - math.cos(4 * th)
                    add(hx * scale * k, -hy * scale * k, 3.4, mk(cols[col_i]), 1.4, 22, 3 if col_i == 0 else 2)
            for i in range(30):
                a = rng.uniform(0, 6.2832)
                v = rng.uniform(10, 60)
                add(math.cos(a) * v, math.sin(a) * v, 2.0, mk(CREAM), 1.2, 20, 1)

    def burst(s, f, t):
        x, y, kind, cols, k = f['x'], f['y'], f['kind'], f['cols'], f['size']
        s.flashes.append([x, y, cols[0], t, min(1.3, k)])
        s.shake = max(s.shake, 5.0 * k)
        if kind == 'grand':
            s.shell('peony', x, y, 1.35, [GOLD, SAFFRON], True, t)
            s.shell('ring', x, y, 1.25, [CREAM, GOLD], False, t)
            s.shell('willow', x, y, 1.3, [GOLD, CREAM], False, t)
            s.flashes.append([x, y, CREAM, t, 1.6])
            s.shake = 12
        else:
            s.shell(kind, x, y, k, cols, f.get('crackle', False), t)

    def update(s, t, dt):
        while s.next < len(s.sched) and t >= s.sched[s.next]['t'] - ROCKET_T:
            f = s.sched[s.next]
            s.rockets.append([f, f['t'] - ROCKET_T, 360 + (f['x'] - 360) * .35])
            s.next += 1
        alive = []
        for r in s.rockets:
            f, t0, sx = r
            u = (t - t0) / ROCKET_T
            if u >= 1:
                s.burst(f, t)
                continue
            e = 1 - (1 - u) ** 2.2
            x = lerp(sx, f['x'], e) + math.sin(u * 18) * 5 * (1 - u)
            y = lerp(HZ - 6, f['y'], e)
            r.append((x, y))
            for _ in range(3):
                s.add_spark(x, y, s.rng.uniform(-18, 18), s.rng.uniform(10, 50), s.rng.uniform(.3, .7),
                            (255, 190, 90), 40, 1.0, 1)
            pygame.draw.circle(s.fx, (255, 235, 190), (int(x), int(y)), 3)
            alive.append(r[:3])
        s.rockets = alive
        k = 1.0
        surv = []
        for p in s.parts:
            p[13], p[14] = p[0], p[1]
            kd = math.exp(-p[9] * dt)
            p[2] *= kd
            p[3] = p[3] * kd + p[10] * dt
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[4] -= dt
            if p[4] > 0:
                surv.append(p)
            elif p[12]:
                for _ in range(3):
                    a = s.rng.uniform(0, 6.2832)
                    v = s.rng.uniform(40, 120)
                    s.add_spark(p[0], p[1], math.cos(a) * v, math.sin(a) * v, .35, (255, 250, 230), 20, 3.0, 1)
        s.parts = surv
        s.flashes = [f for f in s.flashes if math.exp(-(t - f[3]) * 2.6) * f[4] > .02]
        s.shake *= math.exp(-6 * dt)

    def draw(s, t, dt):
        fade = max(2, int(round(9 * dt * 60)))
        s.fx.fill((fade, fade, fade), special_flags=BS)
        rng = s.rng
        line = pygame.draw.line
        fx = s.fx
        for p in s.parts:
            fr = p[4] / p[5]
            kk = fr ** .6
            if fr < .3:
                kk *= .6 + .4 * rng.random()
            col = (int(p[6] * kk), int(p[7] * kk), int(p[8] * kk))
            line(fx, col, (p[13], p[14]), (p[0], p[1]), p[11])
        return fx


# ------------------------------------------------------------------ title
class Title:
    def __init__(s):
        names = 'trajanpro,cinzel,georgia,cambria,palatinolinotype,bookantiqua,timesnewroman,dejavuserif,serif'
        s.y0, s.hh = 140, 340

        def spaced(font, text, spacing):
            sf = [font.render(ch, True, (255, 255, 255)) for ch in text]
            w = sum(a.get_width() for a in sf) + spacing * (len(text) - 1)
            out = pygame.Surface((w, max(a.get_height() for a in sf)), pygame.SRCALPHA)
            x = 0
            for a in sf:
                out.blit(a, (x, 0))
                x += a.get_width() + spacing
            return out

        def fit(text, target, size, spacing, bold=True):
            while size > 20:
                font = pygame.font.SysFont(names, size, bold=bold)
                sf = spaced(font, text, spacing)
                if sf.get_width() <= target:
                    return sf
                size -= 4
            return sf

        def gold(sf, bottom=(230, 120, 25)):
            g = vgrad(sf.get_width(), sf.get_height(),
                      [(0, (255, 250, 205)), (.45, (255, 205, 75)), (1, bottom)])
            out = sf.copy()
            out.blit(g, (0, 0), special_flags=BM)
            return out

        line1 = gold(fit('HAPPY', 540, 150, 14))
        line2 = gold(fit('DIWALI', 650, 110, 8))
        sub = fit('LIGHT  .  JOY  .  PROSPERITY', 560, 26, 6)
        sub = gold(sub, (255, 190, 80))
        s.surf = pygame.Surface((W, s.hh), pygame.SRCALPHA)
        shadow = pygame.Surface((W, s.hh), pygame.SRCALPHA)
        pos1 = ((W - line1.get_width()) // 2, 225 - s.y0 - line1.get_height() // 2)
        pos2 = ((W - line2.get_width()) // 2, 335 - s.y0 - line2.get_height() // 2)
        pos3 = ((W - sub.get_width()) // 2, 425 - s.y0)
        for sf, p in ((line1, pos1), (line2, pos2)):
            tint = sf.copy()
            tint.fill((90, 35, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
            shadow.blit(tint, (p[0] + 3, p[1] + 4))
            s.surf.blit(sf, p)
        s.surf2 = shadow
        s.sub = pygame.Surface((W, s.hh), pygame.SRCALPHA)
        s.sub.blit(sub, pos3)
        # glow
        tmp = pygame.Surface((W, s.hh))
        tmp.blit(s.surf, (0, 0))
        g = pygame.transform.smoothscale(tmp, (W // 8, s.hh // 8))
        g = pygame.transform.smoothscale(g, (W, s.hh))
        g.fill((255, 150, 45), special_flags=BM)
        s.glow = g
        s.white = s.surf.copy()
        s.white.fill((255, 255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
        # dust points
        al = pygame.surfarray.array_alpha(s.surf)
        rgb = pygame.surfarray.array3d(s.surf)
        xs, ys = np.nonzero(al[::3, ::3] > 150)
        xs, ys = xs * 3, ys * 3
        s.tx = xs.astype(np.float32)
        s.ty = (ys + s.y0).astype(np.float32)
        s.col = rgb[xs, ys].astype(np.float32)
        n = len(xs)
        r = np.random.default_rng(21)
        ang = r.uniform(0, 6.2832, n)
        rad = 60 + 440 * r.random(n) ** .7
        s.sx = (W / 2 + np.cos(ang) * rad).astype(np.float32)
        s.sy = (330 + np.sin(ang) * rad * .8).astype(np.float32)
        s.delay = (r.random(n) * .9).astype(np.float32)
        vx, vy = s.tx - s.sx, s.ty - s.sy
        nr = np.hypot(vx, vy) + 1e-3
        amp = (r.random(n) - .5) * 260
        s.px = (-vy / nr * amp).astype(np.float32)
        s.py = (vx / nr * amp).astype(np.float32)
        s.tfx = pygame.Surface((W, H)).convert()
        s.tfx.fill((0, 0, 0))
        s.star = star_sprite(80)
        s.stars = []
        s.rnd = random.Random(8)
        s.shine_band = pygame.Surface((150, s.hh), pygame.SRCALPHA)
        for x in range(150):
            a = int(210 * max(0, math.sin(math.pi * x / 150)) ** 2)
            pygame.draw.line(s.shine_band, (255, 255, 255, a), (x, 0), (x, s.hh))

    def draw(s, f, t, dt):
        q = t - T_TEXT
        if q < 0:
            return
        fade = max(3, int(round(14 * dt * 60)))
        s.tfx.fill((fade, fade, fade), special_flags=BS)
        if q < 3.4:
            u = np.clip((q - s.delay) / 1.7, 0, 1)
            e = 1 - (1 - u) ** 3
            sw = np.sin(np.pi * u)
            X = s.sx + (s.tx - s.sx) * e + s.px * sw
            Y = s.sy + (s.ty - s.sy) * e + s.py * sw
            b = (0.75 + 0.7 * (1 - e) + 0.5 * sw)[:, None]
            C = np.clip(s.col * b + 60 * (1 - e)[:, None], 0, 255).astype(np.uint8)
            xi = np.clip(X.astype(np.int32), 0, W - 3)
            yi = np.clip(Y.astype(np.int32), 0, H - 3)
            arr = pygame.surfarray.pixels3d(s.tfx)
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                arr[xi + dx, yi + dy] = np.maximum(arr[xi + dx, yi + dy], C)
            del arr
        f.blit(s.tfx, (0, 0), special_flags=BA)
        if q > 2.4:
            a = smooth((q - 2.4) / 1.1)
            pulse = 0.55 + 0.2 * math.sin(q * 2.2)
            gl = s.glow.copy()
            v = int(255 * pulse * a)
            gl.fill((v, v, v), special_flags=BM)
            f.blit(gl, (0, s.y0), special_flags=BA)
            s.surf2.set_alpha(int(220 * a))
            f.blit(s.surf2, (0, s.y0))
            s.surf.set_alpha(int(255 * a))
            f.blit(s.surf, (0, s.y0))
            # shimmer sweep
            ph = (q * 0.28) % 1.6
            bx = int(-150 + ph * (W + 300))
            tmp = pygame.Surface((W, s.hh), pygame.SRCALPHA)
            tmp.blit(s.shine_band, (bx, 0))
            tmp.blit(s.white, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            tmp.set_alpha(int(255 * a))
            f.blit(tmp, (0, s.y0))
            # subtitle
            sa = smooth((q - 3.4) / 1.2)
            if sa > 0:
                s.sub.set_alpha(int(255 * sa))
                f.blit(s.sub, (0, s.y0))
            # twinkles
            if s.rnd.random() < min(1, dt * 22):
                i = s.rnd.randrange(len(s.tx))
                s.stars.append([s.tx[i], s.ty[i], q, s.rnd.uniform(.5, .9), s.rnd.uniform(.5, 1.1)])
            keep = []
            for st in s.stars:
                u = (q - st[2]) / st[3]
                if u < 1:
                    keep.append(st)
                    sz = max(8, int(70 * st[4] * math.sin(math.pi * u)))
                    sp = pygame.transform.smoothscale(s.star, (sz, sz))
                    f.blit(sp, (int(st[0] - sz / 2), int(st[1] - sz / 2)), special_flags=BA)
            s.stars = keep


# ------------------------------------------------------------------ the world
class World:
    def __init__(s, quality='high'):
        s.quality = quality
        s.canvas = pygame.Surface((W, H)).convert()
        s.frame = pygame.Surface((W, H)).convert()
        s.sky = build_sky()
        s.floor = build_floor()
        s.skyline, s.windows = build_skyline()
        s.moon = build_moon()
        s.moon_glow = radial(300, 2.0, (70, 62, 95))
        s.footer = build_footer()
        s.brand_tag = build_corner_brand()
        s.rangoli = Rangoli()
        s.diyas = [Diya(x, y, sc, t, i) for i, ((x, y, sc), t) in enumerate(zip(DIYAS, DIYA_T))]
        s.draw_order = sorted(s.diyas, key=lambda d: d.y)
        s.fw = Fireworks()
        s.title = Title()
        s.rng = random.Random(1)
        r = random.Random(5)
        s.stars = [(r.randrange(W), r.randrange(0, HZ - 30), r.random() * 6.28, r.uniform(.6, 2.2), r.choice([1, 1, 1, 2]))
                   for _ in range(240)]
        s.lanterns = [[r.uniform(60, 660), 24 + i * 1.7, r.uniform(.7, 1.3), r.uniform(0, 6.28)] for i in range(10)]
        # lightmap (quarter res)
        s.lw, s.lh = W // 4, H // 4
        s.lm = pygame.Surface((s.lw, s.lh)).convert()
        s.lm_base = vgrad(s.lw, s.lh, [(0, (52, 52, 80)), (HZ / H * .98, (86, 72, 92)), (HZ / H, (30, 27, 40)),
                                       (1, (14, 12, 22))])
        s.lcache = {}
        s.warm = radial(256, 1.8, (255, 172, 82))
        s.cwarm = radial(256, 1.3, (255, 160, 70))
        s.white_r = radial(256, 1.6, (255, 255, 255))
        s.gcache = {}
        s.glow_base = radial(128, 2.2, (255, 150, 50))
        s.hz_glow = vgrad(W, 260, [(0, (0, 0, 0)), (1, (255, 112, 38))])
        s.star_spr = star_sprite(64)
        s.vig = s._vignette()
        rn = np.random.default_rng(2)
        s.grain = []
        if quality == 'high':
            for _ in range(5):
                n = rn.integers(0, 11, (W, H), dtype=np.uint8)
                s.grain.append(pygame.surfarray.make_surface(np.stack([n, n, n], axis=2)).convert())
        s.sparkles = []
        s.last_t = 0.0

    # ---------------------------------------------------------- helpers
    def _vignette(s):
        y, x = np.mgrid[0:H, 0:W]
        d = np.sqrt(((x - W / 2) / (W * .62)) ** 2 + ((y - H / 2) / (H * .62)) ** 2)
        v = 255 * (1 - .62 * np.clip(d - .38, 0, 1) ** 1.5)
        v = np.clip(v, 40, 255).astype(np.uint8)
        arr = np.stack([v, v, (v * .97).astype(np.uint8)], axis=2).swapaxes(0, 1)
        return pygame.surfarray.make_surface(np.ascontiguousarray(arr)).convert()

    def _scaled(s, cache, key, base, size, mult):
        sp = cache.get(key)
        if sp is None:
            sp = pygame.transform.smoothscale(base, size) if size else base.copy()
            sp.fill(mult, special_flags=BM)
            cache[key] = sp
        return sp

    def glow_sprite(s, dia, lvl):
        if lvl <= 0:
            return None
        v = min(255, lvl * 32)
        return s._scaled(s.gcache, (dia, lvl), s.glow_base, (dia, dia), (v, v, v))

    # ---------------------------------------------------------- camera
    CAM = [(0, 1.40, .76), (8, 1.34, .76), (16, 1.20, .70), (26, 1.08, .60), (32, 1.0, .5), (40, 1.0, .5),
           (60, 1.07, .5)]

    def camera(s, t):
        k = s.CAM
        for i in range(len(k) - 1):
            if k[i][0] <= t <= k[i + 1][0]:
                u = smooth((t - k[i][0]) / (k[i + 1][0] - k[i][0]))
                return lerp(k[i][1], k[i + 1][1], u), lerp(k[i][2], k[i + 1][2], u)
        return k[-1][1], k[-1][2]

    # ---------------------------------------------------------- frame
    def render(s, out, t, dt):
        dt = min(max(dt, 1 / 120), 1 / 15)
        fw = s.fw
        fw.update(t, dt)
        s.rangoli.update(t)
        lit = sum(1 for d in s.diyas if d.t_on <= t)
        lit_frac = lit / len(s.diyas)
        ring_frac = clamp((lit - 5) / 22.0)

        # embers rising from flames
        if lit and s.rng.random() < dt * 40:
            d = s.diyas[s.rng.randrange(lit)]
            fw.add_spark(d.x, d.y - 20 * d.sc, s.rng.uniform(-14, 14), -s.rng.uniform(30, 70),
                         s.rng.uniform(1.0, 2.0), (255, 170, 70), -8, .6, 1)
        # rangoli frontier sparkles
        rg = s.rangoli
        if T_RANG0 < t < T_RANG1 + .8 and rg.fresh is not None:
            for _ in range(6):
                x, y = s.rng.randrange(rg.w), s.rng.randrange(rg.h)
                if rg.fresh[x, y]:
                    fw.add_spark(rg.pos[0] + x, rg.pos[1] + y, s.rng.uniform(-10, 10), -s.rng.uniform(20, 60),
                                 s.rng.uniform(.5, 1.0), (255, 225, 140), -10, .8, 1)

        f = s.frame
        f.blit(s.sky, (0, 0))
        f.blit(s.floor, (0, HZ))
        rg.draw(f, t)
        for d in s.draw_order:
            d.body(f, t)

        # ---- lightmap
        lm = s.lm
        lm.blit(s.lm_base, (0, 0))
        if lit_frac > 0:
            cw = int(W * 1.2 / 4)
            sp = s._scaled(s.lcache, ('c', int(lit_frac * 20)), s.cwarm, (cw, int(cw * .55)),
                           (int(150 * lit_frac ** .9),) * 3)
            lm.blit(sp, (RC[0] // 4 - cw // 2, RC[1] // 4 - int(cw * .55) // 2), special_flags=BA)
        for d in s.diyas:
            g = d.g(t)
            if g <= 0:
                continue
            lvl = int(round(14 * g * d.flick(t)))
            sp = s._scaled(s.lcache, (d.dia, lvl), s.warm, (d.dia, d.dia), (min(255, lvl * 13),) * 3)
            lm.blit(sp, (int(d.x / 4 - d.dia / 2), int((d.y - 14 * d.sc) / 4 - d.dia / 2)), special_flags=BA)
        for fl in fw.flashes:
            inten = math.exp(-(t - fl[3]) * 2.6) * fl[4]
            c = fl[2]
            m = (int(min(255, c[0] * inten * 1.0)), int(min(255, c[1] * inten)), int(min(255, c[2] * inten)))
            dia = int(160 * fl[4])
            sp = pygame.transform.smoothscale(s.white_r, (dia, dia))
            sp.fill(m, special_flags=BM)
            lm.blit(sp, (int(fl[0] / 4 - dia / 2), int(fl[1] / 4 - dia / 2)), special_flags=BA)
        big = pygame.transform.smoothscale(lm, (W, H))
        f.blit(big, (0, 0), special_flags=BM)

        # ---- additive sky layers
        hg = int(255 * (0.10 + .38 * lit_frac))
        sp = s._scaled(s.lcache, ('hz', hg // 8), s.hz_glow, None, (min(255, (hg // 8) * 8),) * 3)
        f.blit(sp, (0, HZ - 260), special_flags=BA)
        gain = smooth(t / 3.0)
        for x, y, ph, spd, sz in s.stars:
            v = (.55 + .45 * math.sin(t * spd + ph)) * gain * (1 - .55 * y / HZ)
            c = int(255 * v)
            if c < 22:
                continue
            col = (c, c, min(255, c + 25))
            if sz == 1:
                f.set_at((x, y), col)
            else:
                pygame.draw.rect(f, col, (x, y, 2, 2))
        mg = smooth((t - 1.0) / 4.0)
        if mg > 0:
            gsp = s._scaled(s.lcache, ('mg', int(mg * 10)), s.moon_glow, None, (int(255 * mg),) * 3)
            f.blit(gsp, (610 - 150, 78 - 150), special_flags=BA)
            s.moon.set_alpha(int(255 * mg))
            f.blit(s.moon, (610 - 130, 78 - 130))

        # ---- fireworks (behind skyline)
        fx = fw.draw(t, dt)
        f.blit(fx, (0, 0), special_flags=BA)

        # ---- skyline & windows
        f.blit(s.skyline, (0, 0))
        for x, y, w, h, ton, ph in s.windows:
            if t > ton:
                b = smooth((t - ton) / 2.0) * (.82 + .18 * math.sin(t * 3 + ph))
                col = (int(255 * b), int(185 * b), int(85 * b))
                pygame.draw.rect(f, col, (x, y, w, h))

        # ---- sky lanterns
        for L in s.lanterns:
            tt = t - L[1]
            if tt <= 0:
                continue
            y = HZ - 10 - 17 * tt
            if y < -40:
                continue
            x = L[0] + math.sin(tt * .6 + L[3]) * 14
            sc = L[2] * (0.6 + 0.4 * clamp(1 - tt / 38))
            a = int(255 * smooth(tt / 3))
            gd = int(60 * sc)
            gsp = s._scaled(s.lcache, ('ln', gd, a // 16), s.glow_base, (gd, gd), (int(a * .8),) * 3)
            f.blit(gsp, (int(x - gd / 2), int(y - gd / 2)), special_flags=BA)
            pygame.draw.rect(f, (int(255 * a / 255), int(150 * a / 255), int(50 * a / 255)),
                             (int(x - 4 * sc), int(y - 5 * sc), max(2, int(8 * sc)), max(3, int(11 * sc))))

        # ---- diya flames
        for d in s.draw_order:
            d.flame(f, t, s.glow_sprite)
        # ignition sparkle
        for d in s.diyas:
            u = t - d.t_on
            if 0 <= u < .8:
                sz = int(110 * d.sc * math.sin(math.pi * u / .8) ** .7) + 4
                sp = pygame.transform.smoothscale(s.star_spr, (sz, sz))
                f.blit(sp, (int(d.x - sz / 2), int(d.y - 24 * d.sc - sz / 2)), special_flags=BA)

        # ---- title
        s.title.draw(f, t, dt)

        # ---- bloom
        if s.quality == 'high':
            a = pygame.transform.smoothscale(f, (W // 4, H // 4))
            a.fill((46, 46, 46), special_flags=BS)
            b = pygame.transform.smoothscale(a, (W // 16, H // 16))
            b = pygame.transform.smoothscale(b, (W // 4, H // 4))
            b = pygame.transform.smoothscale(b, (W, H))
            b.fill((255, 255, 255), special_flags=BM)
            f.blit(b, (0, 0), special_flags=BA)

        # ---- camera
        z, cyf = s.camera(t)
        sh = fw.shake
        ox = s.rng.uniform(-1, 1) * sh
        oy = s.rng.uniform(-1, 1) * sh
        if z > 1.0005 or sh > .3:
            z = max(z, 1.012)
            cw, ch = W / z, H / z
            left = clamp(W / 2 + ox - cw / 2, 0, W - cw)
            top = clamp(cyf * H + oy - ch / 2, 0, H - ch)
            sub = f.subsurface((int(left), int(top), int(cw), int(ch)))
            pygame.transform.smoothscale(sub, (W, H), out)
        else:
            out.blit(f, (0, 0))

        # ---- footer + post
        fa = smooth((t - 1.5) / 2.0) * .85
        if fa > 0:
            s.footer.set_alpha(int(255 * fa))
            out.blit(s.footer, ((W - s.footer.get_width()) // 2, H - 58))
        out.blit(s.vig, (0, 0), special_flags=BM)
        if s.grain:
            out.blit(s.grain[int(t * 24) % len(s.grain)], (0, 0), special_flags=BA)

        # HM BHOLA watermark: top-left and bottom-right throughout the film.
        brand_alpha = int(225 * smooth((t - 0.15) / 0.7))
        s.brand_tag.set_alpha(brand_alpha)
        out.blit(s.brand_tag, (18, 20))
        out.blit(s.brand_tag, (W - s.brand_tag.get_width() - 18, H - s.brand_tag.get_height() - 105))

        v = int(255 * smooth(t / 2.4) * (1 - smooth((t - (DURATION - 1.8)) / 1.8)))
        if v < 255:
            out.fill((v, v, v), special_flags=BM)
        return out
