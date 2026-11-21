"""Banners for the "Cloudflare" series: smooth, technical illustrations (no anime, at the user's request).

Each post gets one overview.svg (1200x630) that is embedded in the body and rendered to feature.png for cards and
social previews. Shared look: a deep navy gradient, two soft blurred light blobs, a faint dot grid, glass cards with
hairline borders, curved flow lines with a glow, and the post's own numbers.

Run from the repo root:  python tools/covers/cloudflare_series.py [slug ...]
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORANGE, AMBER, CYAN, VIOLET, GREEN, RED = "#f6821f", "#fbbf24", "#22d3ee", "#a78bfa", "#4ade80", "#f87171"
INK, SOFT, DIM = "#f8fafc", "#cbd5e1", "#94a3b8"
FONT = "Segoe UI, system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
MONO = "Consolas, Menlo, monospace"
only = sys.argv[1:]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs():
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060a18"/><stop offset=".55" stop-color="#0d1330"/><stop offset="1" stop-color="#1a1440"/></linearGradient>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#fff" fill-opacity=".06"/></pattern>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity=".5"/></filter>
  <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".10"/><stop offset="1" stop-color="#ffffff" stop-opacity=".03"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="#f43f5e"/></linearGradient>
  <linearGradient id="flow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".28"/><stop offset="1" stop-color="#ffffff" stop-opacity=".06"/></linearGradient>
</defs>"""


def backdrop(blobs):
    out = '<rect width="1200" height="630" fill="url(#bg)"/>'
    for x, y, r, c, o in blobs:
        out += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}" filter="url(#blur)"/>'
    return out + '<rect width="1200" height="630" fill="url(#dots)"/>'


def heading(part, title, sub):
    return (f'<text x="60" y="76" fill="{ORANGE}" font-size="17" font-weight="700" letter-spacing="3.5">CLOUDFLARE · {part}</text>'
            f'<text x="60" y="128" fill="{INK}" font-size="46" font-weight="800">{esc(title)}</text>'
            f'<text x="60" y="166" fill="{SOFT}" font-size="21">{esc(sub)}</text>')


def card(x, y, w, h, stroke="url(#hair)", rx=18, fill="url(#glass)"):
    return (f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#0b1124" fill-opacity=".72"/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')


def t(x, y, s, size=15, fill=INK, weight=400, anchor="start", mono=False, ls=0):
    fam = f' font-family="{MONO}"' if mono else ""
    spacing = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{fam}{spacing}>{esc(s)}</text>'


def pill(x, y, label, color, w=None, size=13):
    w = w or int(len(label) * size * 0.62 + 24)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".7"/>'
            + t(x + w / 2, y + 18, label, size, color, 700, "middle"))


def flowline(d, color="url(#flow)", width=3, dash=None, glow=True):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    g = ' filter="url(#glow)"' if glow else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{da}{g}/>'


def dot(x, y, c, r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r + 5}" fill="{c}" opacity=".18"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def cloud(cx, cy, s, color):
    """A smooth cloud glyph centred at cx, cy (s = scale)."""
    return (f'<path transform="translate({cx},{cy}) scale({s})" d="M-34 14 H34 A16 16 0 0 0 30 -17 A24 24 0 0 0 -12 -22 '
            f'A18 18 0 0 0 -38 -4 A15 15 0 0 0 -34 14 Z" fill="{color}"/>')


def write(slug, alt, body):
    if only and slug not in only:
        return
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" font-family="{FONT}">'
           f'<title>{esc(alt)}</title>{defs()}{body}</svg>\n')
    path = ROOT / "content" / "posts" / slug / "overview.svg"
    path.write_text(svg, encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(ROOT / "tools/titles/svg_to_png.py"), str(path)], check=True)
    print("wrote", path)


