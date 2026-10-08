#!/usr/bin/env python3
"""Generate the animated space-themed SVG assets used by the profile README.

Usage: python3 scripts/generate_space_assets.py
Writes assets/hero.svg, assets/divider.svg and assets/footer.svg.
Animations are pure SVG (SMIL), so they render on GitHub without JS.
"""
import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI', 'Inter', Helvetica, Arial, sans-serif"
MONO = "'Fira Code', 'JetBrains Mono', ui-monospace, Consolas, monospace"


def twinkling_stars(rng, count, width, height, r_range=(0.4, 1.5), colors=("#ffffff",)):
    out = []
    for _ in range(count):
        x, y = rng.uniform(0, width), rng.uniform(0, height)
        r = rng.uniform(*r_range)
        lo, hi = rng.uniform(0.1, 0.4), rng.uniform(0.7, 1.0)
        dur = rng.uniform(2.0, 6.0)
        begin = -rng.uniform(0, dur)
        color = rng.choice(colors)
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{color}" opacity="{hi:.2f}">'
            f'<animate attributeName="opacity" values="{hi:.2f};{lo:.2f};{hi:.2f}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "\n".join(out)


def drifting_layer(rng, count, width, height, dur, r_range, opacity):
    """A star layer duplicated side by side and translated by -width for a seamless loop."""
    dots = []
    for _ in range(count):
        x, y, r = rng.uniform(0, width), rng.uniform(0, height), rng.uniform(*r_range)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
        dots.append(f'<circle cx="{x + width:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    return (
        f'<g fill="#c0caf5" opacity="{opacity}">'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{width} 0" '
        f'dur="{dur}s" repeatCount="indefinite"/>'
        + "".join(dots)
        + "</g>"
    )


def shooting_star(x, y, dur, begin, length=140):
    dx, dy = -460, 230
    return f"""
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.04;0.14;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};{dx} {dy}" keyTimes="0;0.14;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
      <line x1="{x}" y1="{y}" x2="{x + length}" y2="{y - length / 2}" stroke="url(#tail)" stroke-width="2" stroke-linecap="round"/>
      <circle cx="{x}" cy="{y}" r="2.2" fill="#ffffff"/>
    </g>"""


ASTRONAUT = """
  <g>
    <!-- tether -->
    <path d="M -34 10 C -120 40 -150 -40 -230 -10" fill="none" stroke="#7aa2f7" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="4 6">
      <animate attributeName="stroke-dashoffset" values="0;-40" dur="3s" repeatCount="indefinite"/>
    </path>
    <!-- backpack -->
    <rect x="-40" y="-30" width="80" height="72" rx="16" fill="#aeb8d6"/>
    <rect x="-36" y="-22" width="8" height="40" rx="4" fill="#8a93b5"/>
    <!-- legs -->
    <g fill="#e9edf8" stroke="#b8c0dc" stroke-width="1.5">
      <rect x="-27" y="30" width="23" height="50" rx="11">
        <animateTransform attributeName="transform" type="rotate" values="-4 -15 30;6 -15 30;-4 -15 30" dur="5s" repeatCount="indefinite"/>
      </rect>
      <rect x="4" y="30" width="23" height="50" rx="11">
        <animateTransform attributeName="transform" type="rotate" values="8 15 30;-3 15 30;8 15 30" dur="5s" repeatCount="indefinite"/>
      </rect>
    </g>
    <!-- body -->
    <rect x="-35" y="-26" width="70" height="68" rx="26" fill="#f4f6fc" stroke="#b8c0dc" stroke-width="1.5"/>
    <rect x="-17" y="-6" width="34" height="22" rx="6" fill="#1f2547"/>
    <circle cx="-8" cy="5" r="3" fill="#f7768e"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
    <circle cx="0" cy="5" r="3" fill="#9ece6a"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.6s" repeatCount="indefinite"/></circle>
    <circle cx="8" cy="5" r="3" fill="#7dcfff"><animate attributeName="opacity" values="1;0.3;1" dur="0.9s" repeatCount="indefinite"/></circle>
    <!-- resting arm -->
    <g>
      <rect x="-50" y="-16" width="20" height="44" rx="10" fill="#e9edf8" stroke="#b8c0dc" stroke-width="1.5" transform="rotate(18 -40 -12)"/>
      <circle cx="-52" cy="28" r="10" fill="#aeb8d6"/>
    </g>
    <!-- waving arm: upper arm angled out from the shoulder, forearm waves from the elbow -->
    <g transform="translate(30 -12) rotate(50)">
      <g transform="translate(0 -26)">
        <g>
          <animateTransform attributeName="transform" type="rotate" values="-62;-28;-62" dur="1.4s" repeatCount="indefinite"/>
          <rect x="-9" y="-36" width="18" height="40" rx="9" fill="#e9edf8" stroke="#b8c0dc" stroke-width="1.5"/>
          <circle cx="0" cy="-38" r="10.5" fill="#aeb8d6"/>
        </g>
      </g>
      <rect x="-10" y="-34" width="20" height="40" rx="10" fill="#e9edf8" stroke="#b8c0dc" stroke-width="1.5"/>
    </g>
    <!-- helmet -->
    <line x1="14" y1="-86" x2="22" y2="-104" stroke="#b8c0dc" stroke-width="2"/>
    <circle cx="22" cy="-106" r="4" fill="#f7768e"><animate attributeName="opacity" values="1;0.15;1" dur="1s" repeatCount="indefinite"/></circle>
    <circle cx="0" cy="-52" r="38" fill="#f4f6fc" stroke="#b8c0dc" stroke-width="1.5"/>
    <ellipse cx="5" cy="-50" rx="27" ry="23" fill="url(#visor)"/>
    <path d="M -12 -62 Q -4 -70 10 -68" fill="none" stroke="#ffffff" stroke-opacity="0.75" stroke-width="4" stroke-linecap="round"/>
    <circle cx="18" cy="-40" r="2.5" fill="#ffffff" opacity="0.6">
      <animate attributeName="opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite"/>
    </circle>
    <rect x="-44" y="-60" width="8" height="18" rx="4" fill="#aeb8d6"/>
  </g>"""

