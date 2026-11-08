"""Anime covers for the Linux posts that had no image of their own (2026-11-08).

One animal per post, picked for the post's idea (several are puns): a conductor rabbit (Ansible, agentless), a sloth
(async and poll), an owl (notes), a mouse with a key (SSH access), a chameleon (variables), an auk-like puffin (awk),
a pointer dog (named references), a turtle guard (kernel mode), a bat (ping), a parrot (locale), a squirrel with
sticky notes (bash notes), a meerkat on lookout (ps), a frog scientist (Molecule), a raccoon locksmith (ssh-keygen),
a hedgehog with a padlock (SSH protocol), a mother duck and ducklings (systemd, PID 1) and a mole (SSH tunnels).
The right half shows a real command or idea from each post, with neutral host names.

Run from the repo root: python tools/covers/anime/linux.py [slug ...]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403

HX, HY = HAND


def term(title, lines, size=19, y=150):
    return terminal(600, y, 560, 92 + len(lines) * 31, title, lines, size=size)


def kicker(text, fill):
    return pill(600, 66, text, fill, size=21)


def cover(slug, title, sky, animal, panel, label, label_fill, spark=((40, 70, 24), (560, 40, 18), (1165, 600, 22))):
    write(slug, title, sky, panel + kicker(label, label_fill) + animal + sparkles(spark))


OK = "#4ade80"
DIM = "#94a3b8"
WARN = "#f87171"
KEY = "#fbbf24"

# 1. Ansible: a thought -- a conductor rabbit; the servers answer without agents ---------------------------------
baton = (f'<path d="M{HX} {HY} L{HX + 110} {HY - 120}" stroke="#f8fafc" stroke-width="8" stroke-linecap="round" filter="url(#drop)"/>'
         f'<circle cx="{HX + 112}" cy="{HY - 122}" r="9" fill="#facc15"/>'
         f'<path d="M{HX + 70} {HY - 170} q12 -14 24 0 M{HX + 130} {HY - 160} l0 -36 l20 6" stroke="#7c3aed" stroke-width="5" fill="none" stroke-linecap="round"/>')
cover("ansible-a-thought",
      "Anime illustration: a white rabbit in a conductor's top hat waves a baton, and a terminal shows ansible all -m ping "
      "with web1, web2 and db1 answering SUCCESS pong over plain SSH, no agents",
      dict(s1="#fbcfe8", s2="#fce7f3", s3="#fdf2f8"),
      critter(fur=("#ffffff", "#d6d3d1"), belly="#fafaf9", ears="long", ear_inner="#fbcfe8", hat="tophat",
              iris=("#831843", "#f472b6"), mouth="open", nose_col="#f472b6", prop=baton, scarf="#7c3aed"),
      term("control node", ["$ ansible all -m ping", ("web1 | SUCCESS => pong", OK), ("web2 | SUCCESS => pong", OK),
                            ("db1  | SUCCESS => pong", OK), "", ("# no agents on the nodes,", DIM), ("# just SSH and YAML", DIM)]),
      "Ansible: agentless automation", "#be185d")

# 2. Ansible async & poll -- a sloth with an hourglass: fire and forget, check later -----------------------------
hourglass = (f'<g filter="url(#drop)" transform="translate({HX + 20} {HY - 150})"><rect x="-40" y="0" width="80" height="12" rx="5" fill="#92400e"/>'
             '<rect x="-40" y="128" width="80" height="12" rx="5" fill="#92400e"/>'
             '<path d="M-30 12 C-30 50 -6 60 -6 70 C-6 80 -30 90 -30 128 L30 128 C30 90 6 80 6 70 C6 60 30 50 30 12Z" fill="#e0f2fe" stroke="#0369a1" stroke-width="3"/>'
             '<path d="M-20 30 L20 30 L4 64 L-4 64Z M-24 124 C-20 104 20 104 24 124Z" fill="#f59e0b"/><path d="M0 64 L0 110" stroke="#f59e0b" stroke-width="3"/></g>')
cover("ansible-async-poll",
      "Anime illustration: a sleepy sloth in a night cap holds an hourglass beside a playbook that runs long_task.sh with "
      "async 3600 and poll 0, then checks it later with async_status",
      dict(s1="#c7d2fe", s2="#e0e7ff", s3="#f5f3ff"),
      critter(fur=("#c8ad8d", "#7c5f3f"), belly="#ede0cf", ears="none", mask="sloth", sleepy=True, hat="nightcap",
              iris=("#292524", "#78716c"), mouth="smile", prop=hourglass),
      term("playbook.yml", ["- name: Run long task asynchronously", "  command: long_task.sh", ("  async: 3600", KEY), ("  poll: 0", KEY),
                            "- name: Check async task status", "  async_status:", '    jid: "{{ ansible_job_id }}"'], size=18),
      "Ansible: async & poll", "#4338ca")

# 3. Ansible notes -- an owl with glasses and a notebook ------------------------------------------------------------
notebook = (f'<g filter="url(#drop)" transform="rotate(-12 {HX + 40} {HY - 60})"><rect x="{HX - 10}" y="{HY - 140}" width="120" height="150" rx="8" fill="#fef3c7" stroke="#b45309" stroke-width="3"/>'
            + "".join(f'<path d="M{HX + 8} {HY - 110 + i * 24} H{HX + 92}" stroke="#93c5fd" stroke-width="3"/>' for i in range(5))
            + f'<path d="M{HX - 10} {HY - 140} V{HY + 10}" stroke="#dc2626" stroke-width="6"/></g>')
cover("ansible-notes",
      "Anime illustration: a brown owl in round glasses holds a notebook, next to a list of Ansible's building blocks: "
      "control node, managed nodes, inventory, modules, tasks and playbooks",
      dict(s1="#fde68a", s2="#fef3c7", s3="#fffbeb"),
      critter(fur=("#a16207", "#713f12"), belly="#fde68a", ears="tufts", mask="owl", snout="beak", glasses=True,
              back=("wings",), iris=("#7c2d12", "#f59e0b"), beak_col=("#fcd34d", "#d97706"), prop=notebook),
      term("ansible: the basics", [("▸ control node", KEY), "    runs ansible", ("▸ managed nodes", KEY), "    reached over SSH",
                                   ("▸ inventory", KEY), ("▸ modules · tasks · playbooks", KEY)]),
      "Ansible: notes", "#a16207")

# 4. Ansible SSH access -- a mouse carrying a big key --------------------------------------------------------------
bigkey = (f'<g filter="url(#drop)" transform="rotate(-40 {HX} {HY})"><circle cx="{HX}" cy="{HY - 70}" r="40" fill="#facc15" stroke="#a16207" stroke-width="5"/>'
          f'<circle cx="{HX}" cy="{HY - 70}" r="14" fill="#fef9c3"/><rect x="{HX - 9}" y="{HY - 32}" width="18" height="130" fill="#facc15" stroke="#a16207" stroke-width="4"/>'
          f'<rect x="{HX + 9}" y="{HY + 60}" width="26" height="14" fill="#facc15" stroke="#a16207" stroke-width="3"/><rect x="{HX + 9}" y="{HY + 82}" width="18" height="12" fill="#facc15" stroke="#a16207" stroke-width="3"/></g>')
cover("ansible-ssh-access",
      "Anime illustration: a grey mouse with big pink ears carries a golden key, beside a terminal running ssh-keygen -t rsa, "
      "ssh-copy-id user@hostname and ansible all -m ping, which answers SUCCESS pong",
      dict(s1="#fef08a", s2="#fef9c3", s3="#f0fdf4"),
      critter(fur=("#e5e7eb", "#9ca3af"), belly="#f9fafb", ears="round", ear_inner="#f9a8d4", nose_col="#f472b6",
              iris=("#1e293b", "#64748b"), mouth="grin", prop=bigkey),
      term("control node", ["$ ssh-keygen -t rsa", (" 1. key pair created", DIM), "$ ssh-copy-id user@hostname", (" 2. public key copied", DIM),
                            "$ ansible all -m ping", ("hostname | SUCCESS => pong", OK)]),
      "Ansible: SSH access", "#ca8a04")

# 5. Ansible variables -- a chameleon: one name, a different value on every host --------------------------------------
swatch = ('<g filter="url(#drop)">' + "".join(f'<circle cx="{HX + 40 + i * 34}" cy="{HY - 90 - (i % 2) * 26}" r="16" fill="{c}" stroke="#ffffff" stroke-width="3"/>'
                                         for i, c in enumerate(["#ef4444", "#f59e0b", "#22c55e", "#3b82f6"])) + "</g>")
cover("ansible-variables",
      "Anime illustration: a green-to-teal chameleon with a curled tail juggles coloured dots, beside a playbook that prints "
      "ansible_fqdn and ansible_default_ipv4.address facts and a custom_message variable",
      dict(s1="#a7f3d0", s2="#d1fae5", s3="#ecfeff"),
      critter(fur=("#86efac", "#0d9488"), belly="#d9f99d", ears="none", back=("tail_curl", "tuft"), snout="none",
              iris=("#065f46", "#facc15"), look=(12, -6), mouth="grin", prop=swatch),
      term("playbook.yml", ["- hosts: all", "  gather_facts: true", "  vars:", ('    custom_message: "Hello!"', KEY), "  tasks:",
                            "    - debug:", ('        msg: "{{ ansible_fqdn }}"', OK), "    - debug:", ('        msg: "{{ custom_message }}"', OK)], size=18),
      "Ansible: variables", "#0f766e")

# 6. AWK -- an auk (well, a puffin) with a fish labelled $1 -----------------------------------------------------------
fish = (f'<g filter="url(#drop)" transform="rotate(-20 {HX + 60} {HY - 40})"><ellipse cx="{HX + 60}" cy="{HY - 40}" rx="60" ry="24" fill="#93c5fd" stroke="#1d4ed8" stroke-width="3"/>'
        f'<path d="M{HX + 118} {HY - 40} L{HX + 150} {HY - 64} L{HX + 150} {HY - 16}Z" fill="#93c5fd" stroke="#1d4ed8" stroke-width="3"/>'
        f'<circle cx="{HX + 22}" cy="{HY - 46}" r="5" fill="#1e3a8a"/>'
        f'<text x="{HX + 66}" y="{HY - 32}" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="800" fill="#1e3a8a">$1</text></g>')
PUFFIN_BILL = ('<g filter="url(#drop)"><path d="M218 316 Q270 296 322 316 L270 410Z" fill="#f97316" stroke="#9a3412" stroke-width="3" stroke-linejoin="round"/>'
               '<path d="M218 316 Q270 296 322 316 L314 334 Q270 318 226 334Z" fill="#64748b"/>'
               '<path d="M232 348 Q270 334 308 348 L300 362 Q270 350 240 362Z" fill="#facc15"/>'
               '<path d="M270 330 L270 404" stroke="#9a3412" stroke-width="2" opacity="0.6"/></g>'
               '<path d="M176 268 L150 250 M364 268 L390 250" stroke="#64748b" stroke-width="5" stroke-linecap="round"/>')
cover("awk",
      "Anime illustration: a puffin (a kind of auk) with a striped orange bill holds a fish labelled $1, beside a terminal where awk '/at/' "
      "keeps only gate and what, and awk sums the first column",
      dict(s1="#bae6fd", s2="#e0f2fe", s3="#f8fafc"),
      critter(fur=("#334155", "#0f172a"), belly="#f8fafc", ears="none", mask="puffin", snout="none", mouth="", back=("wings",),
              iris=("#0f172a", "#334155"), hand_col="#1e293b", prop=PUFFIN_BILL + fish),
      term("awk", ["$ printf 'gate\\napple\\nwhat\\nkite\\n' \\", "    | awk '/at/'", ("gate", OK), ("what", OK), "",
                   "$ awk '{ sum += $1 } END { print sum }'", ("# pattern { action }", DIM)], size=18),
      "AWK: pattern { action }", "#0369a1")

# 7. Bash named reference -- a pointer dog, pointing ---------------------------------------------------------------------
point = arrow(f"M{HX + 40} {HY - 30} C{HX + 80} {HY - 60} {HX + 110} {HY - 70} {HX + 140} {HY - 72}", "#dc2626", width=7)
cover("bash-named-reference",
      "Anime illustration: a golden pointer dog with floppy brown ears and a red collar points at a terminal: declare -n "
      "ref=target, ref=42, echo $target prints 42; bash 4.2.46 has no -n, bash 5.1.8 does",
      dict(s1="#fed7aa", s2="#ffedd5", s3="#fff7ed"),
      critter(fur=("#fde68a", "#d97706"), belly="#fffbeb", ears="floppy", scarf="#dc2626", face="#fef3c7",
              iris=("#78350f", "#d97706"), mouth="open", prop=point),
      term("bash", ["$ declare -n ref=target", "$ ref=42", "$ echo $target", ("42", OK), "",
                    ("bash 4.2.46: declare -n  ✗", WARN), ("bash 5.1.8:  declare -n  ✓", OK)]),
      "Bash: named references", "#c2410c")

# 8. Kernel mode -- a turtle guard with a shield between user mode and kernel mode -----------------------------------------
shield = (f'<g filter="url(#drop)"><path d="M{HX + 10} {HY - 120} L{HX + 110} {HY - 100} C{HX + 110} {HY - 20} {HX + 80} {HY + 20} {HX + 60} {HY + 30} '
          f'C{HX + 40} {HY + 20} {HX + 10} {HY - 20} {HX + 10} {HY - 120}Z" fill="#2563eb" stroke="#1e3a8a" stroke-width="5"/>'
          f'<rect x="{HX + 42}" y="{HY - 62}" width="38" height="30" rx="5" fill="#facc15"/><path d="M{HX + 49} {HY - 62} V{HY - 76} C{HX + 49} {HY - 94} {HX + 73} {HY - 94} {HX + 73} {HY - 76} V{HY - 62}" stroke="#facc15" stroke-width="6" fill="none"/></g>')
zones = f'''
  <g filter="url(#drop)">
    <rect x="600" y="150" width="560" height="190" rx="18" fill="#ffffff" stroke="#f59e0b" stroke-width="4"/>
    <text x="630" y="192" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">User mode</text>
    <text x="1130" y="192" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="700" fill="#b45309">untrusted · restricted</text>
    {"".join(f'<rect x="{630 + i * 128}" y="220" width="112" height="90" rx="12" fill="#fef3c7"/><text x="{686 + i * 128}" y="272" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" fill="#92400e">{t}</text>' for i, t in enumerate(["bash", "nginx", "python", "vim"]))}
    <rect x="600" y="400" width="560" height="190" rx="18" fill="#1e293b"/>
    <text x="630" y="442" font-family="{SANS}" font-size="24" font-weight="800" fill="#f8fafc">Kernel mode</text>
    <text x="1130" y="442" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="700" fill="#4ade80">trusted · full access</text>
    {"".join(f'<rect x="{630 + i * 170}" y="470" width="150" height="90" rx="12" fill="#334155"/><text x="{705 + i * 170}" y="522" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" fill="#a5f3fc">{t}</text>' for i, t in enumerate(["memory", "CPU", "I/O"]))}
  </g>
  {arrow("M880 318 L880 392", "#7c3aed", width=6)}
  <text x="896" y="364" font-family="{SANS}" font-size="19" font-weight="800" fill="#6d28d9">system call</text>'''
cover("kernel-mode",
      "Anime illustration: a green turtle in its shell holds a blue shield with a padlock. Beside it, user mode holds "
      "untrusted programs such as bash, nginx, python and vim, and a system call arrow leads down to trusted kernel mode "
      "with full access to memory, CPU and I/O",
      dict(s1="#bbf7d0", s2="#dcfce7", s3="#f7fee7"),
      critter(fur=("#bef264", "#65a30d"), belly="#fef9c3", ears="none", back=("shell",), iris=("#14532d", "#4ade80"),
              mouth="smile", prop=shield),
      zones, "Kernel mode vs user mode", "#15803d")

# 9. Linux utils (ping) -- a bat: it pings and listens for the echo ---------------------------------------------------------
sonar = "".join(f'<path d="M{HX + 40 + i * 28} {HY - 70 - i * 16} C{HX + 70 + i * 34} {HY - 40 - i * 4} {HX + 70 + i * 34} {HY + 10 + i * 4} '
                f'{HX + 40 + i * 28} {HY + 40 + i * 16}" stroke="#a78bfa" stroke-width="7" fill="none" stroke-linecap="round" opacity="{1 - i * 0.25}"/>'
                for i in range(3))
cover("linux-utils",
      "Anime illustration: a purple bat with big ears sends out sonar rings, beside a terminal running ping -c 3 example.com: "
      "three ICMP echo replies, 0% packet loss",
      dict(s1="#ddd6fe", s2="#ede9fe", s3="#faf5ff"),
      critter(fur=("#a78bfa", "#5b21b6"), belly="#ede9fe", ears="bat", ear_inner="#f0abfc", back=("bat_wings",),
              iris=("#7c2d12", "#fbbf24"), mouth="open", nose_col="#3b0764", prop=sonar),
      term("ping", ["$ ping -c 3 example.com", "PING example.com 56(84) bytes of data.", ("64 bytes: icmp_seq=1 ttl=53 time=25 ms", OK),
                    ("64 bytes: icmp_seq=2 ttl=53 time=24 ms", OK), ("64 bytes: icmp_seq=3 ttl=53 time=25 ms", OK),
                    "3 packets transmitted, 3 received,", ("0% packet loss", OK)], size=18),
      "Linux utils: ping", "#6d28d9")

# 10. Locale -- a parrot that speaks many languages ----------------------------------------------------------------------
speech = (f'<g filter="url(#drop)"><path d="M{HX + 10} {HY - 80} C{HX + 0} {HY - 160} {HX + 160} {HY - 160} {HX + 160} {HY - 110} '
          f'C{HX + 160} {HY - 70} {HX + 80} {HY - 70} {HX + 50} {HY - 72} L{HX + 20} {HY - 40} L{HX + 30} {HY - 76}Z" fill="#ffffff"/>'
          f'<text x="{HX + 76}" y="{HY - 108}" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="#15803d">Hola!</text>'
          f'<text x="{HX + 80}" y="{HY - 84}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="#64748b">Hello · Bonjour</text></g>')
cover("locale-centos",
      "Anime illustration: a green parrot with a red crest says Hola, Hello, Bonjour, beside a terminal showing the "
      "setlocale LC_CTYPE warning at login and the fix in /etc/environment: LANG and LC_ALL set to en_US.utf-8",
      dict(s1="#fecaca", s2="#fee2e2", s3="#f0fdf4"),
      critter(fur=("#4ade80", "#15803d"), belly="#fef08a", ears="none", snout="beak", back=("crest", "wings"),
              iris=("#1e293b", "#475569"), beak_col=("#fde68a", "#f59e0b"), prop=speech),
      term("login", [("-bash: warning: setlocale: LC_CTYPE:", WARN), ("cannot change locale (UTF-8)", WARN), "",
                     "$ cat /etc/environment", ("LANG=en_US.utf-8", OK), ("LC_ALL=en_US.utf-8", OK)]),
      "Locale: silence the warning", "#b91c1c")

# 11. Notes: for self -- a squirrel stashing sticky notes ------------------------------------------------------------------
stickies = "".join(f'<g filter="url(#drop)" transform="rotate({r} {HX + x} {HY + y})"><rect x="{HX + x - 36}" y="{HY + y - 36}" width="72" height="72" rx="4" fill="{c}"/>'
                   f'<text x="{HX + x}" y="{HY + y + 8}" text-anchor="middle" font-family="{MONO}" font-size="20" font-weight="800" fill="#334155">{t}</text></g>'
                   for x, y, r, c, t in [(20, -120, -8, "#fef08a", "[["), (90, -80, 10, "#fbcfe8", "=="), (60, -20, -4, "#bbf7d0", "bc")])
SQUIRREL_TAIL = ('<defs><linearGradient id="stail" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdba74"/><stop offset="1" stop-color="#c2410c"/></linearGradient></defs>'
                 '<path d="M150 610 C30 600 0 470 50 380 C90 310 20 240 60 150 C100 70 220 70 230 140 C236 190 170 200 160 260 C150 330 230 450 190 610Z" fill="url(#stail)" filter="url(#drop)"/>'
                 '<path d="M70 170 C100 110 170 100 200 130" stroke="#ffedd5" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>')
cover("notes-1",
      "Anime illustration: an orange squirrel with a fluffy tail holds sticky notes reading [[, == and bc, beside a terminal "
      "of Bash notes: let step++ equals (( step++ )), = and == mean the same, [ versus [[, and bc for decimals",
      dict(s1="#fed7aa", s2="#ffedd5", s3="#fefce8"),
      SQUIRREL_TAIL + critter(fur=("#fb923c", "#9a3412"), belly="#ffedd5", ears="pointy", ear_inner="#fed7aa",
              iris=("#451a03", "#b45309"), mouth="grin", prop=stickies),
      term("bash notes", ['$ let "step++"     # same as (( step++ ))', '$ [ "$a" = "$b" ]  # = and == agree', '$ [[ $a == b* ]]   # [[ adds patterns',
                          "$ echo '7/2' | bc -l", ("3.50000000000000000000", OK)], size=18),
      "Notes: Bash for self", "#c2410c")

# 12. ps -- a meerkat on lookout with binoculars: a snapshot of what's running -----------------------------------------------
binoculars = (f'<g filter="url(#drop)" transform="rotate(-15 {HX + 30} {HY - 40})"><rect x="{HX - 10}" y="{HY - 80}" width="36" height="64" rx="12" fill="#334155"/>'
              f'<rect x="{HX + 36}" y="{HY - 80}" width="36" height="64" rx="12" fill="#334155"/><rect x="{HX + 20}" y="{HY - 64}" width="22" height="18" fill="#475569"/>'
              f'<circle cx="{HX + 8}" cy="{HY - 80}" r="14" fill="#7dd3fc" stroke="#334155" stroke-width="5"/><circle cx="{HX + 54}" cy="{HY - 80}" r="14" fill="#7dd3fc" stroke="#334155" stroke-width="5"/></g>')
cover("ps-process-status",
      "Anime illustration: a meerkat on lookout holds binoculars, beside a terminal with ps aux listing systemd as PID 1, "
      "kthreadd and sshd, and ps aux piped to wc -l counting the processes",
      dict(s1="#fde68a", s2="#fef3c7", s3="#fefce8"),
      critter(fur=("#e7c9a0", "#a8835a"), belly="#f5ebdc", ears="small", mask="meerkat", iris=("#1c1917", "#78716c"),
              mouth="o", prop=binoculars),
      term("ps: a snapshot", ["$ ps aux | head -4", ("USER   PID %CPU COMMAND", DIM), "root     1  0.0 /usr/lib/systemd/systemd",
                              "root     2  0.0 [kthreadd]", "root   812  0.0 /usr/sbin/sshd -D", "$ ps aux | wc -l", ("212", OK)], size=18),
      "PS: process status", "#a16207")

# 13. Molecule -- a frog scientist testing a role in a flask ---------------------------------------------------------------
flask = (f'<g filter="url(#drop)"><path d="M{HX + 10} {HY - 150} L{HX + 50} {HY - 150} L{HX + 50} {HY - 100} L{HX + 90} {HY - 20} '
         f'C{HX + 96} {HY - 6} {HX + 86} {HY + 4} {HX + 72} {HY + 4} L{HX - 12} {HY + 4} C{HX - 26} {HY + 4} {HX - 36} {HY - 6} {HX - 30} {HY - 20} L{HX + 10} {HY - 100}Z" '
         f'fill="#ecfeff" stroke="#0e7490" stroke-width="4"/><path d="M{HX - 18} {HY - 40} L{HX + 78} {HY - 40} L{HX + 88} {HY - 20} C{HX + 92} {HY - 8} {HX + 84} {HY} {HX + 72} {HY} '
         f'L{HX - 12} {HY} C{HX - 24} {HY} {HX - 32} {HY - 8} {HX - 28} {HY - 20}Z" fill="#a3e635"/>'
         f'<circle cx="{HX + 20}" cy="{HY - 60}" r="8" fill="#d9f99d"/><circle cx="{HX + 40}" cy="{HY - 84}" r="6" fill="#d9f99d"/><circle cx="{HX + 28}" cy="{HY - 120}" r="5" fill="#d9f99d"/></g>')
cover("scenario-molecule",
      "Anime illustration: a green frog scientist in lab goggles holds a bubbling flask, beside a terminal running molecule "
      "init scenario check_python_installed -d docker and the tree it creates: converge.yml, molecule.yml, verify.yml",
      dict(s1="#a5f3fc", s2="#cffafe", s3="#f7fee7"),
      critter(fur=("#86efac", "#16a34a"), belly="#ecfccb", ears="frog", snout="none", iris=("#713f12", "#facc15"),
              look=(12, 4), mouth="grin", hat=None, prop=flask),
      term("molecule", ["$ molecule init scenario \\", "    check_python_installed -d docker", "$ tree molecule/check_python_installed",
                        "molecule/check_python_installed", ("├── converge.yml", OK), ("├── molecule.yml", OK), ("└── verify.yml", OK)], size=18),
      "Molecule: test a role", "#0e7490")

# 14. ssh-keygen & ssh-copy-id -- a raccoon locksmith with a matched key and lock ---------------------------------------------
keypair = (f'<g filter="url(#drop)"><circle cx="{HX + 30}" cy="{HY - 110}" r="26" fill="#facc15" stroke="#a16207" stroke-width="4"/>'
           f'<rect x="{HX + 24}" y="{HY - 86}" width="12" height="80" fill="#facc15" stroke="#a16207" stroke-width="3"/>'
           f'<rect x="{HX + 36}" y="{HY - 30}" width="18" height="10" fill="#facc15" stroke="#a16207" stroke-width="2"/>'
           f'<rect x="{HX + 80}" y="{HY - 60}" width="64" height="54" rx="8" fill="#94a3b8" stroke="#334155" stroke-width="4"/>'
           f'<path d="M{HX + 92} {HY - 60} V{HY - 80} C{HX + 92} {HY - 106} {HX + 132} {HY - 106} {HX + 132} {HY - 80} V{HY - 60}" stroke="#334155" stroke-width="8" fill="none"/>'
           f'<circle cx="{HX + 112}" cy="{HY - 36}" r="7" fill="#334155"/></g>')
cover("ssh-keygen-ssh-copy-id",
      "Anime illustration: a raccoon locksmith with a striped tail holds a golden key next to a padlock, beside a terminal "
      "running ssh-keygen and ssh-copy-id: the private key stays home, the public key goes to the server",
      dict(s1="#e2e8f0", s2="#f1f5f9", s3="#fefce8"),
      critter(fur=("#a8a29e", "#57534e"), belly="#e7e5e4", ears="round", ear_inner="#d6d3d1", mask="raccoon",
              back=("tail_stripes",), face="#f5f5f4", iris=("#1e293b", "#94a3b8"), mouth="grin", prop=keypair),
      term("~/.ssh", ["$ ssh-keygen -t rsa -b 4096", ("~/.ssh/id_rsa      private: keep it", KEY), ("~/.ssh/id_rsa.pub  public: share it", OK), "",
                      "$ ssh-copy-id user@remote-host", ("key added to authorized_keys", OK)], size=18),
      "ssh-keygen & ssh-copy-id", "#475569")

# 15. SSH protocol -- a hedgehog (spiky, safe) guarding the connection -----------------------------------------------------
lock = (f'<g filter="url(#drop)"><rect x="{HX - 6}" y="{HY - 80}" width="90" height="74" rx="12" fill="#22c55e" stroke="#14532d" stroke-width="4"/>'
        f'<path d="M{HX + 12} {HY - 80} V{HY - 104} C{HX + 12} {HY - 140} {HX + 66} {HY - 140} {HX + 66} {HY - 104} V{HY - 80}" stroke="#14532d" stroke-width="10" fill="none"/>'
        f'<circle cx="{HX + 39}" cy="{HY - 48}" r="9" fill="#14532d"/></g>')
proto = f'''
  <g filter="url(#drop)">
    <rect x="600" y="150" width="190" height="96" rx="16" fill="#ffffff" stroke="#0ea5e9" stroke-width="4"/>
    <text x="695" y="194" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">client</text>
    <text x="695" y="224" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#0369a1">drives the setup</text>
    <rect x="970" y="150" width="190" height="96" rx="16" fill="#ffffff" stroke="#16a34a" stroke-width="4"/>
    <text x="1065" y="194" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">server</text>
    <text x="1065" y="224" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#15803d">port 22</text>
  </g>
  <path d="M796 198 H962" stroke="#0f172a" stroke-width="6" stroke-dasharray="4 10" stroke-linecap="round"/>
  <text x="880" y="186" text-anchor="middle" font-size="30">🔒</text>
  {terminal(600, 280, 560, 300, "how a session is set up", [("1  server proves who it is", OK), "   public-key cryptography", ("2  you log in", OK),
                                                            "   password  or  public key ✓", ("3  everything after is", OK), "   symmetric encryption + hashing"], size=19)}'''
cover("ssh-protocol",
      "Anime illustration: a hedgehog with brown spikes holds a green padlock, beside a client and a server on port 22 "
      "joined by a locked line: the server proves its identity with public-key cryptography, you log in with a password "
      "or a public key, and the session is protected with symmetric encryption and hashing",
      dict(s1="#bae6fd", s2="#e0f2fe", s3="#f0fdf4"),
      critter(fur=("#e7c9a0", "#b08356"), belly="#fef3c7", ears="small", back=("spikes",), face="#fef3c7",
              iris=("#1e293b", "#475569"), mouth="smile", prop=lock),
      proto, "SSH: the secure shell", "#0369a1")

# 16. systemd -- a mother duck (PID 1) leading her ducklings (services) -----------------------------------------------------
ducklings = "".join(f'''<g filter="url(#drop)"><ellipse cx="{x}" cy="{y}" rx="34" ry="28" fill="#fde047"/><circle cx="{x + 4}" cy="{y - 34}" r="22" fill="#fde047"/>
  <circle cx="{x + 12}" cy="{y - 38}" r="4" fill="#1f2937"/><path d="M{x + 22} {y - 32} L{x + 40} {y - 28} L{x + 22} {y - 24}Z" fill="#fb923c"/>
  <rect x="{x - 40}" y="{y + 30}" width="80" height="26" rx="13" fill="#ffffff"/>
  <text x="{x}" y="{y + 49}" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="800" fill="#334155">{t}</text></g>'''
                    for x, y, t in [(420, 520, "sshd"), (500, 470, "crond"), (560, 540, "nginx")])
cover("systemd-mother-of-all-processes",
      "Anime illustration: a white mother duck labelled PID 1 leads three ducklings named sshd, crond and nginx, beside a "
      "terminal where pstree shows systemd at the root of every process and systemctl starts services in parallel",
      dict(s1="#bfdbfe", s2="#dbeafe", s3="#fefce8"),
      critter(fur=("#ffffff", "#e2e8f0"), belly="#f8fafc", ears="none", snout="bill", back=("tuft", "wings"),
              iris=("#1e293b", "#475569"), beak_col=("#fdba74", "#f97316"), scarf="#2563eb", prop="")
      + ducklings + pill(150, 560, "PID 1", "#2563eb", size=20),
      term("systemd", ["$ pstree -p | head -5", "systemd(1)─┬─sshd(812)", "           ├─crond(640)", "           ├─nginx(1102)",
                       "           └─journald(410)", "$ systemctl status sshd", ("● sshd.service  active (running)", OK)], size=18),
      "systemd: mother of all processes", "#1d4ed8", spark=((40, 70, 24), (560, 40, 18), (1165, 600, 22)))

# 17. SSH tunnel -- a mole with a headlamp and a shovel ---------------------------------------------------------------------
shovel = (f'<g filter="url(#drop)" transform="rotate(200 {HX} {HY - 20})"><rect x="{HX - 6}" y="{HY - 150}" width="12" height="170" rx="5" fill="#92400e"/>'
          f'<path d="M{HX - 30} {HY + 20} L{HX + 30} {HY + 20} L{HX + 24} {HY + 80} C{HX + 10} {HY + 100} {HX - 10} {HY + 100} {HX - 24} {HY + 80}Z" fill="#94a3b8" stroke="#475569" stroke-width="4"/>'
          f'<rect x="{HX - 20}" y="{HY - 162}" width="40" height="14" rx="7" fill="#92400e"/></g>')
cover("tunnel-ssh",
      "Anime illustration: a dark brown mole with a pink nose, a headlamp and a shovel, beside a terminal with three SSH "
      "tunnels: -L forwards a local port to web-server:80, -R opens a remote port back to you, -D starts a SOCKS proxy",
      dict(s1="#e7e5e4", s2="#f5f5f4", s3="#fef3c7"),
      critter(fur=("#78716c", "#292524"), belly="#a8a29e", ears="none", hat="headlamp", nose_col="#f472b6",
              iris=("#1c1917", "#57534e"), mouth="grin", hand_col="#fbcfe8", prop=shovel),
      term("tunnels", ["$ ssh -L 8080:web-server:80 user@remote-host", ("  local port → through the tunnel", OK),
                       "$ ssh -R 8080:localhost:80 user@remote-host", ("  remote port → back to you", OK),
                       "$ ssh -D 1080 user@remote-server", ("  dynamic: a SOCKS proxy", OK)], size=17),
      "SSH tunnels: -L · -R · -D", "#57534e")