# ---------- 1. An introduction ----------
def part1():
    b = backdrop([(860, 360, 190, ORANGE, .30), (230, 560, 170, VIOLET, .28), (1120, 90, 140, CYAN, .18)])
    b += heading(1, "An introduction", "A front desk for your domain: DNS, the proxy and the edge.")
    # visitor
    b += card(60, 250, 200, 150)
    b += f'<rect x="92" y="278" width="136" height="86" rx="10" fill="none" stroke="{CYAN}" stroke-width="2"/>'
    b += f'<circle cx="104" cy="290" r="3" fill="{RED}"/><circle cx="114" cy="290" r="3" fill="{AMBER}"/><circle cx="124" cy="290" r="3" fill="{GREEN}"/>'
    b += t(160, 336, "example.com", 14, SOFT, 600, "middle", mono=True)
    b += t(160, 388, "VISITOR", 13, CYAN, 700, "middle", ls=2.5)
    # edge
    b += f'<circle cx="600" cy="330" r="118" fill="{ORANGE}" opacity=".10"/>'
    b += f'<circle cx="600" cy="330" r="92" fill="#0b1124" stroke="url(#edge)" stroke-width="3" filter="url(#glow)"/>'
    b += cloud(600, 300, 1.25, ORANGE)
    b += t(600, 356, "EDGE", 16, INK, 800, "middle", ls=4)
    b += t(600, 380, "348 cities", 14, AMBER, 600, "middle")
    for i, (lab, col) in enumerate([("DNS", CYAN), ("TLS", GREEN), ("Cache", AMBER), ("Rules", VIOLET), ("WAF", RED)]):
        x = 410 + i * 80
        b += pill(x, 470, lab, col, w=68)
    # origin
    b += card(940, 250, 200, 150)
    for i in range(3):
        b += f'<rect x="985" y="{276 + i * 26}" width="110" height="18" rx="5" fill="none" stroke="{VIOLET}" stroke-width="1.8"/><circle cx="1083" cy="{285 + i * 26}" r="3" fill="{GREEN}"/>'
    b += t(1040, 388, "ORIGIN", 13, VIOLET, 700, "middle", ls=2.5)
    # proxied path
    b += flowline("M262 318 C350 318 420 318 506 318")
    b += flowline("M694 318 C780 318 850 318 938 318")
    b += t(384, 300, "orange cloud: proxied", 14, ORANGE, 700, "middle")
    b += t(816, 300, "only Cloudflare knocks", 14, SOFT, 400, "middle")
    # dns only path
    b += flowline("M160 402 C160 560 1040 560 1040 402", "#64748b", 2, "6 8", glow=False)
    b += f'<rect x="510" y="532" width="180" height="28" rx="14" fill="#0b1124"/>'
    b += t(600, 551, "grey cloud: DNS only", 14, DIM, 700, "middle")
    b += t(60, 604, "95% of internet users within 50 ms of the edge", 14, DIM)
    write("cloudflare-1-an-introduction",
          "A visitor reaches the origin two ways. Orange cloud, proxied: through the Cloudflare edge, present in 348 cities, "
          "which answers DNS and handles TLS, cache, rules and the WAF. Grey cloud, DNS only: straight to the origin.", b)


