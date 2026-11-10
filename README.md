# 🪔 DIWALI CINEMATIC
### A Procedural Festival Film Engine · Built by HM BHOLA

<p align="center">
  <strong>Where Mathematics Meets Art, and Code Becomes Celebration.</strong>
</p>

<p align="center">
  A fully procedural, cinematic Diwali experience engineered with Python.
  <br>
  No stock footage. No pre-rendered visuals. No external audio assets.
  <br>
  Every particle, flame, light, animation, and sound is generated programmatically.
</p>

---

## ◈ PROJECT OVERVIEW

**Diwali Cinematic** is a procedural animation project that transforms Python code into a cinematic festival experience.

Designed as a 60-second vertical film in **9:16 aspect ratio**, the project combines particle systems, dynamic lighting, procedural audio synthesis, animated environments, and cinematic camera effects to recreate the atmosphere of a grand Diwali celebration.

Rather than relying on pre-made visual assets, the experience is constructed through code using mathematical calculations, animation systems, and real-time rendering techniques.

### Project Highlights

| Specification | Details |
|---|---|
| Project | Diwali Cinematic |
| Creator | HM BHOLA |
| Language | Python |
| Graphics Engine | Pygame |
| Numerical Computing | NumPy |
| Video Format | MP4 |
| Resolution | 1080 × 1920 |
| Aspect Ratio | 9:16 |
| Target Frame Rate | 30 FPS |
| Duration | Approximately 60 seconds |
| Audio | Procedurally Generated |

---

## ◈ THE CINEMATIC EXPERIENCE

The animation follows a carefully structured four-stage visual sequence.

### 01 — THE FIRST LIGHT
**Darkness → Illumination**

The journey begins in complete darkness.

A single diya is illuminated, introducing the first source of light. Gradually, additional diyas light up the courtyard, creating a warm and atmospheric environment.

### 02 — THE RANGOLI AWAKENS
**Mathematics → Visual Art**

A complex mandala-inspired rangoli emerges from the centre.

Featuring more than 100 visual layers, coloured particles expand outward to create an intricate geometric pattern inspired by traditional Indian rangoli art.

### 03 — THE FIREWORKS SYMPHONY
**Particles → Celebration**

Rockets launch into the night sky behind a beautifully illuminated temple skyline.

The fireworks system features multiple explosion patterns:

- Peony
- Ring
- Willow
- Crackle
- Heart-shaped fireworks

Each explosion combines particle movement, colour variation, and light effects to create a dynamic visual experience.

### 04 — THE GOLDEN FINALE
**Light → Celebration**

The cinematic sequence reaches its climax with a massive golden fireworks explosion.

Particles converge to form the words:

# HAPPY DIWALI

A final visual tribute celebrating the festival of lights.

---

## ◈ TECHNICAL FEATURES

The project combines multiple procedural graphics and audio techniques.

### Graphics & Rendering
- Procedural visual generation.
- Dynamic light-map system.
- Particle-based animation.
- Multi-layered rangoli generation.
- Procedural fireworks simulation.
- Glowing temple windows.
- Animated sky lanterns.

### Cinematic Effects
- Camera tilt-up and pull-back movements.
- Camera shake during explosions.
- Bloom and glow effects.
- Cinematic vignette.
- Film grain.
- Dynamic illumination and environmental lighting.

### Procedural Audio Engine
The soundtrack is generated programmatically without external audio files.

Sound elements include:

- Temple bells synchronized with diya lighting.
- Atmospheric drone pads.
- Rocket launch whooshes.
- Fireworks explosions.
- Crackling particle effects.
- Golden finale chord.

### Branding & Identity
The **HM BHOLA** watermark remains visible in the top-left and bottom-right corners throughout the animation.

---

## ◈ TECHNOLOGY STACK

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pygame | Rendering, animation and visual output |
| NumPy | Numerical operations and mathematical computations |
| imageio-ffmpeg | MP4 video exporting |

**Development Philosophy:** Procedural generation over pre-made assets.

---

## ◈ PROJECT STRUCTURE

