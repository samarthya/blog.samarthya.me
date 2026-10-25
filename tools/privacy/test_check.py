"""Tests for tools/privacy/check.py.   python -m unittest discover -s tools/privacy -v"""
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402


def rules(text):
    return [f.rule for f in check.scan_text(text)]


def jpeg_with_gps():
    """Minimal JPEG whose EXIF IFD0 points to a non-empty GPS IFD."""
    tiff = b"II*\x00" + struct.pack("<I", 8)
    tiff += struct.pack("<H", 1) + struct.pack("<HHII", 0x8825, 4, 1, 26) + struct.pack("<I", 0)   # IFD0 -> GPS @26
    tiff += struct.pack("<H", 1) + struct.pack("<HHI4s", 0x0000, 1, 4, b"\x02\x02\x00\x00") + struct.pack("<I", 0)
    app1 = b"Exif\x00\x00" + tiff
    return b"\xff\xd8" + b"\xff\xe1" + struct.pack(">H", len(app1) + 2) + app1 + b"\xff\xd9"


def png_with_author():
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + b"\x00\x00\x00\x00"
    return b"\x89PNG\r\n\x1a\n" + chunk(b"tEXt", b"Author\x00Someone") + chunk(b"IEND", b"")


class TextRules(unittest.TestCase):
    def test_jwt(self):
        self.assertIn("jwt", rules("token eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhYmNkZWYifQ.c2lnbmF0dXJlX3ZhbHVl"))

    def test_private_key_header(self):
        self.assertIn("private-key", rules("-----BEGIN OPENSSH PRIVATE KEY-----"))

    def test_cloud_tokens(self):
        self.assertIn("aws-access-key", rules("AKIAIOSFODNN7EXAMPLE"))
        self.assertIn("github-token", rules("ghp_" + "a" * 36))

    def test_real_looking_secret_assignment(self):
        self.assertIn("secret-assignment", rules('"api_key": "NODL7y_TSkinR1GIitRGFQ"'))
        self.assertIn("secret-assignment", rules("password=Tr0ub4dor&3xyz"))

    def test_placeholders_are_not_flagged(self):
        for text in ("api_key: <API_KEY>", "password=<REPLACE-ME>", "token: ${TOKEN}", "secret=xxxxxxxxxx",
                     "password: changeme123", "token=$(kubectl get secret -o name)", "api_key = your-api-key-here"):
            self.assertEqual(rules(text), [], text)

    def test_emails_are_not_flagged(self):
        self.assertEqual(rules("write to iam@gaurav.me or bhanuni@bhanuni.in"), [])

    def test_local_and_migration_paths(self):
        self.assertIn("local-path", rules(r"C:\Users\someone\AppData\Local\Temp\x"))
        self.assertIn("local-path", rules("see wp-import/import-report.md"))
        self.assertIn("local-path", rules("samarthya.WordPress.2026-10-23.xml"))

    def test_unix_home_paths_in_examples_are_fine(self):
        self.assertEqual(rules("cd /home/user/sourcebox/project && make"), [])

    def test_line_numbers(self):
        f = check.scan_text("ok\nok\n-----BEGIN RSA PRIVATE KEY-----", "a.md")
        self.assertEqual((f[0].path, f[0].line), ("a.md", 3))

    def test_report_masks_values(self):
        f = check.scan_text("password=Tr0ub4dor&3xyz-long-value")[0]
        self.assertNotIn("Tr0ub4dor&3xyz-long-value", str(f))


class Files(unittest.TestCase):
    def scan(self, name, data):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / name
            p.write_bytes(data)
            return check.scan_file(p, name)

    def test_gps_in_jpeg(self):
        found = self.scan("photo.jpg", jpeg_with_gps())
        self.assertEqual([f.rule for f in found], ["image-metadata"])
        self.assertIn("GPS", found[0].detail)

    def test_clean_jpeg(self):
        self.assertEqual(self.scan("clean.jpg", b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9"), [])

    def test_png_author_text(self):
        self.assertIn("PNG Author", self.scan("x.png", png_with_author())[0].detail)

    def test_forbidden_files(self):
        for name in ("dump.sql", "uploads.zip", "shell.php", "pseudonym.local.txt", "TODO.md"):
            self.assertEqual([f.rule for f in self.scan(name, b"x")], ["forbidden-file"], name)


class Allowlist(unittest.TestCase):
    def test_allowlisted_fingerprint_is_suppressed_and_new_value_is_not(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "post.md").write_text('"api_key": "NODL7y_TSkinR1GIitRGFQ"\n"api_key": "A_brand_new_value_9"\n')
            allow = root / "allow.txt"
            allow.write_text("secret-assignment 051a1ceb5a4c  # obsolete lab key\n")
            self.assertEqual(check.main([str(root / "post.md"), "--allowlist", str(allow)]), 1)  # new value still fails
            (root / "post.md").write_text('"api_key": "NODL7y_TSkinR1GIitRGFQ"\n')
            self.assertEqual(check.main([str(root / "post.md"), "--allowlist", str(allow)]), 0)


if __name__ == "__main__":
    unittest.main()
