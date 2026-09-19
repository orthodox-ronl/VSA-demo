"""Tests voor bieb_accepteer (classificatie + dry-run scaffold)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import bieb_accepteer as ba
from bibliotheek import BIBLIOTHEEK_ROOT, stem


class ClassifyTests(unittest.TestCase):
    def test_print_vs_hub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hub = root / "x.mscz"
            hub.write_bytes(b"PK")
            print_mscz = root / "x.print.mscz"
            print_mscz.write_bytes(b"PK")
            vsa = root / "x.vsa"
            vsa.write_text("t\n", encoding="utf-8")
            self.assertEqual(ba.classify_source(hub), "hub_mscz")
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
            ba.target_name("hub_mscz", ident, with_vsa=False),
            f"{stem(ident)}.mscz",
        )
        self.assertEqual(
            ba.target_name("mxl", ident, with_vsa=True),
            f"{stem(ident)}.vsa.mxl",
        )


class AcceptDryRunTests(unittest.TestCase):
    def test_dry_run_stub_ok(self) -> None:
        # Geen schrijfactie; faalt alleen op id/alias.
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


if __name__ == "__main__":
    unittest.main()
