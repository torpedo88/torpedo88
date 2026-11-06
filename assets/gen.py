"""Generate the animated SVGs used by README.md. Run: python3 assets/gen.py"""
import html
import pathlib
import textwrap

OUT = pathlib.Path(__file__).parent
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace"
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def esc(s):
    return html.escape(s, quote=True)


def rrect_path(x, y, w, h, r):
    return (f"M{x+r},{y} H{x+w-r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} "
            f"A{r},{r} 0 0 1 {x+w-r},{y+h} H{x+r} A{r},{r} 0 0 1 {x},{y+h-r} "
            f"V{y+r} A{r},{r} 0 0 1 {x+r},{y} Z")


def beam(path, color, dur, delay=0):
    # "border beam": a short bright dash travelling around the card edge
    return f'''<path d="{path}" pathLength="100" fill="none" stroke="url(#beam)" stroke-width="2"
    stroke-linecap="round" stroke-dasharray="14 86" style="animation:run {dur}s linear {delay}s infinite"/>'''


def hero():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-label="Abhishek Maharjan. Engineering leader, founder, DevOps at Paramount.">
<defs>
  <linearGradient id="name" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
    <stop offset="0" stop-color="#F8FAFC"/><stop offset=".45" stop-color="#C4B5FD"/><stop offset=".7" stop-color="#67E8F9"/><stop offset="1" stop-color="#F8FAFC"/>
    <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1200 0" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
  <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" stroke="#FFFFFF" stroke-opacity=".06"/></pattern>
  <radialGradient id="fade" cx=".5" cy=".45" r=".65"><stop offset=".2" stop-color="#FFF"/><stop offset="1" stop-color="#000"/></radialGradient>
  <mask id="m"><rect width="1200" height="360" fill="url(#fade)"/></mask>
  <clipPath id="clip"><rect width="1200" height="360" rx="28"/></clipPath>
  <linearGradient id="beam"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#A855F7"/></linearGradient>
</defs>
<style>
  .b1{{animation:d1 16s ease-in-out infinite alternate}}
  .b2{{animation:d2 19s ease-in-out infinite alternate}}
  .b3{{animation:d3 13s ease-in-out infinite alternate}}
  @keyframes d1{{to{{transform:translate(220px,60px)}}}}
  @keyframes d2{{to{{transform:translate(-260px,-50px)}}}}
  @keyframes d3{{to{{transform:translate(120px,90px)}}}}
  @keyframes run{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}
  {REDUCED}
</style>
<g clip-path="url(#clip)">
  <rect width="1200" height="360" fill="#08080E"/>
  <g filter="url(#blur)" opacity=".6">
    <circle class="b1" cx="220" cy="70" r="170" fill="#7C3AED"/>
    <circle class="b2" cx="960" cy="300" r="180" fill="#0891B2"/>
    <circle class="b3" cx="640" cy="20" r="120" fill="#C026D3"/>
  </g>
  <rect width="1200" height="360" fill="url(#grid)" mask="url(#m)"/>

  <text x="600" y="176" text-anchor="middle" font-family="{SANS}" font-size="76" font-weight="800" letter-spacing="-2" fill="url(#name)">Abhishek Maharjan</text>
  <text x="600" y="232" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="500" fill="#CBD5E1">Engineering Leader  ·  Founder  ·  DevOps at Paramount</text>
  <text x="600" y="280" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#94A3B8" letter-spacing="1">AI-POWERED CI/CD  ·  MCP SERVERS  ·  SDLC DESIGN  ·  MENTORING</text>
