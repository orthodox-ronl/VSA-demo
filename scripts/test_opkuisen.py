"""Tests voor generieke opkuiser (detectie + CLI)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import opkuis_detect as detect
import opkuisen


TD = Path(__file__).resolve().parent / "testdata" / "opkuis"


class DetectTests(unittest.TestCase):
    def test_capella_from_software(self) -> None:
        r = detect.detect_path(TD / "capella-like.musicxml")
        self.assertTrue(r.ok)
        self.assertEqual(r.hoek, detect.HOEK_CAPELLA)
        self.assertGreaterEqual(r.confidence, 0.9)

    def test_generic_musicxml(self) -> None:
        r = detect.detect_path(TD / "generic.musicxml")
        self.assertTrue(r.ok)
        self.assertEqual(r.hoek, detect.HOEK_MUSICXML_GENERIC)
        self.assertFalse(r.low_confidence)

    def test_mscz(self) -> None:
        r = detect.detect_path(TD / "tiny.mscz")
        self.assertTrue(r.ok)
        self.assertEqual(r.hoek, detect.HOEK_MUSESCORE)

    def test_corrupt_mxl(self) -> None:
        r = detect.detect_path(TD / "corrupt.mxl")
        self.assertFalse(r.ok)
        self.assertIn("ongeldig", (r.error or "").lower())

    def test_print_mscz_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.print.mscz"
            p.write_bytes((TD / "tiny.mscz").read_bytes())
            r = detect.detect_path(p)
            self.assertFalse(r.ok)
            self.assertIn("print", (r.error or "").lower())

    def test_assume_overrides(self) -> None:
        r = detect.detect_path(
            TD / "generic.musicxml", assume=detect.HOEK_CAPELLA
        )
        self.assertEqual(r.hoek, detect.HOEK_CAPELLA)
        self.assertEqual(r.confidence, 1.0)

    def test_vsa_hoek(self) -> None:
        r = detect.detect_path(TD / "stub.vsa")
        self.assertEqual(r.hoek, detect.HOEK_VSA)


class CliTests(unittest.TestCase):
    def test_analyze_and_dry_run_equivalent(self) -> None:
        path = str(TD / "generic.musicxml")
        code_a = opkuisen.main([path, "--analyze"])
        code_d = opkuisen.main([path, "--dry-run"])
        self.assertEqual(code_a, 0)
        self.assertEqual(code_d, 0)

    def test_analyze_writes_nothing(self) -> None:
        src = TD / "generic.musicxml"
        before = src.read_bytes()
        self.assertEqual(opkuisen.main([str(src), "--analyze"]), 0)
        self.assertEqual(src.read_bytes(), before)

    def test_content_generic_to_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.musicxml"
            code = opkuisen.main(
                [str(TD / "generic.musicxml"), "-o", str(out)]
            )
            self.assertEqual(code, 0)
            self.assertTrue(out.is_file())
            text = out.read_text(encoding="utf-8")
            self.assertIn("score-partwise", text)

    def test_content_mscz(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "tiny.mscz"
            dest.write_bytes((TD / "tiny.mscz").read_bytes())
            code = opkuisen.main([str(dest)])
            self.assertEqual(code, 0)

    def test_vsa_content_refused(self) -> None:
        code = opkuisen.main([str(TD / "stub.vsa")])
        self.assertEqual(code, opkuisen.EXIT_REFUSED)

    def test_vsa_analyze_without_vsa_binary(self) -> None:
        with mock.patch("opkuisen.shutil.which", return_value=None):
            code = opkuisen.main([str(TD / "stub.vsa"), "--analyze"])
            self.assertEqual(code, opkuisen.EXIT_ERROR)

    def test_cap_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.cap"
            p.write_text("nope", encoding="utf-8")
            code = opkuisen.main([str(p)])
            self.assertEqual(code, opkuisen.EXIT_REFUSED)

    def test_spaces_require_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "has space.musicxml"
            src.write_text(
                (TD / "generic.musicxml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            code = opkuisen.main([str(src)])
            self.assertEqual(code, opkuisen.EXIT_REFUSED)

    def test_protected_input_without_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "oefenhoek" / "input" / "capella"
            root.mkdir(parents=True)
            src = root / "piece.musicxml"
            src.write_text(
                (TD / "generic.musicxml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            code = opkuisen.main(
                [str(src), "--assume", "musicxml-generic"]
            )
            self.assertEqual(code, opkuisen.EXIT_REFUSED)


class ExpandTests(unittest.TestCase):
    def test_recursive_and_skip_print(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sub = base / "sub"
            sub.mkdir()
            (sub / "a.musicxml").write_text(
                (TD / "generic.musicxml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            print_p = sub / "x.print.mscz"
            print_p.write_bytes((TD / "tiny.mscz").read_bytes())
            found = opkuisen.expand_opkuis_paths([base])
            names = {p.name for p in found}
            self.assertIn("a.musicxml", names)
            self.assertNotIn("x.print.mscz", names)


if __name__ == "__main__":
    unittest.main()