```text
DIWALI-CINEMATIC/
│
└── Diwali_Cinematic_HM_BHOLA/
    │
    ├── main.py
    ├── config.py
    ├── world.py
    ├── audio.py
    ├── requirements.txt
    └── README.md
```

| File | Responsibility |
|---|---|
| `main.py` | Application entry point and execution |
| `config.py` | Configuration and animation settings |
| `world.py` | Environment, visual elements and animation |
| `audio.py` | Procedural soundtrack and sound generation |
| `requirements.txt` | Project dependencies |
| `README.md` | Project documentation |

---

## ◈ INSTALLATION & SETUP

### Prerequisites

- Python installed on your system.
- pip package manager.
- A compatible desktop environment for Pygame.

### 01 — Clone the Repository

```bash
git clone https://github.com/hmbholamajhi-eng/DIWALI-CINEMATIC-FIREWORKS.git
```

### 02 — Navigate to the Project

```bash
cd DIWALI-CINEMATIC-FIREWORKS/Diwali_Cinematic_HM_BHOLA
```

### 03 — Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip install pygame numpy imageio-ffmpeg
```

**Note:** `imageio-ffmpeg` is required only when exporting the MP4 video.

---

## ◈ EXECUTION MODES

### Real-Time Playback

Launch the cinematic experience with audio:

```bash
python main.py
```

### Low-Quality Rendering

For systems with limited processing capabilities:

```bash
python main.py --quality low
```

### Cinematic Video Export

Generate the complete cinematic film:

```bash
python main.py --render
```

### Custom Export Filename

Specify your preferred output filename:

```bash
python main.py --render my.mp4
```

**Default Export Specifications**

| Parameter | Output |
|---|---|
| Resolution | 1080 × 1920 |
| Aspect Ratio | 9:16 |
| Frame Rate | 30 FPS target |
| Format | MP4 |
| Audio | Included |

The render mode targets a consistent 30 FPS output independently of real-time playback speed.

---

## ◈ KEYBOARD CONTROLS

| Key | Function |
|---|---|
| `ESC` | Exit application |
| `SPACE` | Restart animation |
| `F` | Toggle fullscreen |

---

## ◈ CUSTOMIZATION & CONFIGURATION

The animation can be customized through the project's configuration and world-generation modules.

### `config.py`

Modify the main animation parameters:

- `BRAND` — Branding and footer text.
- `T_TEXT` — Timing of the cinematic finale.
- `make_fireworks()` — Fireworks schedule, launch timing, positions, types, and colours.

### `world.py`

Customize the final cinematic title:

- `HAPPY`
- `DIWALI`
- Subtitle

The project structure separates configuration, visual generation, audio synthesis, and application execution to keep the implementation organized.

---

## ◈ PERFORMANCE & OUTPUT

For the best video-export experience, use:

```bash
python main.py --render
```

The renderer targets a 30 FPS output, regardless of the speed at which the animation plays on your computer.

For lighter real-time playback, use:

```bash
python main.py --quality low
```

Actual rendering performance depends on hardware capabilities and system resources.

---

## ◈ PROJECT PHILOSOPHY

This project explores how programming can become a medium for digital art.

It demonstrates the creative possibilities of combining:

- Mathematical geometry.
- Procedural animation.
- Particle simulations.
- Dynamic lighting.
- Audio synthesis.
- Cinematic storytelling.

The objective is simple:

**Build an entire cinematic celebration through code, rather than assembling it from pre-existing media assets.**

---

## ◈ AUTHOR & CREDITS

<p align="center">
  <strong>DESIGNED & ENGINEERED BY</strong>
  <br><br>
  <strong>HM BHOLA</strong>
  <br>
  Python Developer · Creative Technology Enthusiast
  <br><br>
  <a href="https://github.com/hmbholamajhi-eng">
    GitHub Profile
  </a>
</p>

<p align="center">
  Made with ❤️, Python, Mathematics & Imagination.
  <br><br>
  <strong>HAPPY DIWALI 🪔</strong>
  <br>
  <em>Let There Be Light. Let There Be Code.</em>
</p>

---

<p align="center">
  © HM BHOLA · DIWALI CINEMATIC
  <br>
  An independent procedural animation project.
</p>