</g>
<rect x=".5" y=".5" width="1199" height="359" rx="28" fill="none" stroke="#FFFFFF" stroke-opacity=".1"/>
{beam(rrect_path(1, 1, 1198, 358, 28), "", 8)}
</svg>'''
    (OUT / "hero.svg").write_text(svg)


CARDS = [
    ("restaurant", "#A855F7", "MULTI-TENANT SAAS · LIVE", "Restaurant ordering platform",
     "Branded storefront, online ordering, Stripe payments, Uber Direct delivery and kitchen printing for independent restaurants.",
     "trisarasf.com  ·  annapurnaoakland.com"),
    ("tixfix", "#22D3EE", "TICKETING PLATFORM", "TixFix",
     "Ticketing for community promoters plus one-command hosting on *.tixfix.ai. Powered Hamro Mela, a street fair in NYC.",
     "tixfix.ai"),
    ("durbar", "#E879F9", "EVENTS · LIVE", "Durbar Events",
     "Presale signups and a day-of box office for Bay Area Nepali concerts.",
     "durbarevents.com"),
    ("newah", "#FBBF24", "NONPROFIT · LIVE", "Newah Organization",
     "Donations and festival tickets for the NorCal chapter of the Newah Organization of America.",
     "noancc.org"),
    ("cravlr", "#34D399", "CONSUMER APP", "Cravlr",
     "Local restaurant recommendations. I run the CI, security reviews and production monitoring.",
     "in development"),
    ("jarvis", "#FB7185", "LOCAL AI · HOMELAB", "Jarvis",
     "A headless GPU server at home that runs local models through Ollama, so private data stays on my hardware.",
     "private build"),
]


def card(i, slug, accent, tag, title, desc, foot):
    W, H = 600, 230
    lines = textwrap.wrap(desc, 54)[:3]
    desc_svg = "".join(
        f'<text x="32" y="{124 + n*26}" font-family="{SANS}" font-size="18" fill="#94A3B8">{esc(l)}</text>'
        for n, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}: {esc(desc)}">
<defs>
  <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".45"/><stop offset=".6" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <linearGradient id="beam"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset="1" stop-color="{accent}"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".16"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".04"/></linearGradient>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<style>
  .g{{animation:breathe 5s ease-in-out {i*0.7:.1f}s infinite}}
  @keyframes breathe{{50%{{opacity:.45}}}}
  @keyframes run{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}
  {REDUCED}
</style>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="#0C0C14"/>
  <rect class="g" width="{W}" height="{H}" fill="url(#glow)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="url(#edge)"/>
{beam(rrect_path(1, 1, W-2, H-2, 22), accent, 6 + i % 3, i * 0.9)}
<circle cx="38" cy="38" r="5" fill="{accent}"/>
<text x="52" y="43" font-family="{MONO}" font-size="13" fill="{accent}" letter-spacing="1.2">{esc(tag)}</text>
<text x="32" y="88" font-family="{SANS}" font-size="32" font-weight="700" fill="#F8FAFC" letter-spacing="-.5">{esc(title)}</text>
{desc_svg}
<text x="32" y="{H-24}" font-family="{MONO}" font-size="13" fill="#64748B">→ {esc(foot)}</text>
</svg>'''
    (OUT / f"card-{slug}.svg").write_text(svg)


PRINCIPLES = [
    ("Rules live in CI", "Every standard has an owner and a check that fails the build when it is broken."),
    ("Same rules for agents", "AI agents pass the same tests and reviews as people, so quality never waits on me."),
    ("Mentoring", "I review my mentees' PRs for security and correctness, next to an AI reviewer."),
    ("Plans get reviewed first", "Agents pick apart a plan before anyone writes code. Weak plans get thrown out."),
    ("Spend carefully", "Serverless before custom infrastructure, hands-on onboarding before self-serve."),
    ("Secure by default", "Row-level security on every tenant table and no secrets in the browser."),
]
ACCENTS = ["#A855F7", "#22D3EE", "#E879F9", "#FBBF24", "#34D399", "#FB7185"]


def principles():
    W, H, tw, th, gap = 1200, 460, 384, 214, 24
    tiles = []
    for n, ((title, body), accent) in enumerate(zip(PRINCIPLES, ACCENTS)):
        x, y = (n % 3) * (tw + gap), (n // 3) * (th + gap) + 4
        lines = "".join(
            f'<text x="{x+28}" y="{y+116+k*24}" font-family="{SANS}" font-size="17" fill="#94A3B8">{esc(l)}</text>'
            for k, l in enumerate(textwrap.wrap(body, 38)[:3]))
        tiles.append(f'''<rect x="{x+.5}" y="{y+.5}" width="{tw-1}" height="{th-1}" rx="20" fill="#0C0C14" stroke="#FFFFFF" stroke-opacity=".09"/>
<rect class="t" style="animation-delay:{n*0.6:.1f}s" x="{x+28}" y="{y+28}" width="44" height="3" rx="1.5" fill="{accent}"/>
<text x="{x+28}" y="{y+80}" font-family="{SANS}" font-size="23" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
{lines}''')
    alt = " ".join(f"{t}: {b}" for t, b in PRINCIPLES)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<style>
  .t{{transform-box:fill-box;transform-origin:left;animation:grow 3.6s ease-in-out infinite}}
  @keyframes grow{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(2.6)}}}}
  {REDUCED}