# ---------- 2. Securing my two sites ----------
def part2():
    b = backdrop([(320, 420, 200, ORANGE, .24), (960, 420, 200, VIOLET, .26), (1100, 80, 120, CYAN, .16)])
    b += heading(2, "How it secured my two sites", "samarthya.me and bhanuni.in: what each record and rule is for.")
    # samarthya.me card
    b += card(60, 210, 520, 360)
    b += t(88, 248, "samarthya.me", 22, INK, 800)
    b += pill(420, 228, "63 → 11 records", AMBER, w=136)
    rows = [("@", "DNS only", "GitHub Pages", "the blog", DIM),
            ("www", "proxied", "301 → apex", "at the edge", ORANGE),
            ("blog", "proxied", "192.0.2.1", "301, old links", ORANGE),
            ("about", "proxied", "Full (strict)", "TLS checked twice", ORANGE),
            ("mail", "DNS only", "mail host", "MX on its own name", DIM)]
    for i, (n, mode, to, job, col) in enumerate(rows):
        y = 290 + i * 54
        b += f'<rect x="84" y="{y - 22}" width="472" height="42" rx="11" fill="#ffffff" fill-opacity=".035"/>'
        b += cloud(112, y - 2, .42, col)
        b += t(138, y + 4, n, 15, INK, 700, mono=True)
        b += t(214, y + 4, mode, 13, col, 700)
        b += t(306, y + 4, to, 14, SOFT, 400, mono=True)
        b += t(540, y + 4, job, 13, DIM, 400, "end")
    # bhanuni.in card
    b += card(620, 210, 520, 360)
    b += t(648, 248, "bhanuni.in", 22, INK, 800)
    b += pill(1012, 228, "no server", GREEN, w=104)
    b += f'<rect x="648" y="272" width="464" height="112" rx="14" fill="#ffffff" fill-opacity=".035"/>'
    b += cloud(690, 312, .55, ORANGE)
    b += t(726, 306, "@  www  →  192.0.2.1", 15, INK, 700, mono=True)
    b += t(726, 330, "proxied placeholder, nothing listens", 13, DIM)
    b += flowline("M690 352 C760 372 860 372 930 352", ORANGE, 2.4)
    b += t(946, 358, "302 → gallery", 14, AMBER, 700)
    b += t(648, 422, "Mail it can never send", 15, INK, 700)
    for i, (rec, col) in enumerate([("v=spf1 -all", GREEN), ("DMARC p=reject", GREEN), ("Always Use HTTPS", CYAN)]):
        b += f'<rect x="648" y="{440 + i * 40}" width="464" height="32" rx="9" fill="#ffffff" fill-opacity=".035"/>'
        b += dot(668, 456 + i * 40, col, 4)
        b += t(686, 461 + i * 40, rec, 14, SOFT, 400, mono=True)
    write("cloudflare-2-securing-my-sites",
          "Two cards. samarthya.me: 63 old DNS records cut to 11; the blog DNS-only to GitHub Pages; www and the old blog "
          "name proxied and redirected with a 301 at the edge (blog via the placeholder 192.0.2.1); about proxied with Full "
          "(strict) TLS; mail DNS-only on its own name. bhanuni.in: no server, both names proxied to 192.0.2.1 and sent to "
          "the gallery with a 302, SPF -all and DMARC p=reject because it sends no mail, and Always Use HTTPS.", b)


