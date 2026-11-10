<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=230&color=0:120C05,35:4A2700,70:B87916,100:FFD700&text=DIWALI%20CINEMATIC&fontSize=43&fontColor=FFF4D0&fontAlignY=38&desc=A%20Procedural%20Festival%20Film%20Engine&descAlignY=58&descSize=17&animation=fadeIn" width="100%" />

<br>

<img src="https://img.shields.io/badge/CREATED%20BY-HM%20BHOLA-DAA520?style=for-the-badge&logo=github&logoColor=white" />
<img src="https://img.shields.io/badge/PYTHON-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PROJECT-PROCEDURAL%20ART-8A2BE2?style=for-the-badge" />

<br><br>

**Where Mathematics Meets Art, and Code Becomes Celebration.**

A cinematic Diwali experience engineered entirely through Python.

*No stock footage. No pre-rendered visuals. No external audio assets.*

**Every particle. Every flame. Every light. Every sound. Generated through code.**

<br>

<a href="https://github.com/hmbholamajhi-eng">
<img src="https://img.shields.io/badge/GitHub-HM%20BHOLA-181717?style=flat-square&logo=github" />
</a>

</div>

---

# 🪔 01. PROJECT OVERVIEW

**DIWALI CINEMATIC** is a fully procedural animation project that transforms mathematical calculations, programming logic, and creative engineering into a cinematic festival experience.

Designed as a 60-second vertical film, the project combines particle simulation, dynamic illumination, procedural audio synthesis, geometric animation, and cinematic camera movements.

The entire experience is generated programmatically using Python.

<div align="center">

| 🎬 Duration | 📱 Format | 🎨 Rendering | 🔊 Audio |
|:---:|:---:|:---:|:---:|
| ~60 Seconds | 9:16 Vertical | Procedural | Generated |

| 🖥️ Resolution | 🎞️ FPS Target | ⚙️ Engine |
|:---:|:---:|:---:|
| 1080 × 1920 | 30 FPS | Pygame |

</div>

---

# ⚡ 02. TECHNOLOGY STACK

<div align="center">

<img src="https://skillicons.dev/icons?i=python&theme=dark" />

<br>

<img src="https://img.shields.io/badge/Python-Core%20Logic-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Pygame-Graphics%20Engine-00A86B?style=for-the-badge" />
<img src="https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/FFmpeg-Video%20Export-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" />

</div>

| Technology | Implementation |
|---|---|
| Python | Core application and animation logic |
| Pygame | Graphics, rendering and real-time animation |
| NumPy | Numerical computation and mathematical operations |
| imageio-ffmpeg | MP4 video exporting |

---

# 🎥 03. THE CINEMATIC EXPERIENCE

The film follows four carefully structured visual sequences.

### 01 — THE FIRST LIGHT

**Darkness → Illumination**

The journey begins in complete darkness.

A single diya illuminates the environment. Gradually, additional diyas light up the courtyard, creating a warm cinematic atmosphere.

### 02 — THE RANGOLI AWAKENS

**Mathematics → Visual Art**

A complex mandala-inspired rangoli emerges from the centre.

Featuring more than 100 visual layers, coloured powder expands outward to create an intricate geometric pattern inspired by traditional Indian art.

### 03 — THE FIREWORKS SYMPHONY

**Particles → Celebration**

Rockets launch behind an illuminated temple skyline.

Firework patterns include:

- 🎆 Peony
- 🎆 Ring
- 🎆 Willow
- 🎆 Crackle
- ❤️ Heart-shaped explosions

Each explosion combines particle movement, colour variation, and dynamic illumination.

### 04 — THE GOLDEN FINALE

**Light → Celebration**

A massive golden fireworks explosion transforms its sparks into:

<div align="center">

# ✨ HAPPY DIWALI ✨

*A cinematic celebration of the festival of lights.*

</div>

---

# 🌟 04. ENGINEERING & VISUAL FEATURES

### Graphics Engine

- Procedural visual generation.
- Dynamic light-map system.
- Particle-based animation.
- Multi-layered rangoli generation.
- Procedural fireworks simulation.
- Glowing temple windows.
- Animated sky lanterns.

### Cinematic Rendering

- Camera tilt-up and pull-back movements.
- Camera shake during explosions.
- Bloom and glow effects.
- Cinematic vignette.
- Film grain.
- Dynamic environmental illumination.

### Procedural Audio Engine

The soundtrack is generated programmatically without external audio files.

