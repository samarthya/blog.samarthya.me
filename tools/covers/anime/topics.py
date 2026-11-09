"""Anime covers for every remaining post that only had the generic topic tile (2026-11-09): Kubernetes, Elastic,
Containers, Go, Java, Streams, DevOps, Python, Security, Web & APIs, Notes and Agile.

Each cover is data: a character from CAST (a chibi animal or an anime kid), the prop it holds, a kicker pill, and a
panel with the post's real content (a terminal, a note card or a stack of steps), on a sky tinted with the topic's
colour from data/covers.yaml. Host names are neutral (node-1, master). A post gets `featureimage: "feature.png"`
in its front matter the first time its cover is written.

Run from the repo root:  python tools/covers/anime/topics.py [slug ...]   (no slugs = every cover below)
                         python tools/covers/anime/topics.py --topic kubernetes
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403
from kit import _esc  # noqa: E402

OK, DIM, WARN, KEY, CY = "#4ade80", "#94a3b8", "#f87171", "#fbbf24", "#67e8f9"

SKY = {  # topic: (sky top, middle, bottom, kicker fill)
    "kubernetes": ("#bfdbfe", "#dbeafe", "#eff6ff", "#1d4ed8"),
    "elastic": ("#99f6e4", "#ccfbf1", "#f0fdfa", "#0f766e"),
    "docker": ("#bae6fd", "#e0f2fe", "#f0f9ff", "#0369a1"),
    "golang": ("#a5f3fc", "#cffafe", "#ecfeff", "#0e7490"),
    "python": ("#fde68a", "#fef3c7", "#fffbeb", "#a16207"),
    "security": ("#fecaca", "#fee2e2", "#fef2f2", "#b91c1c"),
    "kafka": ("#cbd5e1", "#e2e8f0", "#f8fafc", "#334155"),
    "devops": ("#c7d2fe", "#e0e7ff", "#eef2ff", "#4338ca"),
    "java": ("#fed7aa", "#ffedd5", "#fff7ed", "#b45309"),
    "web": ("#a7f3d0", "#d1fae5", "#ecfdf5", "#047857"),
    "notes": ("#fed7aa", "#ffedd5", "#fff7ed", "#c2410c"),
    "agile": ("#ddd6fe", "#ede9fe", "#f5f3ff", "#6d28d9"),
}

# ---------------------------------------------------------------------------------------------------------------
# The cast. ("a", kwargs, description) is a critter(); ("k", kwargs, description) is a kid().
# ---------------------------------------------------------------------------------------------------------------
CAST = {
    "fox": ("a", dict(fur=("#fdba74", "#ea580c"), belly="#fff7ed", ears="pointy", ear_inner="#fff7ed", face="#fff7ed",
                      back=("tail_fluffy",), iris=("#7c2d12", "#f59e0b")), "an orange fox"),
    "cat": ("a", dict(fur=("#e5e7eb", "#9ca3af"), belly="#f9fafb", ears="pointy", ear_inner="#fbcfe8", back=("tail_curl",),
                      nose_col="#f472b6", iris=("#14532d", "#4ade80")), "a grey cat"),
    "blackcat": ("a", dict(fur=("#475569", "#0f172a"), belly="#64748b", ears="pointy", ear_inner="#f9a8d4", back=("tail_curl",),
                           nose_col="#f472b6", iris=("#854d0e", "#facc15")), "a black cat"),
    "panda": ("a", dict(fur=("#ffffff", "#e2e8f0"), belly="#f8fafc", ears="round", ear_inner="#1f2937", mask="meerkat",
                        iris=("#0f172a", "#475569")), "a panda"),
    "bear": ("a", dict(fur=("#b45309", "#78350f"), belly="#fde68a", ears="round", ear_inner="#fcd34d", face="#fde68a",
                       iris=("#1c1917", "#78716c")), "a brown bear"),
    "polar": ("a", dict(fur=("#f8fafc", "#cbd5e1"), belly="#ffffff", ears="round", ear_inner="#e2e8f0", face="#ffffff",
                        iris=("#1e3a8a", "#60a5fa")), "a polar bear"),
    "koala": ("a", dict(fur=("#cbd5e1", "#64748b"), belly="#f1f5f9", ears="round", ear_inner="#fbcfe8", nose_col="#334155",
                        iris=("#1e293b", "#64748b")), "a koala"),
    "rabbit": ("a", dict(fur=("#ffffff", "#d6d3d1"), belly="#fafaf9", ears="long", ear_inner="#fbcfe8", nose_col="#f472b6",
                         iris=("#831843", "#f472b6")), "a white rabbit"),
    "bunny": ("a", dict(fur=("#e7c9a0", "#a8835a"), belly="#fdf6ec", ears="long", ear_inner="#fed7aa", nose_col="#be185d",
                        iris=("#78350f", "#f59e0b")), "a brown bunny"),
    "owl": ("a", dict(fur=("#a16207", "#713f12"), belly="#fde68a", ears="tufts", mask="owl", snout="beak", back=("wings",),
                      iris=("#7c2d12", "#f59e0b"), beak_col=("#fcd34d", "#d97706")), "an owl"),
    "raccoon": ("a", dict(fur=("#a8a29e", "#57534e"), belly="#e7e5e4", ears="round", ear_inner="#d6d3d1", mask="raccoon",
                          back=("tail_stripes",), iris=("#1c1917", "#a8a29e")), "a raccoon"),
    "hedgehog": ("a", dict(fur=("#e7c9a0", "#b08356"), belly="#fef3c7", ears="small", back=("spikes",), face="#fef3c7",
                           iris=("#1c1917", "#78716c")), "a hedgehog"),
    "frog": ("a", dict(fur=("#86efac", "#16a34a"), belly="#ecfccb", ears="frog", snout="none", iris=("#713f12", "#facc15")), "a frog"),
    "turtle": ("a", dict(fur=("#bef264", "#65a30d"), belly="#fef9c3", ears="none", back=("shell",), iris=("#14532d", "#4ade80")), "a turtle"),
    "bat": ("a", dict(fur=("#a78bfa", "#5b21b6"), belly="#ede9fe", ears="bat", ear_inner="#f0abfc", back=("bat_wings",),
                      iris=("#831843", "#f472b6"), nose_col="#4c1d95"), "a purple bat"),
    "mouse": ("a", dict(fur=("#e5e7eb", "#9ca3af"), belly="#f9fafb", ears="round", ear_inner="#f9a8d4", nose_col="#f472b6",
                        iris=("#1e293b", "#475569")), "a grey mouse"),
    "dog": ("a", dict(fur=("#fde68a", "#d97706"), belly="#fffbeb", ears="floppy", face="#fef3c7", iris=("#451a03", "#a16207")), "a puppy"),
    "sloth": ("a", dict(fur=("#c8ad8d", "#7c5f3f"), belly="#ede0cf", ears="none", mask="sloth", iris=("#292524", "#78716c")), "a sloth"),
    "meerkat": ("a", dict(fur=("#e7c9a0", "#a8835a"), belly="#f5ebdc", ears="small", mask="meerkat", iris=("#1c1917", "#78716c")), "a meerkat"),
    "penguin": ("a", dict(fur=("#334155", "#0f172a"), belly="#f8fafc", ears="none", mask="puffin", snout="beak", back=("wings",),
                          iris=("#0f172a", "#38bdf8"), beak_col=("#fdba74", "#f97316")), "a penguin"),
    "duck": ("a", dict(fur=("#fde047", "#eab308"), belly="#fef9c3", ears="none", snout="bill", back=("wings", "tuft"),
                       iris=("#1e293b", "#475569"), beak_col=("#fdba74", "#f97316")), "a yellow duck"),
    "chick": ("a", dict(fur=("#fef08a", "#facc15"), belly="#fefce8", ears="none", snout="beak", back=("wings", "tuft"),
                        iris=("#1e293b", "#475569"), beak_col=("#fdba74", "#ea580c")), "a chick"),
    "tiger": ("a", dict(fur=("#fb923c", "#c2410c"), belly="#fff7ed", ears="small", face="#fff7ed", back=("tail_stripes",),
                        iris=("#14532d", "#84cc16")), "a tiger cub"),
    "hamster": ("a", dict(fur=("#fcd9a8", "#d69e5c"), belly="#fff7ed", ears="small", face="#fff7ed", nose_col="#f472b6",
                          iris=("#1c1917", "#57534e")), "a hamster"),
    "pig": ("a", dict(fur=("#fbcfe8", "#f472b6"), belly="#fce7f3", ears="small", nose_col="#db2777", iris=("#1e293b", "#475569")), "a piglet"),
    "monkey": ("a", dict(fur=("#a16207", "#713f12"), belly="#fde68a", ears="round", ear_inner="#fde68a", face="#fde68a",
                         back=("tail_curl",), iris=("#1c1917", "#78716c")), "a monkey"),
    "otter": ("a", dict(fur=("#a8743f", "#6b4423"), belly="#f5e6d3", ears="small", face="#f5e6d3", iris=("#1c1917", "#78716c")), "an otter"),
    "lamb": ("a", dict(fur=("#ffffff", "#e7e5e4"), belly="#fafaf9", ears="small", face="#fce7f3", back=("tuft",),
                       nose_col="#f472b6", iris=("#1e293b", "#64748b")), "a lamb"),
    "deer": ("a", dict(fur=("#d6a06b", "#a16207"), belly="#fef3c7", ears="pointy", ear_inner="#fde68a", face="#fef3c7",
                       iris=("#451a03", "#b45309")), "a fawn"),
    "mole": ("a", dict(fur=("#78716c", "#292524"), belly="#a8a29e", ears="none", nose_col="#f472b6", iris=("#1c1917", "#57534e")), "a mole"),
    "seal": ("a", dict(fur=("#cbd5e1", "#94a3b8"), belly="#f1f5f9", ears="none", iris=("#0f172a", "#334155")), "a seal pup"),
    "redpanda": ("a", dict(fur=("#f97316", "#9a3412"), belly="#7c2d12", ears="pointy", ear_inner="#ffffff", face="#fff7ed",
                           back=("tail_stripes",), tail_col="#c2410c", iris=("#1c1917", "#57534e")), "a red panda"),
    "lion": ("a", dict(fur=("#fcd34d", "#d97706"), belly="#fef3c7", ears="round", ear_inner="#fde68a", face="#fef3c7",
                       back=("spikes",), iris=("#451a03", "#b45309")), "a lion cub"),
    # kids
    "boy": ("k", dict(), "a boy with spiky dark hair in a blue hoodie"),
    "redgirl": ("k", dict(hair=("#fb7185", "#be123c"), style="soft", back="pigtails", outfit=("#fde68a", "#d97706"), acc="#facc15",
                          iris=("#9f1239", "#fb7185"), mouth="smile"), "a girl with pink pigtails"),
    "tealgirl": ("k", dict(hair=("#2dd4bf", "#0f766e"), style="soft", back="long", outfit=("#c4b5fd", "#7c3aed"), acc="#f43f5e",
                           iris=("#0e7490", "#67e8f9"), mouth="smile"), "a girl with long teal hair"),
    "blondboy": ("k", dict(hair=("#fde68a", "#ca8a04"), style="swept", outfit=("#86efac", "#15803d"), iris=("#1e3a8a", "#60a5fa")),
                 "a blond boy in a green jacket"),
    "purplegirl": ("k", dict(hair=("#c084fc", "#6b21a8"), style="soft", back="ponytail", outfit=("#7dd3fc", "#0284c7"), acc="#facc15",
                             iris=("#581c87", "#c084fc"), mouth="open"), "a girl with a purple ponytail"),
    "curlyboy": ("k", dict(hair=("#92400e", "#451a03"), style="curly", outfit=("#fca5a5", "#dc2626"), iris=("#14532d", "#4ade80")),
                 "a boy with curly brown hair"),
    "silvergirl": ("k", dict(hair=("#e2e8f0", "#94a3b8"), style="soft", back="bob", outfit=("#475569", "#0f172a"), acc="#a78bfa",
                             iris=("#4c1d95", "#a78bfa"), mouth="smile"), "a girl with a silver bob"),
    "bungirl": ("k", dict(hair=("#1f2937", "#030712"), style="soft", back="buns", outfit=("#f9a8d4", "#db2777"), acc="#8b5cf6",
                          iris=("#7c2d12", "#f59e0b"), mouth="open"), "a girl with dark hair in buns"),
    "gingerboy": ("k", dict(hair=("#fb923c", "#c2410c"), style="spiky", outfit=("#a5b4fc", "#4338ca"), iris=("#14532d", "#22c55e")),
                  "a boy with spiky ginger hair"),
    "blueboy": ("k", dict(hair=("#60a5fa", "#1d4ed8"), style="swept", outfit=("#fef3c7", "#d97706"), glasses=True, mouth="smile",
                          iris=("#1e3a8a", "#38bdf8")), "a boy with blue hair and glasses"),
    "greengirl": ("k", dict(hair=("#86efac", "#15803d"), style="curly", back="long", outfit=("#fecaca", "#ef4444"), acc="#facc15",
                            iris=("#14532d", "#4ade80"), mouth="grin"), "a girl with long green curls"),
    "navyboy": ("k", dict(hair=("#1e3a8a", "#172554"), style="soft", outfit=("#e2e8f0", "#94a3b8"), iris=("#7c2d12", "#f59e0b")),
                "a boy with navy hair in a grey jacket"),
    "brownboy": ("k", dict(hair=("#57534e", "#1c1917"), style="swept", outfit=("#fdba74", "#c2410c"), skin=("#e8b68f", "#c98b5e"),
                           iris=("#451a03", "#a16207")), "a boy with swept dark hair"),
    "inkgirl": ("k", dict(hair=("#334155", "#020617"), style="soft", back="long", outfit=("#99f6e4", "#0d9488"), skin=("#e8b68f", "#c98b5e"),
                          acc="#f97316", iris=("#451a03", "#b45309"), mouth="smile"), "a girl with long black hair"),
}

PROP_WORD = {"wheel": "a ship's wheel", "box": "a parcel", "key": "a key", "shield": "a shield", "lens": "a magnifying glass",
             "wrench": "a wrench", "bulb": "a light bulb", "flag": "a flag", "mug": "a mug", "scroll": "a scroll", "book": "a book",
             "lantern": "a lantern", "balloon": "a balloon", "wand": "a magic wand", "pencil": "a pencil", "padlock": "a padlock",
             "telescope": "a telescope", "envelope": "an envelope", "plug": "a plug", "sign": "a sign"}

HAT_WORD = {"tophat": "a top hat", "beret": "a beret", "crown": "a crown", "goggles": "goggles", "headlamp": "a head lamp",
            "grad_cap": "a graduation cap", "nightcap": "a night cap", "bow": "a bow", "cap": "a cap", "beanie": "a beanie",
            "headset": "a headset", "hardhat": "a hard hat", "wizard": "a wizard hat", "headband": "a headband", "flower": "a flower"}


# ---------------------------------------------------------------------------------------------------------------
# Panels (right half). Each returns (svg, height, words for the alt text).
# ---------------------------------------------------------------------------------------------------------------
def T(title, lines):
    return ("term", title, lines)


def N(title, lines):
    return ("note", title, lines)


def S(title, rows):
    return ("steps", title, rows)


def _term(title, lines, y):
    longest = max((len(l if isinstance(l, str) else l[0]) for l in lines), default=1)
    size = 19 if longest <= 46 else max(14, int(19 * 46 / longest))
    gap = 31 if len(lines) <= 9 else 28
    h = 92 + len(lines) * gap - (gap - 31 if gap != 31 else 0)
    return terminal(600, y, 560, h, title, lines, size=size, gap=gap), h


def _note(title, lines, y):
    h = 84 + len(lines) * 40
    body = "".join(f'<text x="626" y="{y + 100 + i * 40}" font-family="{SANS}" font-size="23" font-weight="600" '
                   f'fill="{INK if not isinstance(l, tuple) else l[1]}">{_esc(l if isinstance(l, str) else l[0])}</text>'
                   for i, l in enumerate(lines))
    return card(600, y, 560, h, _esc(title), body=body), h


def _steps(title, rows, y, accent):
    cols = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#06b6d4", "#6366f1", "#a855f7", "#ec4899"]
    out = [f'<text x="604" y="{y + 26}" font-family="{SANS}" font-size="22" font-weight="800" fill="{accent}">{_esc(title)}</text>']
    ry = y + 44
    for i, (name, sub) in enumerate(rows):
        c = cols[(i * 2) % len(cols)] if len(rows) <= 4 else cols[i % len(cols)]
        out.append(f'''
  <g filter="url(#drop)">
    <rect x="600" y="{ry}" width="560" height="58" rx="14" fill="#ffffff"/>
    <rect x="600" y="{ry}" width="14" height="58" rx="7" fill="{c}"/>
    <text x="630" y="{ry + 37}" font-family="{SANS}" font-size="22" font-weight="800" fill="{INK}">{_esc(name)}</text>
    <text x="1142" y="{ry + 37}" text-anchor="end" font-family="{MONO}" font-size="18" font-weight="700" fill="{c}">{_esc(sub)}</text>
  </g>''')
        ry += 68
    return "".join(out), ry - y


def chips_row(chips, y, fill):
    x, out = 600, []
    for c in chips:
        w = int(len(c) * 18 * 0.62) + 36
        if x + w > 1165:
            x, y = 600, y + 54
        out.append(pill(x, y, c, fill, size=18, w=w, mono=True))
        x += w + 12
    return "".join(out)


# ---------------------------------------------------------------------------------------------------------------
def wire(slug):
    """Point the post at feature.png (first time only)."""
    p = REPO / "content" / "posts" / slug / "index.md"
    t = p.read_text(encoding="utf-8")
    head, sep, rest = t.partition("\n---")
    if re.search(r"^featureimage:", head, re.M):
        return
    head = re.sub(r"^(title:.*)$", r'\1\nfeatureimage: "feature.png"', head, count=1, flags=re.M)
    p.write_text(head + sep + rest, encoding="utf-8")


COVERS = []


def C(slug, topic, who, prop_, kicker, panel, chips=(), hat=None, **over):
    COVERS.append((slug, topic, who, prop_, kicker, panel, chips, hat, over))


def render(entry):
    slug, topic, who, prop_, kicker, panel, chips, hat, over = entry
    s1, s2, s3, accent = SKY[topic]
    kind, kw, desc = CAST[who]
    pk, pcol, plabel = (prop_ + (None, None))[:3] if isinstance(prop_, tuple) else (prop_, None, None)
    held = prop(pk, pcol or accent, plabel or "") if pk else ""
    kw = dict(kw, **over)
    if hat:
        kw["hat"] = hat
    figure = critter(prop=held, **kw) if kind == "a" else kid(prop=held, **kw)
    ptype, ptitle, pdata = panel
    y = 150
    if ptype == "term":
        psvg, h = _term(ptitle, pdata, y)
        what = f"a terminal titled {ptitle} showing " + "; ".join(
            (l if isinstance(l, str) else l[0]).lstrip("$ ").strip() for l in pdata if (l if isinstance(l, str) else l[0]).strip())[:200]
    elif ptype == "note":
        psvg, h = _note(ptitle, pdata, y)
        what = f"a note card, {ptitle}: " + "; ".join(l if isinstance(l, str) else l[0] for l in pdata)[:200]
    else:
        psvg, h = _steps(ptitle, pdata, y - 10, accent)
        what = f"{ptitle}: " + ", ".join(f"{a} ({b})" for a, b in pdata)[:200]
    extra = chips_row(chips, y + h + 22, accent) if chips else ""
    wear = f" wearing {HAT_WORD[kw['hat']]}" if kw.get("hat") else ""
    hold = f" holding {PROP_WORD[pk]}" + (f" marked {plabel}" if plabel else "") if pk else ""
    alt = f"Anime illustration: {desc}{wear}{hold}, beside {what}"
    body = psvg + extra + pill(600, 66, kicker, accent, size=21) + figure + sparkles(((40, 70, 24), (560, 40, 18), (1165, 600, 22)))
    write(slug, _esc(alt), dict(s1=s1, s2=s2, s3=s3), body, only=[slug])
    wire(slug)


# =================================================================================================================
# Kubernetes
# =================================================================================================================
C("adding-node-to-a-cluster", "kubernetes", "bear", ("box", "#2563eb", "node"), "K8s: adding a node to a cluster",
  T("master", ["$ kubeadm join master:6443 \\", "    --token <token> --discovery-token-ca-cert-hash …",
               "$ k get nodes", ("NAME     STATUS   ROLES    AGE", DIM), ("node-1   Ready    <none>   22h", OK),
               ("node-2   Ready    <none>   41d", OK), ("node-3   Ready    <none>   131d", OK)]),
  chips=["docker", "kubeadm", "kubelet"], hat="hardhat")
C("configmaps-k8s-2", "kubernetes", "rabbit", "scroll", "ConfigMaps: mounted as a file",
  T("happy-faces.yaml", ["apiVersion: v1", "kind: ConfigMap", "metadata:", "  name: happy-faces-mnt", "data:",
                         "  data.values: |-", ("# mounted into happy-pod as a volume", DIM)]))
C("controller-manager-unhealthy", "kubernetes", "koala", "lens", "controller-manager: #Unhealthy",
  T("master", ["$ k get cs", ("NAME                 STATUS", DIM), ("controller-manager   Unhealthy", WARN),
               ("scheduler            Unhealthy", WARN), ("etcd-0               Healthy", OK), "",
               "$ vi /etc/kubernetes/manifests/ \\", "     kube-controller-manager.yaml",
               ("    #- --port=0   <- commented", KEY)]))
C("deployments-k8s", "kubernetes", "boy", ("flag", None, "x3"), "Deployments: scale it out",
  T("deployment.yaml", ["--- # Pod deployment", "apiVersion: apps/v1", "kind: Deployment", "metadata:",
                        "  name: go-server-deployment", "",
                        "$ k scale deployment/go-server-deployment \\", "    --replicas=3"]))
C("docker-network", "kubernetes", "chick", ("plug", "#2563eb", "net"), "Docker network: learn by example",
  T("docker network", ["$ docker network COMMAND", ("  connect     Connect a container", KEY), ("  create      Create a network", KEY),
                       ("  disconnect  Disconnect a container", KEY), ("  inspect     Display details", KEY),
                       ("  ls          List networks", KEY), ("  rm          Remove networks", KEY)]))
C("helm-charts-packaging", "kubernetes", "navyboy", "wheel", "Helm: charts, config, releases",
  S("Helm, in three ideas", [("chart", "the bundle"), ("config", "values merged in"), ("release", "chart + config, running"),
                             ("Chart.yml", "helm v3.2.4")]), hat="cap", acc="#1d4ed8")
C("helm-install", "kubernetes", "penguin", "wheel", "Helm install on Ubuntu",
  T("ubuntu", ["$ cat /etc/issue", ("Ubuntu 18.04.2 LTS \\n \\l", DIM),
               "$ curl https://storage.googleapis.com/ \\", "    kubernetes-helm/helm-v2.12.3-linux-amd64.tar.gz"]))
C("helpful-links-for-k8s", "kubernetes", "owl", ("book", "#1d4ed8", "API"), "Helpful links for K8s",
  S("three bookmarks", [("API overview", "the YAML, v1.18"), ("Concepts", "kubernetes.io/docs"), ("Glossary", "quick navigation")]))
C("installing-k8s-on-ubuntu", "kubernetes", "redgirl", "wrench", "Installing K8s on Ubuntu",
  T("ubuntu 18.04.4", ["$ cat /etc/issue", ("Ubuntu 18.04.4 LTS", DIM), "$ sudo apt-get install -y docker-ce",
                       "$ sudo apt-get install -y kubelet kubeadm kubectl", "$ sudo kubeadm init \\",
                       "    --pod-network-cidr=10.244.0.0/16", ("Your control-plane has initialized!", OK)]), hat="hardhat")
C("jenkins-k8s", "kubernetes", "dog", "wheel", "Jenkins on Kubernetes, with Helm",
  T("helm", ["$ helm repo add jenkins https://charts.jenkins.io", "$ helm repo update",
             "$ helm upgrade --install myjenkins \\", "    jenkins/jenkins -n jenkins --create-namespace"]),
  chips=["helm", "jenkins", "namespace"], hat="tophat")
C("k8s", "kubernetes", "tealgirl", "wheel", "K8s: what it is",
  T("nginx.yaml", ["apiVersion: apps/v1", "kind: Deployment", "metadata:", "  name: nginx", "spec:      # the desired state",
                   "status:    # the current state"]), chips=["declarative", "resilient", "open source"])
C("k8s-rbac", "kubernetes", "tiger", ("shield", None, "RBAC"), "K8s RBAC: who can do what",
  S("four API objects", [("Role", "one namespace"), ("ClusterRole", "cluster-wide"), ("RoleBinding", "grants a Role"),
                         ("ClusterRoleBinding", "grants cluster-wide")]), chips=["rbac.authorization.k8s.io", "permissions add up"])
C("kubelab", "kubernetes", "monkey", "lens", "KubeLab: poking at the API",
  T("lab", ["$ kubectl version", ("Client Version: v1.13", DIM), "$ kubectl api-resources",
            ("NAME                SHORTNAMES", DIM), "bindings", "componentstatuses   cs", "configmaps          cm", "endpoints           ep"]))
C("metric-server", "kubernetes", "hamster", "lens", "Metrics Server: k top node",
  T("metrics-server", ["$ k top node", ("Error from server (ServiceUnavailable)", WARN),
                       ("(get nodes.metrics.k8s.io)", WARN), "$ kubectl apply -f …/metrics-server/…",
                       ("serviceaccount/metrics-server configured", OK), "$ k top node",
                       ("NAME     CPU(cores)  CPU%  MEMORY%", DIM), ("node-1   131m        0%    21%", OK),
                       ("node-4   395m        2%    22%", OK)]))
C("multicontainer-k8s", "kubernetes", "purplegirl", ("box", "#2563eb", "pod"), "MultiContainer: a Pod's lifecycle",
  T("my-pod", ["$ k run myepserver --image samarthya/epserver:2.0 \\", "    --env SERVERPORT=9090 \\",
               "    --dry-run=client -o yaml", "apiVersion: v1", "kind: Pod", "metadata:", "  labels:", "    app: my-pod"]))
C("network-com", "kubernetes", "bat", "envelope", "Network communication: transport",
  S("transport protocols", [("TCP", "reliable, ordered"), ("UDP", "fast, no handshake"), ("Ports", "which app"), ("OSI", "layer 4")]))
C("network-policy-restrictions", "kubernetes", "hedgehog", "shield", "Network policy: deny by default",
  T("np-demo", ["$ kubectl run --namespace=np-demo nginx \\", "    --replicas=2 --image=nginx", "kind: NetworkPolicy",
                "apiVersion: networking.k8s.io/v1", "metadata:", "  name: default-deny", "  namespace: np-demo", "spec:",
                "  podSelector: {}"]))
C("networkpolicy-k8s", "kubernetes", "turtle", "shield", "NetworkPolicy: ingress and egress",
  T("my-network-policy.yaml", ["apiVersion: networking.k8s.io/v1", "kind: NetworkPolicy", "metadata:", "  name: my-network-policy",
                               "spec:", "  podSelector: …", "  policyTypes:", "  - Ingress", "  - Egress"]))
C("playground-k8s", "kubernetes", "blondboy", ("sign", "#2563eb", "label"), "Playground: labels and annotations",
  T("docker-desktop", ["$ k get nodes", ("docker-desktop   Ready,SchedulingDisabled", KEY),
                       "$ k label node docker-desktop nodeName=docker-node", ("node/docker-desktop labeled", OK),
                       "$ k annotate pods nginx-node \\", "    description='My nginx-node on a node'", ("pod/nginx-node annotated", OK)]))
C("pod-volume-k8s", "kubernetes", "seal", ("box", "#2563eb", "PV"), "Pod & volume: Redis keeps its data",
  T("redis.yaml", ["$ k apply -f redis.yaml", ("pod/redispod created", OK), ("persistentvolume/redis-pv created", OK),
                   ("persistentvolumeclaim/redisdb-pvc created", OK)]), chips=["Pod", "PersistentVolume", "PVC"])
C("probes-k8s", "kubernetes", "silvergirl", "lens", "Probes: is it alive, is it ready?",
  T("pod-bbox-lp", ["--- # Liveness Probe example", "livenessProbe:", "  exec:", "    command:", "    - cat", "    - /tmp/healthy",
                    "$ k get pods", ("pod-bbox-lp   0/1   ContainerCreating", KEY)]),
  chips=["liveness", "readiness", "startup"], hat="headset")
C("pv-pvc", "kubernetes", "mole", ("box", "#2563eb", "PVC"), "PV & PVC: storage, claimed",
  T("storageclass.yaml", ["apiVersion: storage.k8s.io/v1", "kind: StorageClass", "metadata:", "  name: esdatadir",
                          "provisioner: kubernetes.io/no-provisioner", "volumeBindingMode: WaitForFirstConsumer"]))
C("quick-cheat-sheet", "kubernetes", "gingerboy", "scroll", "Cheat sheet: install a K8s cluster",
  S("six steps", [("Check the OS", "lsb_release -a"), ("Docker GPG key", "apt-key add"), ("Docker repo", "add-apt-repository"),
                  ("K8s GPG + repo", "kubernetes-xenial"), ("Update", "apt-get update"), ("Install + hold", "kubeadm kubectl")]))
C("secrets", "kubernetes", "raccoon", "key", "Secrets: three kinds",
  T("k create secret", ["$ k create secret --help", ("  docker-registry  for a Docker registry", KEY),
                        ("  generic          from a file or literal", KEY), ("  tls              a TLS secret", KEY), "",
                        "$ k create secret generic my-secret \\", "    --from-file=path/to/bar"]))
C("serviceaccount", "kubernetes", "cat", ("sign", "#2563eb", "SA"), "ServiceAccount: who a Pod is",
  T("default", [("Error: INSTALLATION FAILED: rendered", WARN), ("manifests contain a resource that…", WARN), "",
                "apiVersion: v1", "kind: ServiceAccount", "metadata:", "  name: default", "  namespace: default"]))
C("services-k8s", "kubernetes", "fox", ("plug", "#2563eb", "svc"), "Services: a stable door to Pods",
  T("nginx-pod", ["kind: Pod", "metadata:", "  name: nginx-pod", "  labels:", "    app: my-pod", "---", "kind: Service",
                  "  selector:", "    app: my-pod"]))
C("taint-nodes", "kubernetes", "deer", ("sign", "#2563eb", "NoSchedule"), "Taint nodes: keep pods off",
  T("taints", ["$ k taint node node-3 node-type=prod:NoSchedule", "", "kind: Deployment",
               "metadata:", "  name: my-prod", "spec:", "  replicas: 1", ("# a toleration lets my-prod land", DIM)]))
C("upgrading-k8s-cluster", "kubernetes", "curlyboy", "wrench", "Upgrading a K8s cluster",
  T("master", ["$ kubeadm upgrade plan", "$ k drain node-1 --ignore-daemonsets", ("node/node-1 drained", OK),
               "$ kubeadm upgrade node", "$ systemctl restart kubelet", "$ k uncordon node-1", ("node/node-1 uncordoned", OK)]),
  hat="hardhat", acc="#1d4ed8")
C("writing-charts", "kubernetes", "bungirl", "wand", "Writing Helm charts",
  T("templates/", ["{{/* a comment */}}", "{{- if .Values.serviceAccount.create }}", "kind: ServiceAccount",
                   "  annotations:", "  {{- toYaml .Values.serviceAccount.annotations }}", "{{- end }}",
                   "app: {{ .Values.appname }}"]), hat="wizard")

# =================================================================================================================
# Elastic
# =================================================================================================================
C("_reindex-_update_by_query-_delete_by_query", "elastic", "otter", ("box", None, "docs"), "Elasticsearch: three bulk APIs",
  S("copy, change, remove", [("_reindex", "index to index"), ("_update_by_query", "in place"), ("_delete_by_query", "matching docs")]))
C("aggregations-elastic", "elastic", "bunny", "lens", "Aggregations: metrics from many docs",
  T("Dev Tools", ["GET network_sample/_search", "{", '  "size": 0,', '  "aggs": {', '    "agg_count": {', '      "max": { … }',
                  "    } } }", ('"took" : 3067,', DIM), ('"_shards" : { "total" : 3, "successful" : 3 }', OK)]))
C("analyze-_analyze-api", "elastic", "blueboy", "lens", "The _analyze API: text to tokens",
  T("Dev Tools", ["GET _analyze", "{", '  "text": "My simple text!",', '  "explain": true', "}",
                  ('"analyzer" : { "name" : "standard",', DIM), ('  "tokens" : [ my, simple, text ]', OK)]),
  chips=["whitespace", "stop", "keyword", "english"])
C("api-_reindex", "elastic", "duck", ("box", None, "19"), "API _reindex: copy an index",
  T("Dev Tools", ["POST _reindex", "{", '  "source": { "index": "source-index" },', '  "dest":   { "index": … }', "}",
                  ('"total" : 19,', DIM), ('"updated" : 0,', DIM), ('"created" : 19', OK)]))
C("cluster-elastic-7-3", "elastic", "penguin", "flag", "A three-node Elastic 7.3 cluster",
  T("Dev Tools", ["GET _cat/nodes", ("… dim * node1", OK), ("… dim - node2", OK), ("… dim - node3", OK), "", "PUT myindex1",
                  ('"acknowledged" : true,', OK), ('"shards_acknowledged" : true', OK)]))
C("ecs-elastic-common-schema", "elastic", "tealgirl", ("book", None, "ECS"), "ECS: one schema for every source",
  S("field sets", [("Base", "@timestamp, tags"), ("Agent", "e.g. FileBeat"), ("Error", "error.code"), ("Event", "context"),
                   ("Host", "where it ran")]))
C("elastic-cluster-api", "elastic", "meerkat", "lens", "Cluster settings: monitoring",
  T("Dev Tools", ["GET _cluster/settings", '"persistent" : {', '  "xpack" : { "monitoring" : {', '    "collection" : {',
                  '      "enabled" : "true"', "    } } }", ("# monitoring is XPack only", DIM)]))
C("elasticsearch-v7-6", "elastic", "polar", "lens", "Elasticsearch 7.6: first questions",
  T("Dev Tools", ["GET _cat/health?v", ("status       yellow", KEY), ("node.total   4", DIM), ("node.data    4", DIM),
                  "GET profile/_search", ('"type" : "index_not_found_exception"', WARN), ('"reason" : "no such index [profile]"', WARN)]))
C("elasticsearch-v7-6-2", "elastic", "redgirl", "lens", "Elasticsearch 7.6: queries",
  T("profile/_search", ["GET profile/_search", "{", '  "query": {', '    "match": {', '      "title": "Mr. Ms."', "    }", "  }", "}"]),
  chips=["match_phrase", "bool", "aggregations"])
C("elastic-7-5", "elastic", "seal", ("box", None, "7.5"), "Elastic 7.5: install with Docker",
  T("install", ["$ yum install docker", "$ docker pull \\", "    docker.elastic.co/elasticsearch/elasticsearch:7.5.1"]))
C("fortune-v1-0", "elastic", "cat", "wand", "Fortune v1.0: a fortune teller in Java",
  T("FortuneTeller.java", ["public class FortuneTeller {", "  private List<String> allData =", "      new LinkedList<String>();",
                           "  public FortuneTeller(File dbFile) { … }", "  public void populateDB(File localFile) { … }", "}"]),
  chips=["Fortune.DB", "JUnit"], hat="beret")
C("journalctl-query-the-systemd-journal", "elastic", "sloth", "lantern", "journalctl: query the systemd journal",
  T("journal", ["$ systemctl list-units --show-types | grep kubelet", ("kubelet.service  loaded active running", OK),
                "$ journalctl -u kubelet"]))
C("painless-scripting", "elastic", "lamb", "pencil", "Painless scripting",
  N("Painless is", ["simple", "secure", "made for Elasticsearch", ("the guide, for version 7.4", DIM)]))
C("performance-tweaks-kibana", "elastic", "gingerboy", "wrench", "Kibana behind nginx, with SSL",
  T("nginx.repo", ["[nginx-stable]", "name=nginx stable repo", "baseurl=http://nginx.org/packages/centos/…", "gpgcheck=1", "enabled=1",
                   "$ nginx -v", ("nginx version: nginx/1.19.1", OK)]), chips=["nginx", "SSL", "Kibana"])
C("text-elastic", "elastic", "koala", "scroll", "text vs keyword",
  T("my_index", ["POST my_index/_doc/1", '{ "country_name":', '    "The United States of America" }', "GET my_index/_mapping",
                 ('"type" : "text",', OK), ('"fields" : { "keyword" : …', OK)]), chips=["text", "keyword", "multi-fields"])

# =================================================================================================================
# Containers
# =================================================================================================================
C("buildah-https-buildah-io", "docker", "otter", "box", "Buildah: images without a daemon",
  T("buildah", ["$ sudo apt-get install buildah", "$ buildah from centos"]))
C("clusterrole-refresher", "docker", "lion", ("shield", "#0369a1", "RBAC"), "ClusterRole: a refresher",
  T("clusterrole", ["$ k create clusterrole myclusterrole \\", "    --verb=get,list,watch --resource=persistentvolumes", "{",
                    '  "kind": "ClusterRole",', '  "apiVersion": "rbac.authorization.k8s.io/v1",', '  "metadata": {',
                    '    "name": "myclusterrole"', "} }"]))
C("docker-clean-in-bulk", "docker", "pig", "bulb", "Docker: clean up in bulk",
  T("docker", ["$ docker system prune -f", "$ docker image ls my-registry/my-connector", ("# a long listing", DIM),
               "$ docker rmi -f `docker image ls \\", "    my-registry/my-connector -q`", ("Untagged … Deleted …", OK)]))
C("docker-registry", "docker", "redpanda", ("box", "#0369a1", "5000"), "Run your own Docker registry",
  T("registry", ["$ docker run -d -p 5000:5000 \\", "    --restart=always --name registry registry:latest",
                 "$ docker tag ubuntu registry.example:5000/ubuntu:latest", "$ docker push registry.example:5000/ubuntu:latest"]))
C("docker-ubuntu-a-refresher", "docker", "brownboy", "box", "Docker on Ubuntu: a refresher",
  T("ubuntu 18.04.4", ["$ cat /etc/issue", ("Ubuntu 18.04.4 LTS", DIM), "$ sudo apt-get update", "$ sudo apt-get -y install \\",
                       "    apt-transport-https ca-certificates curl", "$ docker version"]), chips=["--init", "layers", "flattening"])
C("dockerfile", "docker", "chick", "scroll", "Dockerfile: hello world",
  T("Dockerfile", ["# Lesson 1 - Using basic Dockerfile", "FROM alpine:3.7", 'CMD ["echo","Hello world!"]', "",
                   ("# INSTRUCTION arguments", DIM)]))
C("dockerizd-service", "docker", "hamster", ("box", "#0369a1", "go"), "A Go service, Dockerised",
  T("Dockerfile", ["# Building the container image", "ARG VERSION=alpine", "# Sets the base image", "FROM golang:${VERSION} AS baseimage",
                   "RUN echo 'Building image...'"]), chips=["multi-stage", "golang:alpine"])
C("shared-volume", "docker", "frog", ("box", "#0369a1", "vol"), "Shared volumes",
  T("docker volume", ["$ docker volume ls", ("DRIVER    VOLUME NAME", DIM), ("local     c9ad85b13e22…", OK), "$ docker volume",
                      ("  create    Create a volume", KEY), ("  inspect   Display detailed information", KEY)]),
  chips=["--mount", "-v / --volume"])
C("storage-drivers", "docker", "mole", "box", "Storage drivers",
  T("docker", ["$ docker run --name hello hello-world", ("Hello from Docker!", OK), "$ docker info", ("Storage Driver: overlay2", KEY)]))
C("vagrant-osx-m1", "docker", "greengirl", "box", "Vagrant on an M1 Mac",
  T("vagrant", ["$ vagrant version", ("Installed Version: 2.3.0", DIM), ("Latest Version: 2.3.0", DIM), "$ vagrant init",
                ("A `Vagrantfile` has been placed in", OK), ("this directory.", OK)]))
C("vagrant-osx-m1-2", "docker", "inkgirl", "plug", "Vagrant with the Docker provider",
  T("vagrant up", ["$ vagrant up --provider=docker", ("Bringing machine 'default' up with", DIM), ("'docker' provider...", DIM),
                   ("==> default: Creating and configuring", OK), ("    docker networks...", OK), "$ docker ps -a"]))

# =================================================================================================================
# Go
# =================================================================================================================
C("concurrency-golang", "golang", "bunny", "lens", "Go concurrency: counting letters in parallel",
  T("letter.go", ["package letter", 'import "sync"', "type FreqMap map[rune]int", "type SafeMap struct {", "    val  FreqMap",
                  "    lock sync.Mutex", "}"]), chips=["goroutines", "sync.Mutex", "ParallelFreq"])
C("documenting-go", "golang", "owl", ("book", "#0e7490", "godoc"), "Documenting Go", hat="grad_cap",
  panel=N("GoDoc", ["“Godoc comments are just good", "comments, the sort you would want", "to read even if godoc didn’t exist.”",
                    ("— the Go blog", DIM)]))
C("files-golang", "golang", "otter", "scroll", "Files in Go: reading",
  T("files.go", ["package files", "import (", '    "bufio"', '    "fmt"', '    "io"', '    "log"', ")"]))
C("files-golang-2", "golang", "lamb", "scroll", "Files in Go: stats and content",
  T("sample.txt", ["I am just a plain text file", "I have float, int, bool and string", ("int: 20", KEY), ("float: 20.50", KEY),
                   ('string: "Get some content"', KEY), ("bool: true", KEY)]))
C("go-helpful-links", "golang", "meerkat", "telescope", "Go: helpful links",
  S("bookmarks", [("Effective Go", "golang.org/doc"), ("Specification", "ref/spec"), ("http package", "pkg/net/http"),
                  ("Using Go modules", "the Go blog")]))
C("go-modules", "golang", "frog", ("box", "#0e7490", "mod"), "Go modules: GO111MODULE",
  T("go env", [("package src is not in GOROOT", WARN), "$ go env | grep GO111", ('GO111MODULE=""', KEY), "$ go env -w GO111MODULE=auto"]))
C("golang-command-line-arguments", "golang", "chick", "flag", "Go: command-line arguments",
  T("main.go", ["func main() {", "  if len(os.Args) > 0 {", '    fmt.Println(" More than one argument found: "', "      + fmt.Sprintf(\"%s\", os.Args[1:]))",
                "  }", "}", "$ go run main 1 2 3 4", ("More than one argument found: [1 2 3 4]", OK)]))
C("golang-encoding", "golang", "panda", "envelope", "Go: encoding with gob",
  T("enc", ['import "encoding/gob"', "$ ./main -f abc.txt", (" Read:  Blog: My first blog", OK), (" Category: technical", OK),
            (" Length: 200", OK), (" --- End Program --", DIM)]))
C("golang-hex-output", "golang", "blueboy", "lens", "Go: a hex dump",
  T("hex.go", ["var fileName string", "func init() {", '  flag.StringVar(&fileName, "f", "", "File to read")', "  flag.Parse()", "}",
               "b, err := fr.ReadByte()", ('-------- STARTOFFILE -------', DIM)]))
C("golang-program-banner", "golang", "dog", ("sign", "#0e7490", "banner"), "Go: a program banner with flags",
  T("cmd", ['var times = flag.Int("n", 1, …)', 'var msg = flag.String("m", "", …)', 'var dbg = flag.Bool("d", false, …)',
            "$ go build src/cmdline/cmd.go", '$ ./cmd -n 2 -m="Why is world round?"']))
C("golang-proteins-rna", "golang", "silvergirl", "lens", "Go: proteins from RNA",
  T("protein.go", ['RNA:     "AUGUUUUCU"', 'Codons:  "AUG", "UUU", "UCU"', ('Protein: "Methionine", "Phenylalanine",', OK),
                   ('         "Serine"', OK), "", 'case "AUG":', '    return "Methionine", nil']), glasses=False)
C("golang-reflection", "golang", "rabbit", "lens", "Go: reflection",
  T("reflect", ["func main() {", "  i := 0", "  fmt.Println(reflect.TypeOf(i))", "  fmt.Println(reflect.ValueOf(i))", "}",
                ("int", OK), ("0", OK)]))
C("golang-try-catch", "golang", "tiger", "shield", "Go has no try-catch: panic and recover",
  T("errors.go", ["func throwError() (string, error) {", '  return "", fmt.Errorf("I am an simple error")', "}", "defer func() {",
                  "  if r := recover(); r != nil { … }", "}()"]))
C("house-that-jack-built", "golang", "mouse", "book", "The house that Jack built, in Go", hat="beret",
  panel=N("the rhyme", ["This is the house that Jack built.", "This is the malt", "that lay in the house that Jack built.",
                        "This is the rat", "that ate the malt …"]))
C("pangram", "golang", "fox", ("sign", "#0e7490", "a-z"), "Pangram: every letter, once",
  T("pangram.go", ["package pangram", 'const Alphabets string =', '    "abcdefghijklmnopqrstuvqxyz"', "func IsPangram(in string) bool",
                   "", ("> The quick brown fox jumps", OK), ("  over the lazy dog.", OK)]))
C("say-a-number", "golang", "penguin", ("sign", "#0e7490", "123"), "Say a number, in words",
  T("say.go", ["var myMap = map[int]string{", '    0: "zero",', '    1: "one",', "}", "func tens(i int) (string, bool)",
               ('123 → "one hundred twenty-three"', OK)]))

# =================================================================================================================
# Python
# =================================================================================================================
C("moving-to-hugo-2-the-migration-playbook", "python", "boy", "box", "Moving to Hugo 2: the migration playbook",
  T("myblog", ["$ hugo new site myblog && cd myblog", "$ git init", "$ git submodule add -b main \\",
               "    https://github.com/nunocoracao/blowfish.git …", "", "[tools]", 'hugo-extended = "0.167.0"']),
  chips=["back up", "inventory", "convert", "rescue images"], hat="cap")
C("python-class", "python", "dog", ("sign", "#a16207", "Woof!"), "Python: classes",
  T("dog.py", ["class Dog:", "    def __init__(self, name, breed):", "        self.name = name", "    def bark(self):",
               '        print("Woof!")', 'dog = Dog("Fido", "Labrador")', "dog.bark()", ("# Output: Woof!", OK)]))
C("python-db", "python", "seal", ("box", "#a16207", "db"), "Python & SQLite",
  T("example.py", ["import sqlite3", "conn = sqlite3.connect('example.db')", "cursor = conn.cursor()",
                   "cursor.execute('''CREATE TABLE IF NOT", "    EXISTS users ( … )''')", "conn.commit()"]))
C("python-decorators", "python", "purplegirl", "wand", "Python: decorators", hat="wizard",
  panel=T("decorator.py", ["def logging_decorator(func):", "    def wrapper(*args, **kwargs):", "        result = func(*args, **kwargs)",
                           "        return result", "    return wrapper", "@logging_decorator", ("Running add with args: (3, 4), {}", OK),
                           ("add returned: 7", OK)]))
C("python-inheritance", "python", "panda", "book", "Python: inheritance",
  T("animal.py", ["class Animal:", "    def make_sound(self):", '        print("Some sound")', "class Dog(Animal):", "    …",
                  'dog = Dog("Mydo", "Belgian")', "dog.make_sound()", ("# Output: Woof!", OK)]))
C("python-interface", "python", "blackcat", ("sign", "#a16207", "ABC"), "Python: interfaces with ABC",
  T("shape.py", ["from abc import ABC, abstractmethod", "class Shape(ABC):", "    @abstractmethod", "    def area(self):",
                 "        pass", "class Square(Shape):", "    …"]))
C("python-multi-args", "python", "monkey", "balloon", "Python: *args and **kwargs",
  T("args.py", ["def foo(*args):", "    for arg in args:", "        print(arg)", "foo(1, 2, 3)", "def bar(**kwargs):",
                '    for key, value in kwargs.items(): …', "bar(a=1, b=2, c=3)", ("# a: 1  b: 2  c: 3", OK)]))
C("python-pointers-reference", "python", "koala", "lens", "Python: names, not pointers",
  T("refs.py", ["a = [1, 2, 3]", "b = a", "b[1] = 4", "print(a)", ("# Output: [1, 4, 3]", OK), ("# a and b are the same list", DIM)]))
C("python-sample-project", "python", "redgirl", "box", "Python: a sample project with tests",
  T("test_square.py", ["def square(x):", "    return x * x", "", "import unittest", "class TestSquare(unittest.TestCase):",
                       "    def test_square(self):", "        self.assertEqual(square.square(2), 4)"]))
C("testinfra", "python", "meerkat", "lens", "Testinfra: test the server, not the script",
  T("test_example.py", ["def test_httpd_installed(host):", '    httpd = host.package("httpd")', "    assert httpd.is_installed", "",
                        "$ testinfra test_example.py"]))

# =================================================================================================================
# Security
# =================================================================================================================
C("cism-security-governance-notes", "security", "owl", ("book", "#b91c1c", "CISM"), "CISM: controls meet governance", hat="grad_cap",
  panel=T("risk register", ["Business objective -> risk -> control", "  -> owner -> evidence -> review", "", ("Risk ID:    INFRA-014", KEY),
                            "Likelihood: Possible", ("Impact:     High", WARN), "Owner:      Platform Engineering", "Treatment:  Reduce",
                            "Review:     Quarterly"]))
C("cracking-cism", "security", "boy", ("book", "#b91c1c", "CISM"), "Cracking CISM", hat="headband",
  panel=S("how I prepared", [("Review manual", "read it all"), ("Practice questions", "heaps of them"), ("Read keywords", "MOST, LEAST"),
                             ("Groups of 10", "150 questions")]))
C("elastic-_security-api", "security", "hedgehog", "key", "Elastic: the _security API",
  T("_authenticate", ["> GET /_security/_authenticate HTTP/1.1", "> Host: es.example:9200", "> Authorization: Basic …", "",
                      ("< HTTP/1.1 200 OK", OK)]))
C("golang-hash", "security", "inkgirl", "padlock", "Go: hashing with crypto",
  T("hash.go", ["hasher = md5.New()", "io.WriteString(hasher,", "    \"And Leon's getting laaarger!\")", 'fmt.Printf("%x\\n", hasher.Sum(nil))',
                ]), chips=["MD5", "SHA1", "SHA256", "BLAKE2b"])
C("golang-simplecipher", "security", "fox", "key", "Go: a simple cipher",
  T("cipher.go", ["// Encrypt struct", "type Encrypt struct {", "    distance int", "    key      string", "}",
                  "// NewCaesar Object that implements", "// the interface Cipher"]), chips=["Caesar", "Shift", "Vigenère"])
C("isg-information-security-governance", "security", "lion", "scroll", "Information security governance", hat="crown",
  panel=S("Policies + Standards + Procedures", [("Strategic alignment", "with the business"), ("Risk management", "reduce impact"),
                                               ("Value delivery", "spend wisely"), ("Performance", "measure, report")]))
C("kafka-jmx-reading-metrics", "security", "otter", "lens", "Kafka JMX: read the numbers in order",
  T("consumer lag", ["traffic -> latency -> consumer lag", "  -> replication -> JVM -> host", "",
                     ("Before: lag=120,    1,020 records/sec", OK), ("After:  lag=40,000,  115 records/sec", WARN),
                     ("Broker bytes in: unchanged", DIM)]))
C("ldap-realm-in-elasticsearch", "security", "navyboy", "key", "An LDAP realm in Elasticsearch",
  T("elasticsearch.yml", ["xpack.security.enabled: true", "xpack.security.authc.realms:", "  native.secops:", "    order: 0",
                          "  ldap.secldap:", "    order: 1", '    url: "ldaps://ldap.example.com:636"', '    filter: "(uid={0})"']))
C("pki", "security", "polar", "key", "PKI: keys, certificates, trust",
  S("the pieces", [("Public key", "encrypts"), ("Private key", "decrypts"), ("X.509", "identity"), ("CA", "signs"), ("CRL", "revokes")]))
C("securing-kafka-brokers", "security", "turtle", "padlock", "Securing Kafka brokers: a checklist",
  T("permissions", [("/etc/kafka/server.properties  root:kafka 0640", KEY), ("/etc/kafka/secrets/           root:kafka 0750", KEY),
                    ("/var/lib/kafka/               kafka:kafka 0750", KEY), "",
                    ("-rw-r----- 1 root kafka 18432 server.properties", OK), ("drwxr-x--- 3 kafka kafka 4096 /var/lib/kafka", OK)]))
C("spring-data-ldap", "security", "greengirl", "plug", "Spring Data LDAP",
  T("pom.xml", ["<dependency>", "  <groupId>org.springframework.boot</groupId>", "  <artifactId>", "    spring-boot-starter-data-ldap",
                "  </artifactId>", "</dependency>"]), chips=["Angular", "Spring", "LDAP"])
C("understanding-pci-dss-ensuring-security-in-payment-card-transactions", "security", "pig", "padlock", "PCI DSS: protect the card data",
  S("key requirements", [("Secure network", "infrastructure"), ("Cardholder data", "encryption"), ("Access controls", "who sees it"),
                         ("Practices", "policies, procedures")]))
C("xee-xml-entity-attack-xxe", "security", "blackcat", "scroll", "XXE: the billion laughs attack",
  T("lol.xml", ['<!DOCTYPE lolz [', '  <!ENTITY lol "lol">', '  <!ENTITY lol1 "&lol;&lol;&lol;…">', '  <!ENTITY lol2 "&lol1;&lol1;…">',
                "  …", "]>", "<lolz>&lol9;</lolz>", ("# one entity expands to a billion", WARN)]))

# =================================================================================================================
# Streams (Kafka and Java streams)
# =================================================================================================================
C("consumer", "kafka", "bunny", "mug", "Java: the Consumer interface",
  T("Main.java", ["Consumer<String> myString =", "    (x) -> System.out.println(x);", 'myString.accept("Hello World!");', "",
                  "toUpper.andThen(toJoin)", "       .accept(dummyContents);", ("Hello World!", OK)]))
C("event-streaming", "kafka", "tealgirl", "envelope", "Event streaming",
  N("Apache Kafka", ["“Event streaming is the digital", "equivalent of the human body's", "central nervous system.”",
                     ("distributed · secure · fault-tolerant", "#334155")]))
C("java-stream-examples", "kafka", "duck", "lens", "Java streams: six examples",
  T("PlaySteams.java", ["int[] a = new int[]", "    {1,1,1,2,2,2,3,3,3,4,4,4};", "//Stream Sum of the array",
                        "long sum = IntStream.range(0, a.length)", "                 .count();", 'System.out.printf("Sum: %d\\n", sum);']))
C("java-streams", "kafka", "lamb", "scroll", "Java streams, with BigInteger",
  T("Streams.java", ["private Map<Integer, BigInteger> lHM =", "    new LinkedHashMap<>();", "for (int i = 0; i < 64; i++) {",
                     "  if (i == 0) {", "    lHM.put(Integer.valueOf(1), BigInteger.ONE);", "    continue;", "  } …"]))
C("javastream-characters", "kafka", "fox", ("sign", "#334155", "a-z"), "Java streams over characters",
  T("PangramChecker.java", ["public class PangramChecker {", "  private String allChars =", '      "abcdefghijklmnopqrstuvwxyz";',
                            "  public boolean isPangram(String input) {", "    if (input.isBlank()) return false;", "    …"]))
C("kafka-cluster-fundamentals", "kafka", "seal", ("box", "#334155", "P0"), "Kafka: brokers, topics, partitions",
  T("topics", ["partition = hash(key) % number_of_partitions", "", "$ kafka-topics.sh \\", "    --bootstrap-server broker.example:9092 \\",
               "    --create --topic events \\", "    --partitions 3 --replication-factor 3"]), chips=["leaders", "replicas", "consumer groups"])
C("naming-convention-policy-for-kafka-topics", "kafka", "deer", ("sign", "#334155", "a.b.c"), "Kafka: a topic naming policy",
  T("topics", ["$ bin/kafka-topics.sh --help", "", "<organizationname>.<productname>", ("# a CreateTopicPolicy on every broker", DIM)]))
C("nth-prime", "kafka", "curlyboy", "flag", "The nth prime, with IntStream",
  T("PrimeCalculator.java", ["public int nth(int nth) {", "  if (nth <= 0)", "    throw new IllegalArgumentException();",
                             "  return IntStream.iterate(2, i -> i + 1)", "      .filter(…)…", "}"]))

# =================================================================================================================
# Java
# =================================================================================================================
C("gradle", "java", "bear", "wrench", "Gradle: a graph of tasks", hat="goggles",
  panel=S("lifecycle tasks", [("Clean", "lifecycle"), ("Check", "lifecycle"), ("Assemble", "lifecycle"), ("Build", "a DAG of tasks")]))
C("map-and-flatmap", "java", "cat", "box", "Java: map and flatMap",
  T("Main.java", ["<R> Stream<R> flatMap(Function<? super T,", "    ? extends Stream<? extends R>> mapper)", "",
                  "Arrays.stream(myArray)", "    .map(index -> index * 5)", "    .forEach(System.out::println);"]))
C("smallest-integer", "java", "mouse", ("sign", "#b45309", "1"), "The smallest missing integer",
  T("Solution.java", ["[-1, 2]  -> 1", "[-1,-2]  -> 1", "[1, 3]   -> 2", "class Solution {", "  public int solution(int[] A) {",
                      "    int smallestInt = 1;", "    // Sort …"]))
C("tip-maven", "java", "owl", ("mug", "#b45309", "JAVA"), "Tip: Maven and JAVA_HOME",
  T("env", ["export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-…", "export M2_HOME=/usr/share/maven", "export PATH=${M2_HOME}/bin:${PATH}",
            "$ mvn -version", ("Apache Maven 3.0.5 (Red Hat 3.0.5-17)", OK), ("Java version: 11.0.16.1", OK)]))

# =================================================================================================================
# DevOps
# =================================================================================================================
C("ansible-configuration-basics", "devops", "koala", "scroll", "Ansible: make the defaults explicit",
  T("ansible-project/", ["ansible.cfg", "inventory/", "  hosts.ini", "playbooks/", "  site.yml", "", "$ ansible --version",
                         "$ ansible-config dump --only-changed"]))
C("ansible-magic-variables", "devops", "silvergirl", "wand", "Ansible: magic variables", hat="wizard",
  panel=T("debug", ["msg:", '  - "inventory name: {{ inventory_hostname }}"', '  - "groups: {{ group_names }}"', "",
                    "TASK [Show the current host] ****", ("ok: [web01] => {", OK), ('    "inventory name: web01",', OK),
                    ("    \"groups: ['web']\"", OK)]))
C("ansible-playbook-structure", "devops", "bear", "scroll", "A maintainable Ansible playbook",
  T("ansible/", ["ansible.cfg", "inventories/", "  lab/hosts.ini", "  production/hosts.ini", "playbooks/", "",
                 "- name: Configure the Kafka platform", "  hosts: kafka_brokers"]))
C("consul", "devops", "meerkat", "telescope", "Consul: service discovery and more",
  S("what Consul gives you", [("Service discovery", "DNS + HTTP"), ("Health checking", "drop the failing"),
                              ("Key-value store", "configuration"), ("Multi-datacenter", "one view")]))
C("iac-infrastructure-as-code", "devops", "brownboy", "wrench", "IaC: installing Terraform", hat="hardhat", acc="#4338ca",
  panel=T("terraform", ["$ brew tap hashicorp/tap", "$ brew install hashicorp/tap/terraform", "$ terraform -h",
                        ("Usage: terraform [global options]", OK), ("       <subcommand> [args]", OK)]))
C("moving-to-hugo-3-living-with-hugo", "devops", "blondboy", "pencil", "Moving to Hugo 3: living with it",
  T("my-new-post", ["$ hugo new content posts/my-new-post/index.md", "---", 'title: "My New Post"', "date: 2026-10-26T09:00:00-04:00",
                    'categories: ["technical"]', "tags: []", "---"]))
C("scm-for-git-clone", "devops", "mole", "key", "Maven SCM and git clone",
  T("mvn", ["$ mvn scm:checkout -DcheckoutDirectory=./helm-chart2 …", ("[ERROR] The git-clone command failed.", WARN),
            ("git@github.com: Permission denied (publickey).", WARN), ("fatal: Could not read from remote repository.", WARN), "",
            "$ mvn release:prepare", "$ mvn release:perform"]))
C("spinnaker-artifact-helm", "devops", "penguin", "wheel", "Spinnaker: Helm artifacts",
  T("halyard", ["$ hal config artifact helm enable", "$ hal config artifact helm account get dev-helm-ac", ("+ Get current deployment", OK),
                ("  Success", OK), ("+ Artifact account dev-helm-ac:", OK), "$ hal deploy apply"]))
C("spinnaker-docker-registry", "devops", "redpanda", "box", "Spinnaker: a docker-registry provider",
  T("halyard", ["$ hal config provider docker-registry \\", "    account list", ("+ Accounts for dockerRegistry:", OK), "",
                "$ hal config provider docker-registry \\", "    account get my-docker-registry", ("+ Account my-docker-registry:", OK)]))

# =================================================================================================================
# Web & APIs
# =================================================================================================================
C("creating-your-app-with-vuejs", "web", "frog", "flag", "Creating an app with Vue CLI",
  T("vue", ["$ vue --help", ("  create [options] <app-name>", KEY), ("  add [options] <plugin>", KEY), ("  serve [options] [entry]", KEY),
            "$ vue create samarthya", "$ npm run serve"]))
C("handshake-js", "web", "raccoon", ("sign", "#047857", "0b11"), "Secret handshake, in JavaScript",
  N("Secret handshake", ["a number comes in;", "its binary digits pick the moves:", ("wink · double blink · close your eyes · jump", "#047857")]))
C("kuberenetes-rest-api", "web", "duck", ("plug", "#047857", "API"), "Kubernetes: the REST API",
  N("the REST API", ["is the fabric of Kubernetes:", "every component talks through it,", "so everything is an API object."]))
C("maths-problem-in-js", "web", "hamster", "pencil", "A maths problem, with regex in JS",
  T("maths.js", ["let exp = /[0-9]*/;", "const Numeric = /-?\\d+\\b/g;", "const ADDITION = /\\bplus\\b/ig;", "",
                 ("> What is 50 plus 3?", KEY), ("operation: plus, numerals: [53, 2]", OK)]))
C("moving-to-hugo-1-why-hugo", "web", "redgirl", "lens", "Moving to Hugo 1: why Hugo",
  S("the candidates", [("WordPress, hardened", "same surface"), ("Ghost", "a server app"), ("Jekyll", "Ruby toolchain"),
                       ("Eleventy / Astro", "a node stack"), ("Hugo", "one Go binary")]))
C("vue-lesson-2", "web", "chick", "box", "Vue, lesson 2: the CLI",
  T("vue create", ["$ vue create hello-world -d", ("# -d: use the default preset", DIM)]),
  chips=["zero configuration", "create rapidly", "pick libraries", "optimise loading"])

# =================================================================================================================
# Notes and Agile
# =================================================================================================================
C("asynchronous", "notes", "purplegirl", "envelope", "Asynchronous: a remote team",
  N("one team, many time zones", ["How will you distribute the work?", "How will you track the progress?",
                                  "How will you agree on ground rules?"]))
C("devanagari", "notes", "inkgirl", "scroll", "Devanagari",
  N("देवनागरी", ["Hindi, Nepali, Marathi, Sanskrit", "written from left to right", "47 primary characters",
                 "a line runs along the top"]))
C("index-modules", "notes", "panda", ("box", "#c2410c", "idx"), "Elasticsearch: index modules",
  S("index settings", [("Static", "number_of_shards"), ("Static", "check_on_startup"), ("Dynamic", "number_of_replicas"),
                       ("Dynamic", "refresh_interval")]))
C("learning-step-1", "notes", "gingerboy", "lantern", "Learning, step 1: Laravel",
  T("homestead", ["$ laravel new myblog --force", "$ vagrant up", "$ laravel mix", ("# Vagrant + Laravel Homestead", DIM)]))
C("managers-dillema", "notes", "lion", "mug", "A manager's dilemma",
  N("“Do not handle adults with kid gloves”", ["Be direct; don't gloss the message.", "The organisation will back you.",
                                               "They get to show their maturity."]))
C("nuil-intf", "notes", "frog", "lens", "Go: the nil interface",
  T("nil.go", ["type NilI interface {", "     NoFunction()", "}", "var i NilI", "i.NoFunction()",
               ("panic: runtime error: invalid memory", WARN), ("address or nil pointer dereference", WARN)]))
C("quotes", "notes", "owl", "book", "Quotes",
  N("Quotes", ["“There are a thousand excuses for", "failure but never a good reason.”", ("— Mark Twain", DIM),
               "“Losers make excuses,", "winners make progress.”"]))
C("saturday-morning", "notes", "dog", "mug", "Saturday morning", hat="nightcap",
  panel=N("Saturday morning", ["a good night's sleep", "woke at 9:00 to the door bell", "my little devil, full of energy",
                               "a great day ahead"]))
C("serverless-patterns", "notes", "bunny", "balloon", "Serverless patterns",
  N("why serverless?", ["no upfront infrastructure cost", "1. storage services", "2. computing", "3. others"]))
C("the-inevitable", "notes", "tealgirl", "telescope", "The inevitable",
  N("generations", ["India: diversity, ever growing", "from copper-wire phones", "to the technological leap",
                    "“just enough” to “over the edge”"]))
C("safe-for-lean-enterprises", "agile", "purplegirl", ("flag", "#6d28d9", "SAFe"), "SAFe for Lean enterprises",
  S("four configurations", [("Essential SAFe", "start here"), ("Large Solution SAFe", "big systems"), ("Portfolio SAFe", "strategy"),
                            ("Full SAFe", "everything")]))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--check"]:  # list panel lines whose words are not in the post, to keep covers honest
        for slug, topic, *_rest in COVERS:
            panel = _rest[3]
            post = (REPO / "content/posts" / slug / "index.md").read_text(encoding="utf-8").lower()
            for ln in panel[2]:
                if not ln:
                    continue
                text = " ".join(ln) if panel[0] == "steps" else (ln if isinstance(ln, str) else ln[0])
                words = [w for w in re.findall(r"[a-z0-9_.:/=-]{3,}", text.lower()) if w not in ("node-1", "node-2", "node-3", "master")]
                miss = [w for w in words if w.strip(".:") not in post]
                if miss:
                    print(f"{slug:40} {text[:60]!r:64} missing: {miss}")
        sys.exit()
    if args[:1] == ["--topic"]:
        todo = [e for e in COVERS if e[1] == args[1]]
    else:
        todo = [e for e in COVERS if not args or e[0] in args]
    for e in todo:
        render(e)
        print("ok", e[0])