# ---------- 3. The free tier ----------
def part3():
    b = backdrop([(300, 460, 210, CYAN, .18), (900, 430, 220, ORANGE, .26), (1110, 90, 120, VIOLET, .2)])
    b += heading(3, "The free tier, and what to do with it", "What $0 a month buys, and the settings worth a Saturday.")
    tiles = [("∞", "DDoS protection", "unmetered, L3–L7", ORANGE),
             ("1", "Managed ruleset", "widely exploited CVEs", RED),
             ("5", "WAF custom rules", "block, challenge, skip", VIOLET),
             ("1", "Rate-limit rule", "per IP, 10 s window", AMBER),
             ("10", "Redirect rules", "single redirects", CYAN),
             ("10", "Cache rules", "HTML too, if you say so", GREEN),
             ("✓", "Universal SSL", "apex + one level", GREEN),
             ("50", "Zero Trust users", "Access, Tunnel, Gateway", CYAN)]
    for i, (big, name, note, col) in enumerate(tiles):
        x, y = 60 + (i % 4) * 274, 210 + (i // 4) * 170
        b += card(x, y, 250, 148)
        b += f'<circle cx="{x + 52}" cy="{y + 56}" r="30" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6"/>'
        b += t(x + 52, y + 67, big, 28 if len(big) < 2 else 24, col, 800, "middle")
        b += t(x + 96, y + 62, name, 15, INK, 700)
        b += t(x + 24, y + 116, note, 14, SOFT)
    b += t(60, 604, "Free plan limits as documented by Cloudflare, November 2026", 14, DIM)
    write("cloudflare-3-free-tier-checklist",
          "Eight tiles for the Cloudflare free plan: unmetered DDoS protection, the free managed WAF ruleset (one ruleset), 5 WAF custom "
          "rules, 1 rate-limiting rule per IP over 10 seconds, 10 redirect rules, 10 cache rules, Universal SSL for the apex "
          "and one level of subdomains, and Zero Trust for up to 50 users.", b)


# ---------- 4. Zero trust ----------
def part4():
    b = backdrop([(250, 420, 190, RED, .16), (840, 400, 230, CYAN, .22), (1080, 110, 130, ORANGE, .2)])
    b += heading(4, "An introduction to zero trust", "Stop trusting the network. Check the person, every request.")
    # castle and moat
    b += card(60, 210, 360, 360)
    b += t(240, 246, "CASTLE AND MOAT", 13, RED, 700, "middle", ls=2.5)
    b += f'<circle cx="240" cy="380" r="104" fill="none" stroke="#38bdf8" stroke-opacity=".5" stroke-width="10"/>'
    b += f'<circle cx="240" cy="380" r="72" fill="{RED}" fill-opacity=".08" stroke="{RED}" stroke-opacity=".5" stroke-dasharray="4 6"/>'
    for (x, y) in [(214, 360), (262, 356), (236, 404)]:
        b += f'<rect x="{x - 14}" y="{y - 10}" width="28" height="20" rx="5" fill="none" stroke="{SOFT}" stroke-width="1.6"/>'
    b += t(240, 520, "inside = trusted", 15, INK, 700, "middle")
    b += t(240, 544, "one stolen VPN login reaches all", 13, DIM, 400, "middle")
    # zero trust flow
    b += card(450, 210, 690, 360)
    b += t(795, 246, "ZERO TRUST WITH CLOUDFLARE ONE", 13, CYAN, 700, "middle", ls=2.5)
    nodes = [(530, "person", "you@example.com", CYAN), (720, "Access", "policy + OTP", ORANGE),
             (910, "Tunnel", "outbound only", VIOLET), (1070, "app", "no open port", GREEN)]
    for i, (x, name, sub, col) in enumerate(nodes):
        b += f'<circle cx="{x}" cy="350" r="44" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-width="2" filter="url(#glow)"/>'
        b += t(x, 356, name, 16, INK, 800, "middle")
        b += t(x, 424, sub, 13, SOFT, 400, "middle")
        if i < 3:
            nx = nodes[i + 1][0]
            bend = 20 if nx - x > 170 else 8
            b += flowline(f"M{x + 48} 350 C{x + 80} {350 - bend} {nx - 80} {350 - bend} {nx - 48} 350", col, 2.6)
    b += f'<rect x="478" y="460" width="634" height="84" rx="14" fill="#ffffff" fill-opacity=".035"/>'
    b += t(500, 492, "Include: emails ending @example.com", 14, SOFT, 400, mono=True)
    b += t(500, 520, "deny by default · PIN expires in 10 min", 14, DIM, 400, mono=True)
    b += pill(980, 476, "free: 50 users", GREEN, w=116)
    write("cloudflare-4-zero-trust",
          "Left, castle and moat: a moat around a network where everything inside is trusted, so one stolen VPN login "
          "reaches everything. Right, zero trust with Cloudflare One: a person passes Access (a policy and a one-time PIN "
          "that expires in 10 minutes), then a Tunnel that only connects outwards, to an app with no open port. Access "
          "denies by default; the free plan covers 50 users.", b)


part1()
part2()
part3()
part4()
