import os
import tempfile
import unittest

from core.report_generator import build_report, write_pdf_report


class ReportGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "subject": {
                "full_name": "Example Person",
                "email": "example@email.com",
                "phone": "+33 6 00 00 00 00",
                "username": "exampleuser",
            },
            "findings": [
                {
                    "category": "Profil public",
                    "category_en": "Public profile",
                    "details": "Bio publique",
                    "details_en": "Public bio",
                    "source": "https://example.com/profile",
                    "reliability": "medium",
                }
            ],
            "sources": [
                {
                    "label": "Profil public",
                    "label_en": "Public profile",
                    "url": "https://example.com/profile",
                    "reliability": "medium",
                    "notes": "Page publique",
                    "notes_en": "Public page",
                }
            ],
            "notes": [
                {"fr": "Note en francais", "en": "Note in English"},
            ],
        }

    def test_build_report_contains_sections(self):
        html = build_report(self.data)
        self.assertIn("Identifiants / Identifiers", html)
        self.assertIn("Constats / Findings", html)

    def test_write_pdf_report_creates_pdf(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.pdf")
            write_pdf_report(output_path, self.data)
            self.assertTrue(os.path.exists(output_path))
            with open(output_path, "rb") as handle:
                header = handle.read(4)
            self.assertEqual(header, b"%PDF")