ROCKET = """
  <g>
    <path d="M -18 -4 L -34 0 L -18 4 Z" fill="#ff9e64">
      <animate attributeName="d" values="M -18 -4 L -34 0 L -18 4 Z;M -18 -5 L -42 0 L -18 5 Z;M -18 -4 L -34 0 L -18 4 Z" dur="0.25s" repeatCount="indefinite"/>
    </path>
    <path d="M -18 -2.5 L -26 0 L -18 2.5 Z" fill="#ffe08a"/>
    <path d="M -18 -7 L -25 -14 L -9 -7 Z" fill="#f7768e"/>
    <path d="M -18 7 L -25 14 L -9 7 Z" fill="#f7768e"/>
    <path d="M -18 -7 L 10 -7 Q 24 0 10 7 L -18 7 Z" fill="#e9edf8"/>
    <circle cx="2" cy="0" r="3.6" fill="#7dcfff" stroke="#1f2547" stroke-width="1.2"/>
  </g>"""


def hero(rng):
    w, h = 1200, 420
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Judikael Bellance - full-stack developer, space themed animated banner">
  <defs>
    <radialGradient id="space" cx="0.3" cy="0.2" r="1.1">
      <stop offset="0" stop-color="#151a33"/>
      <stop offset="0.55" stop-color="#090c1c"/>
      <stop offset="1" stop-color="#03040b"/>
    </radialGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7dcfff"/>
      <stop offset="0.45" stop-color="#bb9af7"/>
      <stop offset="0.75" stop-color="#ff79c6"/>
      <stop offset="1" stop-color="#7dcfff"/>
      <animate attributeName="x1" values="0;-1;0" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="1;0;1" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="tail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#7dcfff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="visor" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2b2f6b"/>
      <stop offset="0.6" stop-color="#5a3d8f"/>
      <stop offset="1" stop-color="#ff79c6"/>
    </linearGradient>
    <radialGradient id="planet" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="#c3a6ff"/>
      <stop offset="0.5" stop-color="#7a5bd6"/>
      <stop offset="1" stop-color="#2a1a5e"/>
    </radialGradient>
    <radialGradient id="moon" cx="0.35" cy="0.35" r="0.8">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#8a93b5"/>
    </radialGradient>
    <radialGradient id="glow">
      <stop offset="0" stop-color="#bb9af7" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#bb9af7" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath>
    <clipPath id="planetClip"><circle cx="1060" cy="300" r="130"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#space)"/>

    <!-- nebulae -->
    <g filter="url(#blur)">
      <ellipse cx="300" cy="120" rx="260" ry="110" fill="#3d59a1" opacity="0.55">
        <animate attributeName="opacity" values="0.55;0.3;0.55" dur="12s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="300;360;300" dur="20s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse cx="760" cy="330" rx="300" ry="100" fill="#7a3d9f" opacity="0.45">
        <animate attributeName="opacity" values="0.45;0.2;0.45" dur="15s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="760;700;760" dur="24s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse cx="1000" cy="80" rx="200" ry="80" fill="#ff79c6" opacity="0.18">
        <animate attributeName="opacity" values="0.18;0.32;0.18" dur="10s" repeatCount="indefinite"/>
      </ellipse>
    </g>

    <!-- star field: distant drift + twinkling foreground -->
    {drifting_layer(rng, 70, w, h, 140, (0.3, 0.8), 0.5)}
    {drifting_layer(rng, 30, w, h, 70, (0.6, 1.2), 0.7)}
    <g>{twinkling_stars(rng, 90, w, h, colors=("#ffffff", "#ffffff", "#c0caf5", "#7dcfff", "#ffd8a8"))}</g>

    <!-- sparkle stars -->
    <g fill="#ffffff">
      <path d="M 640 60 l 3 9 l 9 3 l -9 3 l -3 9 l -3 -9 l -9 -3 l 9 -3 z"><animate attributeName="opacity" values="1;0.2;1" dur="3s" repeatCount="indefinite"/></path>
      <path d="M 90 330 l 2 6 l 6 2 l -6 2 l -2 6 l -2 -6 l -6 -2 l 6 -2 z"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.5s" repeatCount="indefinite"/></path>
      <path d="M 1150 190 l 2 6 l 6 2 l -6 2 l -2 6 l -2 -6 l -6 -2 l 6 -2 z"><animate attributeName="opacity" values="1;0.3;1" dur="4s" repeatCount="indefinite"/></path>
    </g>

    <!-- shooting stars -->
    {shooting_star(900, 40, 9, 1)}
    {shooting_star(1150, 120, 13, 5)}
    {shooting_star(600, 20, 17, 10)}

    <!-- ringed planet: back ring, planet, front ring, moon orbiting on the ring plane -->
    <circle cx="1060" cy="300" r="230" fill="url(#glow)"/>
    <g transform="rotate(-14 1060 300)">
      <ellipse cx="1060" cy="300" rx="230" ry="44" fill="none" stroke="#e0af68" stroke-opacity="0.45" stroke-width="9"/>
    </g>
    <circle cx="1060" cy="300" r="130" fill="url(#planet)"/>
    <g clip-path="url(#planetClip)" opacity="0.35">
      <g>
        <animateTransform attributeName="transform" type="translate" from="0 0" to="-400 0" dur="40s" repeatCount="indefinite"/>
        <path d="M 880 245 q 100 -20 200 0 t 200 0 t 200 0 t 200 0" fill="none" stroke="#2a1a5e" stroke-width="16"/>
        <path d="M 880 288 q 100 18 200 0 t 200 0 t 200 0 t 200 0" fill="none" stroke="#e0c3ff" stroke-width="10"/>
        <path d="M 880 338 q 100 -14 200 0 t 200 0 t 200 0 t 200 0" fill="none" stroke="#2a1a5e" stroke-width="22"/>
      </g>
    </g>
    <g transform="rotate(-14 1060 300)">
      <clipPath id="ringFront"><rect x="780" y="300" width="560" height="80"/></clipPath>
      <ellipse cx="1060" cy="300" rx="230" ry="44" fill="none" stroke="#e0af68" stroke-opacity="0.9" stroke-width="9" clip-path="url(#ringFront)"/>
      <ellipse cx="1060" cy="300" rx="208" ry="38" fill="none" stroke="#ffd8a8" stroke-opacity="0.4" stroke-width="3" clip-path="url(#ringFront)"/>
      <g>
        <animateMotion dur="20s" repeatCount="indefinite" path="M 820 300 a 240 62 0 1 0 480 0 a 240 62 0 1 0 -480 0"/>
        <animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="0;0.62;0.67;0.83;0.88;1" dur="20s" repeatCount="indefinite"/>
        <circle cx="0" cy="0" r="13" fill="url(#moon)"/>
        <circle cx="-4" cy="-3" r="3" fill="#8a93b5" opacity="0.6"/>
      </g>
    </g>

    <!-- floating astronaut -->
    <g transform="translate(800 210)">
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 -16;0 0" dur="6s" repeatCount="indefinite"/>
        <g>
          <animateTransform attributeName="transform" type="rotate" values="-8;8;-8" dur="9s" repeatCount="indefinite"/>
          {ASTRONAUT}
        </g>
      </g>
    </g>

    <!-- title block -->
    <g font-family="{SANS}">
      <g opacity="0">
        <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze"/>
        <text x="70" y="96" font-family="{MONO}" font-size="15" letter-spacing="4" fill="#7dcfff">MISSION CONTROL · FR</text>
      </g>
      <g opacity="0">
        <animate attributeName="opacity" values="0;1" begin="0.2s" dur="1s" fill="freeze"/>
        <animateTransform attributeName="transform" type="translate" values="0 20;0 0" begin="0.2s" dur="1s" fill="freeze"/>
        <text x="66" y="166" font-size="64" font-weight="800" letter-spacing="-1" fill="url(#title)">Judikael Bellance</text>
      </g>
      <g opacity="0">
        <animate attributeName="opacity" values="0;1" begin="0.7s" dur="1s" fill="freeze"/>
        <text x="70" y="210" font-size="22" font-weight="500" fill="#c0caf5">Full-stack developer · Epitech · France</text>
      </g>
    </g>

    <!-- terminal typing line -->
    <clipPath id="typing">
      <rect x="70" y="232" width="0" height="30">
        <animate attributeName="width" values="0;470" begin="1.3s" dur="2.6s" fill="freeze"/>
      </rect>
    </clipPath>
    <text x="70" y="254" font-family="{MONO}" font-size="18" fill="#9ece6a" textLength="466" lengthAdjust="spacingAndGlyphs" clip-path="url(#typing)">&gt; launching: Rust · PHP · React · Next.js · Symfony</text>
    <rect x="72" y="238" width="10" height="20" fill="#9ece6a">
      <animate attributeName="x" values="72;542" begin="1.3s" dur="2.6s" fill="freeze"/>
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>

    <!-- status pills -->
    <g font-family="{SANS}" font-size="14" font-weight="600" opacity="0">
      <animate attributeName="opacity" values="0;1" begin="3.6s" dur="0.8s" fill="freeze"/>
      <g transform="translate(70 290)">
        <rect width="214" height="36" rx="18" fill="#9ece6a" fill-opacity="0.1" stroke="#9ece6a" stroke-opacity="0.45"/>
        <circle cx="20" cy="18" r="5" fill="#9ece6a">
          <animate attributeName="r" values="4;7;4" dur="1.6s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="1;0.35;1" dur="1.6s" repeatCount="indefinite"/>
        </circle>
        <text x="36" y="23" fill="#c0caf5">Open to collaboration</text>
      </g>
      <g transform="translate(298 290)">
        <rect width="190" height="36" rx="18" fill="#7dcfff" fill-opacity="0.1" stroke="#7dcfff" stroke-opacity="0.45"/>
        <text x="18" y="23" fill="#c0caf5">🛰  agency.jud3v.fr</text>
      </g>
    </g>
  </g>