- Temple bells synchronized with diya lighting.
- Atmospheric drone pads.
- Rocket launch whooshes.
- Fireworks explosions.
- Crackling particle effects.
- Golden finale chord.

### Personal Branding

The **HM BHOLA** watermark remains visible in the top-left and bottom-right corners throughout the animation.

---

# 🏗️ 05. PROJECT ARCHITECTURE

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
| `world.py` | Environment and visual generation |
| `audio.py` | Procedural soundtrack and sound generation |
| `requirements.txt` | Dependency management |
| `README.md` | Project documentation |

---

# ⚙️ 06. INSTALLATION & SETUP

### Prerequisites

- Python 3.11 or compatible version.
- pip package manager.
- Compatible desktop environment for Pygame.

### Step 01 — Clone Repository

```bash
git clone https://github.com/hmbholamajhi-eng/DIWALI-CINEMATIC-FIREWORKS.git
```

### Step 02 — Navigate to Project

```bash
cd DIWALI-CINEMATIC-FIREWORKS/Diwali_Cinematic_HM_BHOLA
```

### Step 03 — Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate on Windows:

```powershell
venv\Scripts\activate
```

### Step 04 — Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip install pygame numpy imageio-ffmpeg
```

> **Note:** `imageio-ffmpeg` is only required for MP4 video exporting.

---

# 🚀 07. EXECUTION MODES

### Real-Time Cinematic Playback

```bash
python main.py
```

Launch the complete animation with sound.

### Low-Quality Mode

```bash
python main.py --quality low
```

Designed for systems with limited processing capabilities.

### Cinematic Video Export

```bash
python main.py --render
```

Exports the cinematic animation as an MP4 video.

### Custom Export Filename

```bash
python main.py --render my.mp4
```

### Default Export Specifications

| Parameter | Specification |
|---|---|
| Resolution | 1080 × 1920 |
| Aspect Ratio | 9:16 |
| Frame Rate | 30 FPS target |
| Format | MP4 |
| Audio | Included |
| Duration | Approximately 60 seconds |

The renderer targets a consistent 30 FPS output independently of real-time playback speed. Actual rendering performance depends on hardware.

---

# 🎮 08. KEYBOARD CONTROLS

| Key | Action |
|---|---|
| `ESC` | Exit application |
| `SPACE` | Restart animation |
| `F` | Toggle fullscreen |

---

# 🎨 09. CUSTOMIZATION

The animation can be customized through the configuration and world-generation modules.

### `config.py`

| Parameter | Purpose |
|---|---|
| `BRAND` | Branding and footer text |
| `T_TEXT` | Timing of the cinematic finale |
| `make_fireworks()` | Firework schedule, positions, types and colours |

### `world.py`

Customize the final cinematic title:

- `HAPPY`
- `DIWALI`
- Subtitle

The project separates configuration, visual generation, audio synthesis, and application execution into dedicated modules.

---

# 🧠 10. DEVELOPMENT PHILOSOPHY

This project explores the intersection of programming, mathematics, digital art, and cinematic storytelling.

Its development demonstrates how:

- Mathematical geometry can generate complex visual patterns.
- Particle systems can simulate fireworks and environmental effects.
- Dynamic lighting can create atmospheric environments.
- Procedural audio can construct a complete soundtrack.
- Python can be used as a creative medium beyond conventional software applications.

**The objective: Build an entire cinematic celebration through code instead of assembling it from pre-existing media assets.**

---

# 👨‍💻 11. AUTHOR & BRAND IDENTITY

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:1A1005,50:6A410C,100:D4AF37&height=120&text=HM%20BHOLA&fontSize=40&fontColor=FFF5D6&animation=fadeIn" width="100%" />

### HM BHOLA

**Python Developer · Creative Technology Enthusiast**

Building ideas through code, logic, mathematics, and imagination.

<br>

<a href="https://github.com/hmbholamajhi-eng">
<img src="https://img.shields.io/badge/EXPLORE%20MY%20GITHUB-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

</div>

---

# ❤️ 12. FINAL WORD

A celebration of Indian culture, expressed through programming.

From a single diya to thousands of glowing particles, every frame represents the creative possibilities of software engineering.

<div align="center">

## 🪔 HAPPY DIWALI 🪔

**LET THERE BE LIGHT. LET THERE BE CODE.**

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFD700,50:B87916,100:120C05&height=110&section=footer" width="100%" />

**© HM BHOLA · DIWALI CINEMATIC**

*An independent procedural animation project.*

</div>
