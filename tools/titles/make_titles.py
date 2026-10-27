"""Draw replacement title images for recovered posts whose originals were lost.

Each image is drawn from the post's own content (a timeline, a sequence, a comparison...) in the colours of the
post's topic (data/covers.yaml), and written to tools/wp2hugo/media/<slug>/<name>.png, where the importer and
tools/wayback/recover.py pick it up. overrides.yaml swaps the post's "image unavailable" placeholder (or lost
thumbnail) for the image, with a caption saying it was recreated.

    tools\\.venv\\Scripts\\python.exe -I tools\\titles\\make_titles.py            # all
    tools\\.venv\\Scripts\\python.exe -I tools\\titles\\make_titles.py x509-history
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "tools" / "wp2hugo" / "media"
W, H = 1200, 630  # the usual social-card size; reads well as a title image
FONTS = Path("C:/Windows/Fonts")
INK, MUTED, PAPER, LINE, SOFT = (31, 41, 55), (75, 85, 99), (255, 255, 255), (229, 231, 235), (248, 250, 252)
TOPIC = {  # from / to colours of data/covers.yaml
    "security": ("#ef4444", "#7f1d1d"),
    "python": ("#eab308", "#713f12"),
    "linux": ("#22c55e", "#14532d"),
    "docker": ("#0ea5e9", "#0c4a6e"),
    "web": ("#10b981", "#064e3b"),
    "devops": ("#6366f1", "#312e81"),
}


def font(size, bold=False, mono=False):
    name = "consolab.ttf" if mono and bold else "consola.ttf" if mono else "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / name), size)


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def tint(c, k):
    """Mix colour c with white: k=0 -> c, k=1 -> white."""
    return tuple(round(v + (255 - v) * k) for v in c)


def canvas(topic, kicker, title):
    """White card with a topic-coloured band on top holding the kicker and the title."""
    a, b = (rgb(c) for c in TOPIC[topic])
    im = Image.new("RGB", (W, H), PAPER)
    band = Image.new("RGB", (W, 150))
    px = band.load()
    for x in range(W):
        t = x / (W - 1)
        c = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
        for y in range(150):
            px[x, y] = c
    im.paste(band, (0, 0))
    d = ImageDraw.Draw(im)
    d.text((56, 30), kicker.upper(), font=font(22, True), fill=PAPER)
    d.text((56, 62), title, font=font(52, True), fill=PAPER)
    return im, d, a, b


def footer(d, text):
    d.line([(56, H - 64), (W - 56, H - 64)], fill=LINE, width=2)
    d.text((56, H - 50), text, font=font(22), fill=MUTED)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def centred(d, x, y, text, f, fill, width=None):
    """Draw text centred on x (wrapped to width if given); return the y below it."""
    for line in wrap(d, text, f, width) if width else [text]:
        d.text((x - d.textlength(line, font=f) / 2, y), line, font=f, fill=fill)
        y += f.size + 8
    return y


def arrow(d, p, q, colour, width=4, head=12):
    d.line([p, q], fill=colour, width=width)
    (x0, y0), (x1, y1) = p, q
    if abs(x1 - x0) >= abs(y1 - y0):
        s = 1 if x1 > x0 else -1
        d.polygon([(x1, y1), (x1 - s * head, y1 - head * 0.7), (x1 - s * head, y1 + head * 0.7)], fill=colour)
    else:
        s = 1 if y1 > y0 else -1
        d.polygon([(x1, y1), (x1 - head * 0.7, y1 - s * head), (x1 + head * 0.7, y1 - s * head)], fill=colour)


def box(d, xy, fill, outline, radius=16, width=3):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- layouts

def steps(topic, kicker, title, items, note, mono_first=False):
    """A row of numbered boxes joined by arrows; items are (heading, detail)."""
    im, d, a, b = canvas(topic, kicker, title)
    n, gap, top, bottom = len(items), 34, 236, 470
    bw = (W - 112 - gap * (n - 1)) / n
    fh = font(26 if n <= 4 else 23, True, mono_first)
    fd = font(21 if n <= 4 else 19)
    for i, (head, detail) in enumerate(items):
        x0 = 56 + i * (bw + gap)
        box(d, [x0, top, x0 + bw, bottom], tint(a, 0.9), tint(a, 0.45))
        d.ellipse([x0 + bw / 2 - 22, top - 22, x0 + bw / 2 + 22, top + 22], fill=b)
        centred(d, x0 + bw / 2, top - 15, str(i + 1), font(24, True), PAPER)
        y = centred(d, x0 + bw / 2, top + 44, head, fh, INK, bw - 28)
        centred(d, x0 + bw / 2, y + 10, detail, fd, MUTED, bw - 30)
        if i < n - 1:
            arrow(d, (x0 + bw + 4, (top + bottom) / 2), (x0 + bw + gap - 4, (top + bottom) / 2), b, 4, 10)
    footer(d, note)
    return im


def compare(topic, kicker, title, left, right, rows, note):
    """Two columns; rows are (label, left text, right text)."""
    im, d, a, b = canvas(topic, kicker, title)
    lx, rx, top = 56, W / 2 + 12, 180
    cw = W / 2 - 68
    for x, name, colour in ((lx, left, b), (rx, right, a)):
        box(d, [x, top, x + cw, top + 62], colour, colour, 14, 1)
        centred(d, x + cw / 2, top + 12, name, font(30, True), PAPER)
    y = top + 82
    fl, ft = font(18, True), font(21)
    row_h = (H - 90 - y) / len(rows)
    for label, l_text, r_text in rows:
        for x, text in ((lx, l_text), (rx, r_text)):
            box(d, [x, y, x + cw, y + row_h - 12], SOFT, LINE, 12, 2)
            d.text((x + 18, y + 10), label.upper(), font=fl, fill=b)
            for j, line in enumerate(wrap(d, text, ft, cw - 36)[:2]):
                d.text((x + 18, y + 36 + j * 27), line, font=ft, fill=INK)
        y += row_h
    if note:
        footer(d, note)
    return im


def cards(topic, kicker, title, items, note, cols=None):
    """A grid of small cards; items are (heading, detail)."""
    im, d, a, b = canvas(topic, kicker, title)
    n = len(items)
    cols = cols or (3 if n in (3, 5, 6, 9) else 4 if n in (4, 7, 8) else 3)
    rows = -(-n // cols)
    gap, top, bottom = 22, 182, H - 84
    cw = (W - 112 - gap * (cols - 1)) / cols
    ch = (bottom - top - gap * (rows - 1)) / rows
    fh, fd = font(23 if cols >= 4 else 25, True), font(19 if cols >= 4 else 20)
    for i, (head, detail) in enumerate(items):
        r, c = divmod(i, cols)
        if r == rows - 1 and n % cols:  # centre a short last row
            c += (cols - n % cols) / 2
        x0, y0 = 56 + c * (cw + gap), top + r * (ch + gap)
        box(d, [x0, y0, x0 + cw, y0 + ch], tint(a, 0.92), tint(a, 0.5), 14, 2)
        d.rectangle([x0 + 2, y0 + 14, x0 + 8, y0 + ch - 14], fill=b)
        d.text((x0 + 24, y0 + 14), head, font=fh, fill=INK)
        for j, line in enumerate(wrap(d, detail, fd, cw - 44)[:3]):
            d.text((x0 + 24, y0 + 14 + fh.size + 12 + j * (fd.size + 6)), line, font=fd, fill=MUTED)
    footer(d, note)
    return im


def nested(topic, kicker, title, layers, note, side=None):
    """Boxes inside boxes, outermost first; layers are (label, detail). side: optional (title, lines) panel."""
    im, d, a, b = canvas(topic, kicker, title)
    x0, y0, x1, y1 = 56, 180, (760 if side else W - 56), H - 84
    for i, (label, detail) in enumerate(layers):
        k = 0.92 - i * 0.16
        box(d, [x0, y0, x1, y1], tint(a, max(k, 0.25)), tint(b, 0.3 + i * 0.1), 18, 3)
        dark = k < 0.5
        d.text((x0 + 22, y0 + 12), label, font=font(26, True), fill=PAPER if dark else INK)
        d.text((x0 + 22 + d.textlength(label, font=font(26, True)) + 14, y0 + 17), detail, font=font(20),
               fill=PAPER if dark else MUTED)
        x0, y0, x1, y1 = x0 + 34, y0 + 62, x1 - 34, y1 - 22
    if side:
        heading, lines = side
        sx = 800
        d.text((sx, 190), heading, font=font(26, True), fill=b)
        for j, line in enumerate(lines):
            d.text((sx, 236 + j * 40), line, font=font(22, mono=True), fill=INK)
    footer(d, note)
    return im


# ---------------------------------------------------------------- the images

def x509_history():
    im, d, a, b = canvas("security", "Security · x509", "X.509: a short history")
    events = [  # (year, heading, detail) — all from the post
        ("late 1970s", "PKI is born", "public-key cryptography (RSA)"),
        ("1988", "X.509 v1", "ITU and ISO define the certificate format"),
        ("1993", "X.509 v2", "subject and issuer unique IDs"),
        ("1996", "X.509 v3", "extensions, including SAN"),
        ("today", "Everywhere", "SSL/TLS, code signing, email, IoT"),
    ]
    y_axis, x0, x1 = 320, 130, W - 130
    d.line([(x0, y_axis), (x1, y_axis)], fill=b, width=6)
    step = (x1 - x0) / (len(events) - 1)
    fy, fh, fd = font(30, True), font(26, True), font(21)
    for i, (year, head, detail) in enumerate(events):  # year above the line, what happened below it
        x = x0 + i * step
        d.ellipse([x - 16, y_axis - 16, x + 16, y_axis + 16], fill=a, outline=PAPER, width=4)
        d.text((x - d.textlength(year, font=fy) / 2, y_axis - 66), year, font=fy, fill=b)
        d.text((x - d.textlength(head, font=fh) / 2, y_axis + 36), head, font=fh, fill=INK)
        for j, line in enumerate(wrap(d, detail, fd, 210)):
            d.text((x - d.textlength(line, font=fd) / 2, y_axis + 74 + j * 28), line, font=fd, fill=MUTED)
    footer(d, "v1 → v2 → v3: each version kept the format and added what the internet needed next")
    return im


def tls_handshake():
    im, d, a, b = canvas("security", "Security · TLS", "The SSL/TLS handshake")
    cx, sx, top = 250, W - 250, 190
    for x, name in ((cx, "Client"), (sx, "Server")):
        box(d, [x - 110, top, x + 110, top + 50], b, b, 12, 1)
        centred(d, x, top + 9, name, font(26, True), PAPER)
        d.line([(x, top + 50), (x, H - 30)], fill=LINE, width=4)
    msgs = [("Client Hello", 1), ("Server Hello", -1), ("Certificate", -1), ("Server Key Exchange (optional)", -1),
            ("Certificate Request (optional)", -1), ("Client Key Exchange", 1), ("Certificate Verify (if asked)", 1),
            ("Finished", 1), ("Finished", -1)]
    y, f = top + 86, font(19, True)
    for label, direction in msgs:
        p, q = ((cx + 6, y), (sx - 6, y)) if direction > 0 else ((sx - 6, y), (cx + 6, y))
        colour = b if direction > 0 else a
        arrow(d, p, q, colour, 3, 11)
        tw = d.textlength(label, font=f)
        d.rectangle([W / 2 - tw / 2 - 8, y - 25, W / 2 + tw / 2 + 8, y - 4], fill=PAPER)
        centred(d, W / 2, y - 26, label, f, INK)
        y += 37
    return im


def ssl_tls():
    return steps("security", "Security · SSL/TLS", "How SSL/TLS protects a connection", [
        ("Handshake", "client and server agree on version and ciphers"),
        ("Authentication", "certificates prove who is who"),
        ("Key exchange", "agree a shared symmetric key"),
        ("Encryption", "data travels encrypted with that key"),
        ("Integrity", "a MAC shows nothing was changed"),
    ], "Asymmetric keys to start, a fast symmetric key for the data")


def keystore_truststore(title, note):
    def draw():
        return compare("security", "Security · Java keystores", title, "Keystore", "Truststore", [
            ("Holds", "your private key and your own certificate", "certificates of CAs and peers you trust"),
            ("Answers", "\"who am I?\": presents an identity", "\"do I trust you?\": verifies others"),
            ("Used by", "servers, and clients doing mutual TLS", "browsers, clients, Kafka brokers checking peers"),
            ("Protect", "password, and keep it private", "password; contents are public certificates"),
        ], note)
    return draw


def python_vs_bash():
    return compare("python", "Python", "Python vs Bash", "Python", "Bash", [
        ("Kind", "general-purpose, high-level language", "Unix shell scripting language"),
        ("Best for", "web, data analysis, ML, larger programs", "system admin: files, processes, glue"),
        ("Libraries", "a huge ecosystem of packages", "the commands already on the system"),
        ("Choose when", "logic grows, data structures, tests", "a few commands in a row, quick automation"),
    ], "Both have their place: pick by the task, not by habit")


def python_when_not():
    return cards("python", "Python", "When not to use Python", [
        ("Performance-critical", "interpreted, slower than C or C++"),
        ("Mobile apps", "Java for Android, Swift for iOS"),
        ("Low-level systems", "drivers and operating systems: C or Assembly"),
        ("Strict real-time", "embedded systems: C or C++"),
        ("Tiny one-off scripts", "a shell script or Perl can be lighter"),
    ], "A great language, but not the answer to every problem")


def python_argparse():
    return steps("python", "Python · argparse", "Command-line arguments with argparse", [
        ("import argparse", "standard library, nothing to install"),
        ("ArgumentParser()", "the parser and its description"),
        ("add_argument()", "name, type, help, required, default"),
        ("parse_args()", "reads sys.argv and validates it"),
        ("args.name", "use the values; -h prints help for free"),
    ], "argparse also reports missing or invalid arguments for you", mono_first=True)


def python_polymorphism():
    im, d, a, b = canvas("python", "Python · OOP", "Polymorphism: one call, many behaviours")
    base = (W / 2 - 170, 190, W / 2 + 170, 270)
    box(d, base, b, b, 14, 1)
    centred(d, W / 2, 200, "Animal", font(30, True), PAPER)
    centred(d, W / 2, 238, "make_sound()", font(22, mono=True), tint(a, 0.6))
    kids = [("Dog", "\"Bark\""), ("Cat", "\"Meow\"")]
    for i, (name, sound) in enumerate(kids):
        x = W / 2 + (-260 if i == 0 else 260)
        arrow(d, (x, 360), (W / 2 + (-90 if i == 0 else 90), 276), MUTED, 3, 12)
        box(d, [x - 150, 360, x + 150, 450], tint(a, 0.88), tint(a, 0.4), 14, 3)
        centred(d, x, 370, name, font(28, True), INK)
        centred(d, x, 410, "make_sound() → " + sound, font(21, mono=True), MUTED)
    centred(d, W / 2, 484, "for animal in animals: print(animal.make_sound())", font(24, mono=True), INK)
    footer(d, "The caller never checks the type: each class answers the same method its own way")
    return im


def python_venv():
    return steps("python", "Python", "Python virtual environments", [
        ("Create", "python3 -m venv venv"),
        ("Activate", "source venv/bin/activate"),
        ("Install", "pip install <packages>"),
        ("Freeze", "pip freeze > requirements.txt"),
        ("Recreate", "pip install -r requirements.txt"),
    ], "One project, one environment: no clashes between package versions")


def ansible_venv():
    return steps("linux", "Ansible · Molecule", "Ansible and Molecule in a virtual environment", [
        ("Project folder", "mkdir and cd into it"),
        ("python3-venv", "install the venv package (CentOS 7)"),
        ("Create", "python3 -m venv"),
        ("Activate", "source <env>/bin/activate"),
        ("pip install", "ansible, molecule and friends"),
    ], "Keeps Ansible and Molecule versions separate from the system Python")


def ansible_refresher():
    return cards("linux", "Ansible", "Why Ansible?", [
        ("Simple", "human-readable YAML, easy to learn"),
        ("Agentless", "nothing to install on managed hosts"),
        ("Idempotent", "runs converge to the desired state"),
        ("Modular", "roles package reusable tasks"),
        ("Integrates", "cloud, containers, network gear"),
        ("Community", "large, active, lots of collections"),
        ("Open source", "free to use and extend"),
    ], "An open-source platform for automating and configuring systems")


def ansible_playbook():
    """The four parts sit side by side inside one playbook (they are not nested in each other)."""
    im, d, a, b = canvas("linux", "Ansible", "Structure of a playbook")
    box(d, [56, 180, 760, H - 84], tint(a, 0.94), tint(b, 0.35), 18, 3)
    d.text((80, 192), "Playbook", font=font(28, True), fill=INK)
    d.text((80 + d.textlength("Playbook", font=font(28, True)) + 14, 199), "site.yml", font=font(20, mono=True),
           fill=MUTED)
    parts = [("Inventory", "the hosts to run on"), ("Variables", "values reused across tasks"),
             ("Roles", "reusable tasks, files and templates"), ("Tasks", "the actions to perform")]
    cw, ch = 316, 136
    for i, (head, detail) in enumerate(parts):
        r, c = divmod(i, 2)
        x0, y0 = 84 + c * (cw + 20), 248 + r * (ch + 18)
        box(d, [x0, y0, x0 + cw, y0 + ch], PAPER, tint(a, 0.4), 14, 3)
        d.rectangle([x0 + 2, y0 + 14, x0 + 8, y0 + ch - 14], fill=b)
        d.text((x0 + 24, y0 + 16), head, font=font(26, True), fill=INK)
        for j, line in enumerate(wrap(d, detail, font(20), cw - 44)):
            d.text((x0 + 24, y0 + 56 + j * 27), line, font=font(20), fill=MUTED)
    d.text((800, 190), "Example", font=font(26, True), fill=b)
    for j, line in enumerate(["- hosts: webservers", "  vars:", "    http_port: 80", "  roles:", "    - common",
                              "  tasks:", "    - name: …", "      tags: [web]"]):
        d.text((800, 236 + j * 36), line, font=font(22, mono=True), fill=INK)
    footer(d, "Use tags to run only some tasks or roles")
    return im


def ansible_templates():
    return steps("linux", "Ansible · Jinja2", "Ansible templates", [
        ("Template", "httpd.conf.j2 in the role's templates/"),
        ("Variables", "facts, vars, defaults"),
        ("Jinja2 renders", "{{ variables }}, loops, conditions"),
        ("template module", "copies the result to the host"),
        ("Config file", "/etc/httpd/conf/httpd.conf"),
    ], "One template, many hosts: each gets a file with its own values")


def ansible_cfg():
    return cards("linux", "Ansible", "ansible.cfg: settings you will use", [
        ("inventory", "where the hosts file is"),
        ("remote_user", "who to connect as"),
        ("become", "use privilege escalation"),
        ("become_user", "the user to become"),
        ("become_method", "sudo by default"),
        ("library", "where to find modules"),
        ("forks", "parallel processes (default 5)"),
        ("location", "./, ~/, or /etc/ansible/"),
    ], "The main configuration file: change Ansible's defaults in one place")


def ansible_variables():
    return cards("linux", "Ansible", "Where Ansible variables live", [
        ("Inline", "vars: on a single task"),
        ("Playbook", "vars: for the whole play"),
        ("Role", "my_role/vars/main.yml"),
        ("Inventory", "host_vars and group_vars"),
        ("Command line", "--extra-vars"),
        ("Facts", "gathered from each host"),
    ], "Define a value once, use it across playbooks, roles and tasks")


def ansible_lookup():
    im, d, a, b = canvas("linux", "Ansible · plugins", "The lookup plugin")
    sources = ["file", "env", "template", "programs"]
    for i, s in enumerate(sources):
        y = 190 + i * 88
        box(d, [56, y, 316, y + 66], tint(a, 0.9), tint(a, 0.45), 12, 3)
        centred(d, 186, y + 16, s, font(26, True, mono=True), INK)
        arrow(d, (322, y + 33), (440, 340), MUTED, 3, 10)
    box(d, [446, 280, 806, 400], b, b, 16, 1)
    centred(d, 626, 300, "{{ lookup('<plugin>',", font(24, True, mono=True), PAPER)
    centred(d, 626, 340, "'<arguments>') }}", font(24, True, mono=True), PAPER)
    arrow(d, (812, 340), (900, 340), b, 4, 12)
    box(d, [906, 270, W - 56, 410], tint(a, 0.9), tint(a, 0.45), 16, 3)
    centred(d, 1025, 290, "a value", font(26, True), INK)
    centred(d, 1025, 330, "for vars, templates or when: conditions", font(20), MUTED, 200)
    footer(d, "Read data from files, environment variables, templates or commands at run time")
    return im


def ansible_async():
    return steps("linux", "Ansible", "Long-running tasks: async and poll", [
        ("async: 300", "the task may run in the background for up to 300 s"),
        ("poll: 60", "Ansible checks on it every 60 s"),
        ("register", "keep the job ID in task_result"),
        ("async_status", "with the job ID, until: finished"),
        ("debug", "print stdout_lines when it is done"),
    ], "Show progress instead of a playbook that seems to hang", mono_first=True)


def git_pat():
    return steps("devops", "Git", "Using a Personal Access Token", [
        ("Generate", "in your Git provider's settings"),
        ("Keep it safe", "treat it like a password"),
        ("Configure git", "user.name and user.email"),
        ("Credential helper", "osxkeychain on macOS"),
        ("Push", "paste the PAT when asked for a password"),
    ], "A token instead of your account password: scoped, and easy to revoke")


def podman_machine():
    return nested("docker", "Containers · Podman", "Podman Machine", [
        ("Your system", "local machine or a remote server"),
        ("Podman Machine", "a VM that runs the containers"),
        ("Podman", "the container runtime"),
        ("Containers", "many on one machine"),
    ], "Create a machine, start it, then run containers in it", side=("Commands", [
        "podman machine create \\", "  <machine-name>", "podman machine start \\", "  <machine-name>",
        "podman run -d \\", "  -p 8080:80 nginx"]))


def podman_molecule():
    return nested("docker", "Containers · Molecule", "Molecule with rootless Podman", [
        ("Molecule", "tests the Ansible role"),
        ("podman-docker", "docker CLI → podman"),
        ("podman.socket", "API for the user"),
        ("Containers", "run as non-root"),
    ], "The fix: enable the user's podman.socket and point DOCKER_HOST at it", side=("Steps", [
        "systemctl enable --now \\", "  --user podman.socket", "export DOCKER_HOST=\\",
        "  unix:///run/user/<uid>/\\", "  podman/podman.sock", "molecule test"]))


def curl_anatomy():
    im, d, a, b = canvas("web", "Web · cURL", "cURL: a true companion")
    cmd = "curl -X POST -H \"Content-Type: application/json\" -d '{...}' https://api"
    box(d, [56, 180, W - 56, 250], INK, INK, 14, 1)
    d.text((80, 196), cmd, font=font(25, mono=True), fill=PAPER)
    parts = [("-X", "method: GET, POST, PUT, DELETE"), ("-H", "headers, e.g. Content-Type"),
             ("-d", "the request body"), ("URL", "HTTP, HTTPS, FTP and more")]
    cw = (W - 112 - 3 * 22) / 4
    for i, (flag, what) in enumerate(parts):
        x0 = 56 + i * (cw + 22)
        box(d, [x0, 290, x0 + cw, 420], tint(a, 0.9), tint(a, 0.45), 14, 3)
        centred(d, x0 + cw / 2, 304, flag, font(30, True, mono=True), b)
        centred(d, x0 + cw / 2, 352, what, font(20), MUTED, cw - 30)
    centred(d, W / 2, 452, "add -v to see the request and response headers", font(22, True), INK)
    footer(d, "Transfer data between clients and servers from the command line")
    return im


IMAGES = {  # slug: (file name, drawing function)
    "x509-history": ("x509.png", x509_history),
    "handshake": ("ssl-handshake.png", tls_handshake),
    "ssl-tls": ("ssl-tls.png", ssl_tls),
    "trust-store-apache-kafka": ("ks-store.png", keystore_truststore(
        "Keystore and truststore", "Kafka brokers and clients use both for TLS between them")),
    # "keystore-vs-truststore": the original drawing was found on 2026-10-27, so it is no longer recreated
    "python-vs-bash": ("pycomp.png", python_vs_bash),
    "python-when-not-to-use-it": ("nopy.png", python_when_not),
    "python-argparse": ("pyarg.png", python_argparse),
    "python-polymorphism": ("pypoly.png", python_polymorphism),
    "venvansible": ("an-lint-1.png", python_venv),
    "venv-ansible": ("an-venv.png", ansible_venv),
    "ansible-refresher": ("an-refresh.png", ansible_refresher),
    "ansible-structure-of-a-playbook": ("ansible.png", ansible_playbook),
    "ansible-templates": ("an-template.png", ansible_templates),
    "ansible-configuration-ansible-cfg": ("an-config.png", ansible_cfg),
    "ansible-variables-2": ("ans-vars.png", ansible_variables),
    "lookup-ansible": ("an-lookup.png", ansible_lookup),
    "async-poll-notify-ansible-long-running-process": ("as-async.png", ansible_async),
    "pat-personal-access-token": ("an-lint.png", git_pat),
    "podman-machine-how-why": ("podman.png", podman_machine),
    "non-root-podman-and-molecule": ("molecule.png", podman_molecule),
    "curl": ("curl.png", curl_anatomy),
}


def main():
    wanted = sys.argv[1:] or list(IMAGES)
    for slug in wanted:
        name, draw = IMAGES[slug]
        out = MEDIA / slug / name
        out.parent.mkdir(parents=True, exist_ok=True)
        draw().save(out, optimize=True)
        print(f"{slug}: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
