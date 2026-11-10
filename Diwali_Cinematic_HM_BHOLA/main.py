"""
DIWALI CINEMATIC  -  HM BHOLA
  python main.py                  -> play live (with sound)
  python main.py --render         -> export 1080x1920 MP4 reel with audio
  python main.py --quality low    -> lighter effects for slower PCs
Keys: ESC quit | SPACE restart | F fullscreen
"""
import os
import sys
import time
import wave
import argparse
import subprocess
import tempfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--render', nargs='?', const='Diwali_Cinematic_HM_BHOLA.mp4', help='export MP4 instead of playing')
    ap.add_argument('--quality', choices=['low', 'high'], default='high')
    ap.add_argument('--mute', action='store_true')
    ap.add_argument('--fullscreen', action='store_true')
    ap.add_argument('--seconds', type=float, default=None, help='limit render length (testing)')
    ap.add_argument('--shots', nargs='*', type=float, help='save PNG previews at these times (testing)')
    ap.add_argument('--shot-dir', default='shots')
    args = ap.parse_args()

    offline = args.render is not None or args.shots is not None
    if offline:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
    os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

    import pygame
    from config import W, H, DURATION, FPS, SAMPLE_RATE
    pygame.init()

    if offline:
        pygame.display.set_mode((16, 16))
    else:
        info = pygame.display.Info()
        sc = min(1.0, (info.current_h - 110) / H)
        size = (int(W * sc), int(H * sc))
        flags = pygame.RESIZABLE | (pygame.FULLSCREEN if args.fullscreen else 0)
        screen = pygame.display.set_mode(size, flags)
        pygame.display.set_caption('Happy Diwali  |  HM BHOLA')

    from world import World
    print('Building the world ...')
    world = World(args.quality)
    canvas = pygame.Surface((W, H)).convert()

    if args.shots is not None:
        os.makedirs(args.shot_dir, exist_ok=True)
        targets = sorted(args.shots)
        dt = 1 / 15
        t, i = 0.0, 0
        while i < len(targets):
            world.render(canvas, t, dt)
            if t >= targets[i] - 1e-6:
                p = os.path.join(args.shot_dir, 'shot_%05.1f.png' % targets[i])
                pygame.image.save(canvas, p)
                print('saved', p)
                i += 1
            t += dt
        return

    import audio
    print('Composing soundtrack ...')
    track = audio.build()

    if args.render is not None:
        import imageio_ffmpeg
        OW, OH = 1080, 1920
        seconds = args.seconds or DURATION
        n = int(seconds * FPS)
        tmpwav = os.path.join(tempfile.gettempdir(), 'diwali_audio.wav')
        with wave.open(tmpwav, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(track.tobytes())
        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', '%dx%d' % (OW, OH), '-r', str(FPS), '-i', '-', '-i', tmpwav,
               '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-maxrate', '14M', '-bufsize', '28M', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', args.render]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        big = pygame.Surface((OW, OH))
        tob = getattr(pygame.image, 'tobytes', None) or pygame.image.tostring
        t0 = time.time()
        for i in range(n):
            world.render(canvas, i / FPS, 1 / FPS)
            pygame.transform.smoothscale(canvas, (OW, OH), big)
            proc.stdin.write(tob(big, 'RGB'))
            if i % 30 == 0:
                el = time.time() - t0
                print('  frame %d/%d  (%.0f%%)  eta %.0fs' % (i, n, 100 * i / n, el / max(1, i) * (n - i)))
        proc.stdin.close()
        proc.wait()
        print('Done ->', os.path.abspath(args.render))
        return

    # ------------------------------------------------ live playback
    clock = pygame.time.Clock()
    snd = None
    if not args.mute:
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
            snd = pygame.sndarray.make_sound(track)
        except Exception as e:
            print('Audio disabled:', e)

    def start():
        if snd:
            snd.stop()
            snd.play()
        return time.perf_counter()

    t_start = start()
    last = t_start
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif e.key == pygame.K_SPACE:
                    world = World(args.quality)
                    t_start = start()
                elif e.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
        now = time.perf_counter()
        t = now - t_start
        dt = now - last
        last = now
        if t > DURATION + 2.5:
            world = World(args.quality)
            t_start = start()
            t = 0.0
        world.render(canvas, min(t, DURATION), dt)
        sw, sh = screen.get_size()
        if (sw, sh) == (W, H):
            screen.blit(canvas, (0, 0))
        else:
            k = min(sw / W, sh / H)
            tw, th = int(W * k), int(H * k)
            screen.fill((0, 0, 0))
            scaled = pygame.transform.smoothscale(canvas, (tw, th))
            screen.blit(scaled, ((sw - tw) // 2, (sh - th) // 2))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
