"""Tests voor bieb_accepteer (classificatie + dry-run + interactieve prompts)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import bieb_accepteer as ba
from bibliotheek import BIBLIOTHEEK_ROOT, stem


class ClassifyTests(unittest.TestCase):
    def test_print_vs_partituur(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            basispartituur = root / "x.mscz"
            basispartituur.write_bytes(b"PK")
            print_mscz = root / "x.print.mscz"
            print_mscz.write_bytes(b"PK")
            vsa = root / "x.vsa"
            vsa.write_text("t\n", encoding="utf-8")
            self.assertEqual(ba.classify_source(basispartituur), "partituur_mscz")
            self.assertEqual(ba.classify_source(print_mscz), "print_mscz")
            self.assertEqual(ba.classify_source(vsa), "vsa")

    def test_refuse_capella(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cap = Path(tmp) / "ruw.capx"
            cap.write_bytes(b"x")
            kind = ba.classify_source(cap)
            self.assertTrue(kind.startswith("refuse:"))

    def test_target_names(self) -> None:
        ident = "5-eniggeboren-zoon/default/hemelum"
        self.assertEqual(
            ba.target_name("partituur_mscz", ident, with_vsa=False),
            f"{stem(ident)}.mscz",
        )
        self.assertEqual(
            ba.target_name("mxl", ident, with_vsa=True),
            f"{stem(ident)}.vsa.mxl",
        )


class AcceptDryRunTests(unittest.TestCase):
    def test_dry_run_stub_ok(self) -> None:
        code = ba.accept(
            "zz-test-accepteer/default/hemelum",
            [],
            title="Test",
            status="voorzien",
            stub=True,
            move=False,
            force=False,
            dry_run=True,
            skip_vsa_validate=True,
            artefacten_handmatig=False,
        )
        self.assertEqual(code, 0)
        leaf = BIBLIOTHEEK_ROOT / "zz-test-accepteer" / "default" / "hemelum"
        self.assertFalse(leaf.exists())

    def test_refuse_bare_mxl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mxl = Path(tmp) / "alleen.mxl"
            mxl.write_bytes(b"PK")
            code = ba.accept(
                "zz-test-accepteer/default/hemelum",
                [mxl],
                title=None,
                status=None,
                stub=False,
                move=False,
                force=False,
                dry_run=True,
                skip_vsa_validate=True,
                artefacten_handmatig=False,
            )
            self.assertEqual(code, 1)


class PromptTests(unittest.TestCase):
    def test_resolve_ident_from_cli(self) -> None:
        self.assertEqual(
            ba.resolve_ident("5-eniggeboren-zoon/default/hemelum"),
            "5-eniggeboren-zoon/default/hemelum",
        )

    def test_resolve_ident_asks_after_question_mark(self) -> None:
        answers = iter(["5-eniggeboren-zoon/default/hemelum"])
        with patch("bieb_accepteer.prompt_line", side_effect=lambda _m: next(answers)):
            self.assertEqual(
                ba.resolve_ident("?"),
                "5-eniggeboren-zoon/default/hemelum",
            )

    def test_resolve_ident_rejects_then_accepts(self) -> None:
        answers = iter(["niet-geldig", "5-eniggeboren-zoon/default/hemelum"])
        with patch("bieb_accepteer.prompt_line", side_effect=lambda _m: next(answers)):
            self.assertEqual(
                ba.resolve_ident(None),
                "5-eniggeboren-zoon/default/hemelum",
            )

    def test_resolve_bestand_stub(self) -> None:
        answers = iter(["stub"])
        with patch("bieb_accepteer.prompt_line", side_effect=lambda _m: next(answers)):
            got = ba.resolve_bestanden_en_stub([], stub=False)
        self.assertEqual(got, ([], True))

    def test_resolve_bestand_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mscz = Path(tmp) / "x.mscz"
            mscz.write_bytes(b"PK")
            answers = iter([str(mscz), ""])
            with patch(
                "bieb_accepteer.prompt_line",
                side_effect=lambda _m: next(answers),
            ):
                got = ba.resolve_bestanden_en_stub([], stub=False)
            self.assertIsNotNone(got)
            assert got is not None
            paths, stub = got
            self.assertFalse(stub)
            self.assertEqual(len(paths), 1)
            self.assertEqual(paths[0].resolve(), mscz.resolve())

    def test_main_interactive_stub_dry_run(self) -> None:
        answers = iter(
            [
                "zz-test-accepteer/default/hemelum",
                "stub",
            ]
        )
        with patch("bieb_accepteer.prompt_line", side_effect=lambda _m: next(answers)):
            code = ba.main(["--dry-run"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