</style>
{"".join(tiles)}
</svg>'''
    (OUT / "principles.svg").write_text(svg)


# Simple Icons (CC0) paths in assets/icons/. Codex and Bedrock AgentCore have no
# own mark, so they reuse the parent brand and rely on the label.
AI_STACK = [
    ("claude", "#D97757", "Claude Code"),
    ("modelcontextprotocol", "#F8FAFC", "MCP"),
    ("anthropic", "#F0EEE6", "Anthropic API"),
    ("openai", "#F8FAFC", "OpenAI"),
    ("openai", "#10A37F", "Codex"),
    ("googlegemini", "#8E75B2", "Gemini"),
    ("ollama", "#F8FAFC", "Ollama"),
    ("amazonwebservices", "#FF9900", "Bedrock AgentCore"),
]


def ai_stack():
    import re
    tile, gap, label_h = 96, 22, 36
    pad = 34  # room for labels wider than a tile
    W = len(AI_STACK) * tile + (len(AI_STACK) - 1) * gap + 2 * pad
    H = tile + label_h
    parts = []
    for n, (icon, color, label) in enumerate(AI_STACK):
        d = re.search(r' d="([^"]+)"', (OUT / "icons" / f"{icon}.svg").read_text()).group(1)
        x = pad + n * (tile + gap)
        parts.append(f'''<g transform="translate({x},0)"><title>{esc(label)}</title>
<rect width="{tile}" height="{tile}" rx="22" fill="#242938"/>
<path transform="translate(24,24) scale(2)" fill="{color}" d="{d}"/>
<text x="{tile/2}" y="{tile+26}" text-anchor="middle" font-family="{SANS}" font-size="17" fill="#94A3B8">{esc(label)}</text></g>''')
    alt = ", ".join(l for _, _, l in AI_STACK)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
{"".join(parts)}
</svg>'''
    (OUT / "ai-stack.svg").write_text(svg)


JOURNEY = [
    ("QA", "Quality engineering", "#22D3EE"),
    ("Release Eng", "Developer, build and release", "#34D399"),
    ("DevOps", "CI/CD and platform", "#A855F7"),
    ("Architecture", "Systems and SDLC design", "#E879F9"),
    ("Leadership", "Teams, mentoring, founder", "#FBBF24"),
]


def journey():
    W, H, x0, x1, y = 1200, 170, 120, 1080, 52
    step = (x1 - x0) / (len(JOURNEY) - 1)
    nodes = []
    for n, (title, sub, accent) in enumerate(JOURNEY):
        x = x0 + n * step
        nodes.append(f'''<circle class="ring" style="animation-delay:{n*0.5:.1f}s" cx="{x:.0f}" cy="{y}" r="14" fill="none" stroke="{accent}"/>
<circle cx="{x:.0f}" cy="{y}" r="9" fill="{accent}"/>
<text x="{x:.0f}" y="{y+56}" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
<text x="{x:.0f}" y="{y+84}" text-anchor="middle" font-family="{SANS}" font-size="16" fill="#94A3B8">{esc(sub)}</text>''')
    alt = "Career path: " + " → ".join(f"{t} ({s})" for t, s, _ in JOURNEY)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<defs><linearGradient id="line" x1="{x0}" x2="{x1}" gradientUnits="userSpaceOnUse">
{"".join(f'<stop offset="{n/(len(JOURNEY)-1):.2f}" stop-color="{a}"/>' for n, (_, _, a) in enumerate(JOURNEY))}
</linearGradient></defs>
<style>
  .flow{{animation:flow 1.6s linear infinite}}
  @keyframes flow{{to{{stroke-dashoffset:-24}}}}
  .ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}}
  @keyframes ring{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(2.2);opacity:0}}}}
  {REDUCED}
</style>
<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#line)" stroke-opacity=".25" stroke-width="4"/>
<line class="flow" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#line)" stroke-width="2" stroke-dasharray="12 12"/>
{"".join(nodes)}
</svg>'''
    (OUT / "journey.svg").write_text(svg)


if __name__ == "__main__":
    hero()
    journey()
    ai_stack()
    for i, c in enumerate(CARDS):
        card(i, *c)
    principles()
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
