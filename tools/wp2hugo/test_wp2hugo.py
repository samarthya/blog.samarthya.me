"""Behaviour tests for the importer's privacy safeguards.

    tools\\.venv\\Scripts\\python.exe -m unittest discover -s tools/wp2hugo -v

Runs the real script (in a temporary copy of tools/) on a one-post WordPress export, so the pseudonym file
can be present or absent. Needs the importer's own dependencies (beautifulsoup4, markdownify), so it is a
local test; CI runs the dependency-free tests in tools/privacy.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
HAS_DEPS = all(importlib.util.find_spec(m) for m in ("bs4", "markdownify"))

JWT = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzeXN0ZW06c2EifQ.c2lnbmF0dXJlLXZhbHVlLWhlcmU"
KEY = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAexample\n-----END RSA PRIVATE KEY-----"
BODY = f"<p>Written by Jane Testperson.</p><pre><code>token: {JWT}\n{KEY}\npassword=Tr0ub4dor-real-ish</code></pre>"
WXR = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:wp="http://wordpress.org/export/1.2/" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/">
<channel><item>
  <title>Test post</title>
  <content:encoded><![CDATA[{BODY}]]></content:encoded>
  <excerpt:encoded><![CDATA[]]></excerpt:encoded>
  <wp:post_id>42</wp:post_id><wp:post_name>test-post</wp:post_name>
  <wp:post_date>2021-01-02 03:04:05</wp:post_date><wp:post_date_gmt>2021-01-02 03:04:05</wp:post_date_gmt>
  <wp:status>publish</wp:status><wp:post_type>post</wp:post_type>
</item></channel></rss>"""


@unittest.skipUnless(HAS_DEPS, "importer dependencies (bs4, markdownify) not installed")
class ImporterPrivacy(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        tools = self.tmp / "tools"
        shutil.copytree(TOOLS / "privacy", tools / "privacy", ignore=shutil.ignore_patterns("__pycache__"))
        (tools / "wp2hugo").mkdir()
        shutil.copy(TOOLS / "wp2hugo" / "wp2hugo.py", tools / "wp2hugo")  # no pseudonym.local.txt copied
        (self.tmp / "export.xml").write_text(WXR, encoding="utf-8")
        self.script = tools / "wp2hugo" / "wp2hugo.py"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_importer(self, *extra):
        return subprocess.run([sys.executable, str(self.script), "--xml", "export.xml", "--all", "--out", "out",
                               "--report", "report.md", *extra], cwd=self.tmp, capture_output=True, text=True)

    def test_refuses_without_pseudonym_rules(self):
        r = self.run_importer()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("pseudonym", r.stderr)
        self.assertFalse((self.tmp / "out").exists(), "nothing may be written")

    def test_opt_in_converts_but_says_so(self):
        r = self.run_importer("--allow-unredacted")
        self.assertEqual(r.returncode, 0, r.stderr)
        post = (self.tmp / "out" / "test-post" / "index.md").read_text(encoding="utf-8")
        report = (self.tmp / "report.md").read_text(encoding="utf-8")
        self.assertIn("<REDACTED-TOKEN>", post)
        self.assertIn("<REDACTED-PRIVATE-KEY>", post)
        self.assertNotIn(JWT, post)
        self.assertIn("NONE loaded", report)
        self.assertIn("1 JWT(s), 1 private-key block(s)", report)
        self.assertIn("[secret-assignment]", report)  # left for manual review, not silently changed
        self.assertIn("Tr0ub4dor-real-ish", post)

    def test_rules_are_applied_and_counted(self):
        (self.script.parent / "pseudonym.local.txt").write_text("Jane Testperson => Samarthya\n", encoding="utf-8")
        r = self.run_importer()
        self.assertEqual(r.returncode, 0, r.stderr)
        post = (self.tmp / "out" / "test-post" / "index.md").read_text(encoding="utf-8")
        report = (self.tmp / "report.md").read_text(encoding="utf-8")
        self.assertNotIn("Jane Testperson", post)
        self.assertIn("**1 loaded**, 1 replacement(s) made", report)


@unittest.skipUnless(HAS_DEPS, "importer dependencies (bs4, markdownify) not installed")
class Overrides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("wp2hugo", TOOLS / "wp2hugo" / "wp2hugo.py")
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_alt_text_markdown_and_gallery(self):
        body = '![](a.png "Caption")\n![old](b.png)\n  <img src="c.png" alt="" class="grid-w50" />'
        ov = {"alt": {"a.png": "Chart of [x]", "b.png": "New", "c.png": 'Say "hi"'}}
        out, unmatched = self.mod.apply_overrides("p", body, {}, ov)
        self.assertIn('![Chart of (x)](a.png "Caption")', out)
        self.assertIn("![New](b.png)", out)
        self.assertIn('alt="Say &quot;hi&quot;"', out)
        self.assertEqual(unmatched, [])

    def test_description_and_replace(self):
        fields = {"description": ""}
        out, unmatched = self.mod.apply_overrides(
            "p", "*[image unavailable: x.png]*", fields,
            {"description": "One line.", "replace": [{"from": "*[image unavailable: x.png]*", "to": "See [source](https://example.com)"}]})
        self.assertEqual(fields["description"], "One line.")
        self.assertEqual(out, "See [source](https://example.com)")
        self.assertEqual(unmatched, [])

    def test_tags_replace_imported_tags(self):
        fields = {"tags": ["old"]}
        self.mod.apply_overrides("p", "text", fields, {"tags": ["ai", "llm"]})
        self.assertEqual(fields["tags"], ["ai", "llm"])

    def test_unmatched_entries_are_reported(self):
        _, unmatched = self.mod.apply_overrides("p", "no images here", {}, {
            "alt": {"gone.png": "x"}, "replace": [{"from": "absent", "to": "y"}]})
        self.assertEqual(len(unmatched), 2)


if __name__ == "__main__":
    unittest.main()