</svg>
"""


def divider(rng):
    w, h = 1200, 48
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="presentation">
  <defs>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#bb9af7" stop-opacity="0"/>
      <stop offset="1" stop-color="#ff9e64" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7aa2f7" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#bb9af7" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#7dcfff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect y="23.5" width="{w}" height="1" fill="url(#line)"/>
  <g>{twinkling_stars(rng, 40, w, h, (0.5, 1.3), ("#c0caf5", "#7dcfff", "#bb9af7"))}</g>
  <g>
    <animateTransform attributeName="transform" type="translate" values="-80 24;1280 24" dur="7s" repeatCount="indefinite"/>
    <rect x="-180" y="-1.5" width="150" height="3" rx="1.5" fill="url(#trail)"/>
    <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0;0 3;0 0" dur="1.2s" repeatCount="indefinite"/>{ROCKET}</g>
  </g>
</svg>
"""


def footer(rng):
    w, h = 1200, 240
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Thanks for visiting - see you among the stars">
  <defs>
    <radialGradient id="sky" cx="0.5" cy="1" r="1">
      <stop offset="0" stop-color="#1b1f3f"/>
      <stop offset="1" stop-color="#03040b"/>
    </radialGradient>
    <radialGradient id="ground" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="#7a5bd6"/>
      <stop offset="1" stop-color="#1a1240"/>
    </radialGradient>
    <linearGradient id="atmo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#bb9af7" stop-opacity="0"/>
      <stop offset="1" stop-color="#bb9af7" stop-opacity="0.55"/>
    </linearGradient>
    <linearGradient id="exhaust" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ff9e64" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#ff9e64" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#sky)"/>
    <g>{twinkling_stars(rng, 80, w, 170)}</g>

    <!-- rocket launch -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="260 230;260 230;330 -60" keyTimes="0;0.35;1" dur="8s" repeatCount="indefinite"/>
      <g transform="rotate(-76)">
        <rect x="-110" y="-2" width="90" height="4" rx="2" fill="url(#exhaust)" transform="rotate(180 -65 0)"/>
        {ROCKET}
      </g>
    </g>

    <!-- planet horizon -->
    <ellipse cx="600" cy="560" rx="900" ry="400" fill="url(#atmo)" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0.5;0.8" dur="6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="600" cy="600" rx="880" ry="420" fill="url(#ground)"/>

    <text x="600" y="110" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="700" fill="#c0caf5">
      Thanks for visiting
      <animate attributeName="opacity" values="0.75;1;0.75" dur="4s" repeatCount="indefinite"/>
    </text>
    <text x="600" y="142" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="#7dcfff">SEE YOU AMONG THE STARS ✦</text>
  </g>
</svg>
"""


def main():
    ASSETS.mkdir(exist_ok=True)
    rng = random.Random(42)
    (ASSETS / "hero.svg").write_text(hero(rng), encoding="utf-8")
    (ASSETS / "divider.svg").write_text(divider(rng), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(footer(rng), encoding="utf-8")


if __name__ == "__main__":
    main()
