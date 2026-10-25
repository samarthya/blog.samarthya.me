"""Privacy/content check for everything that gets published.

Scans text files for credential-shaped content and leaked local/migration paths, refuses migration
artifacts (SQL dumps, archives, PHP...), and reads image metadata for personal fields (GPS, owner,
serial numbers, copyright). Standard library only, so it runs anywhere CI runs.

    python tools/privacy/check.py                 # default: content static assets data layouts config
    python tools/privacy/check.py content/posts   # or any files/folders

Sources only, on purpose: every published word comes from these folders, and rendered HTML (joined lines,
HTML entities) produces false positives without finding anything new.

Exit status 1 if any finding is not covered by tools/privacy/allowlist.txt. Not flagged on purpose:
email addresses (example data and the public contact address are intentional) and documentation
placeholders such as <API_KEY>, ${TOKEN}, xxxx or changeme.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATHS = ["content", "static", "assets", "data", "layouts", "config"]
ALLOWLIST = Path(__file__).with_name("allowlist.txt")

TEXT_EXT = {".md", ".markdown", ".html", ".htm", ".txt", ".toml", ".yaml", ".yml", ".json", ".xml",
            ".css", ".js", ".svg", ".gotmpl", ".webmanifest"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
# Migration artifacts and server-side code never belong in the published tree.
FORBIDDEN_EXT = {".sql", ".gz", ".zip", ".tar", ".tgz", ".7z", ".php", ".env", ".bak", ".pem", ".key", ".p12", ".pfx"}
FORBIDDEN_NAMES = {"pseudonym.local.txt", "LOCAL-README.md", "TODO.md", "PUBLISHING.md", "MISSING-MEDIA.md",
                   "dns-directadmin.txt", "samarthya.me.cloudflare-import.txt"}

# (rule id, regex). Each regex's match is what gets reported and fingerprinted.
TEXT_RULES = [
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY(?: BLOCK)?-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    # key = value, key: value, "key": "value", KEY=value ... with a real-looking value (checked below)
    ("secret-assignment", re.compile(
        r"(?i)\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?key|client[_-]?secret|auth[_-]?token|token)"
        r"[\"']?\s*[:=]\s*[\"']?(?P<value>[^\s\"'<>`,;]{8,})")),
    ("local-path", re.compile(
        r"(?i)(?:\b[A-Z]:\\(?:Users|home)\\[^\s\"'<>]+|AppData[\\/]Local"
        r"|\bwp-import/|\bwp-uploads/|\buploads\.zip\b|\.sql\.gz\b|\bWordPress\.\d{4}-\d\d-\d\d\.xml\b"
        r"|pseudonym\.local\.txt)")),
]
PLACEHOLDER = re.compile(
    r"(?i)^(?:<.*>|\$\{.*\}|\$\(.*|\$[A-Z_]+|\{\{.*\}\}|x{3,}.*|\*{3,}.*|.*(?:changeme|example|placeholder|your[_-]|"
    r"replace|redacted|dummy|sample|secret_here|password_here).*)$")

# EXIF/TIFF tags that identify a person or a place.
PERSONAL_TAGS = {0x013B: "Artist", 0x8298: "Copyright", 0xA430: "CameraOwnerName",
                 0xA431: "BodySerialNumber", 0xA435: "LensSerialNumber", 0x8825: "GPS"}
PNG_TEXT_KEYS = {b"Author", b"Copyright", b"Owner", b"Artist"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    detail: str
    fingerprint: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.rule}] {self.detail} (fp {self.fingerprint})"


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def mask(text: str) -> str:
    """Show enough to locate a value without repeating a secret in logs."""
    return text if len(text) <= 12 else f"{text[:6]}...{text[-3:]} ({len(text)} chars)"


def scan_text(text: str, path: str = "<text>") -> list[Finding]:
    found = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rule, rx in TEXT_RULES:
            for m in rx.finditer(line):
                if rule == "secret-assignment":
                    value = m.group("value")
                    if PLACEHOLDER.match(value) or value.lower() in {"true", "false", "null", "none"}:
                        continue
                    hit = value
                else:
                    hit = m.group(0)
                found.append(Finding(path, lineno, rule, mask(hit), fingerprint(hit)))
    return found


def _tiff_personal_tags(tiff: bytes) -> set[str]:
    """Personal tags present in a TIFF/EXIF block (IFD0, its Exif sub-IFD and a non-empty GPS IFD)."""
    if len(tiff) < 8 or tiff[:2] not in (b"II", b"MM"):
        return set()
    end = "<" if tiff[:2] == b"II" else ">"

    def ifd(offset: int) -> dict[int, tuple[int, int, int]]:
        if offset + 2 > len(tiff):
            return {}
        (count,) = struct.unpack_from(end + "H", tiff, offset)
        entries = {}
        for i in range(count):
            pos = offset + 2 + 12 * i
            if pos + 12 > len(tiff):
                break
            tag, typ, n, value = struct.unpack_from(end + "HHII", tiff, pos)
            entries[tag] = (typ, n, value)
        return entries

    (first,) = struct.unpack_from(end + "I", tiff, 4)
    ifd0 = ifd(first)
    tags = dict(ifd0)
    if 0x8769 in ifd0:
        tags.update(ifd(ifd0[0x8769][2]))
    found = {name for tag, name in PERSONAL_TAGS.items() if tag in tags and tag != 0x8825}
    if 0x8825 in ifd0 and ifd(ifd0[0x8825][2]):
        found.add("GPS")
    return found


def image_metadata(data: bytes) -> set[str]:
    """Names of personal metadata fields in a JPEG, PNG or WebP file."""
    found: set[str] = set()
    if data[:2] == b"\xff\xd8":  # JPEG: walk the APPn segments before the image data
        pos = 2
        while pos + 4 <= len(data) and data[pos] == 0xFF:
            marker = data[pos + 1]
            if marker in (0xDA, 0xD9):  # start of scan / end of image
                break
            (size,) = struct.unpack_from(">H", data, pos + 2)
            seg = data[pos + 4:pos + 2 + size]
            if marker == 0xE1 and seg.startswith(b"Exif\x00\x00"):
                found |= _tiff_personal_tags(seg[6:])
            elif marker == 0xE1 and b"ns.adobe.com/xap" in seg[:64]:
                if re.search(rb"<dc:creator|exif:GPSLatitude|photoshop:Credit|xmpRights:Owner", seg):
                    found.add("XMP creator/GPS")
            pos += 2 + size
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        pos = 8
        while pos + 8 <= len(data):
            (length,) = struct.unpack_from(">I", data, pos)
            ctype, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
            if ctype == b"eXIf":
                found |= _tiff_personal_tags(body)
            elif ctype in (b"tEXt", b"iTXt") and body.split(b"\x00", 1)[0] in PNG_TEXT_KEYS:
                found.add("PNG " + body.split(b"\x00", 1)[0].decode())
            if ctype == b"IEND":
                break
            pos += 12 + length
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        pos = 12
        while pos + 8 <= len(data):
            ctype = data[pos:pos + 4]
            (length,) = struct.unpack_from("<I", data, pos + 4)
            if ctype == b"EXIF":
                body = data[pos + 8:pos + 8 + length]
                found |= _tiff_personal_tags(body[6:] if body.startswith(b"Exif\x00\x00") else body)
            pos += 8 + length + (length & 1)
    return found


def scan_file(path: Path, rel: str) -> list[Finding]:
    ext = path.suffix.lower()
    if path.name in FORBIDDEN_NAMES or ext in FORBIDDEN_EXT:
        return [Finding(rel, 0, "forbidden-file", "migration/private file must not be published", fingerprint(rel))]
    if ext in TEXT_EXT:
        return scan_text(path.read_text(encoding="utf-8", errors="replace"), rel)
    if ext in IMAGE_EXT:
        fields = image_metadata(path.read_bytes())
        if fields:
            return [Finding(rel, 0, "image-metadata", "personal metadata: " + ", ".join(sorted(fields)),
                            fingerprint(rel))]
    return []


def load_allowlist(path: Path) -> set[tuple[str, str]]:
    """Lines: '<rule> <fingerprint>  # reason'. Blank lines and comments are ignored."""
    allowed = set()
    if not path.exists():
        return allowed
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].split()
        if len(line) >= 2:
            allowed.add((line[0], line[1]))
    return allowed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", default=DEFAULT_PATHS, help="files or folders, relative to the repo root")
    ap.add_argument("--allowlist", type=Path, default=ALLOWLIST)
    args = ap.parse_args(argv)

    allowed = load_allowlist(args.allowlist)
    files = []
    for p in args.paths:
        target = (ROOT / p) if not Path(p).is_absolute() else Path(p)
        if not target.exists():
            continue
        files += [target] if target.is_file() else sorted(f for f in target.rglob("*") if f.is_file())

    findings, suppressed = [], 0
    for f in files:
        rel = f.relative_to(ROOT).as_posix() if f.is_relative_to(ROOT) else str(f)
        for finding in scan_file(f, rel):
            if (finding.rule, finding.fingerprint) in allowed:
                suppressed += 1
            else:
                findings.append(finding)

    for finding in findings:
        print(finding)
    print(f"privacy check: {len(files)} files, {len(findings)} finding(s), {suppressed} allowlisted")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
