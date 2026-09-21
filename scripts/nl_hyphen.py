"""Nederlandse lettergreep-splitsing voor liturgische lyrics (MXL en .mscz)."""
from __future__ import annotations

import re

# Handmatige splitsing voor woorden die de naive regel mist of verkeerd doet.
# Alleen de stam, zonder leestekens.
HYPHEN_EXCEPTIONS: dict[str, str] = {
    "altijd": "al-tijd",
    "eeuwen": "eeuw-en",
    "aanbidden": "aan-bid-den",
    "aanschouwen": "aan-schou-wen",
    "aarde": "aar-de",
    "allerlei": "al-ler-lei",
    "barmhartigheid": "barm-har-tig-heid",
    "barmhartigen": "barm-har-ti-gen",
    "dorsten": "dors-ten",
    "gedenk": "ge-denk",
    "gekomen": "ge-ko-men",
    "geschieden": "ge-schie-den",
    "heilige": "hei-li-ge",
    "hemelse": "he-mel-se",
    "hongeren": "hon-ge-ren",
    "kinderen": "kin-de-ren",
    "koninkrijk": "ko-nink-rijk",
    "lasterlijk": "las-ter-lijk",
    "nedervallen": "ne-der-val-len",
    "opgestaan": "op-ge-staan",
    "treurenden": "treu-ren-den",
    "vader": "va-der",
    "verheugt": "ver-heugt",
    "vervolgd": "ver-volgd",
    "vredestichters": "vre-de-stich-ters",
    "wanneer": "wan-neer",
    "wonderbaar": "won-der-baar",
    "worden": "wor-den",
    "zachtmoedigen": "zacht-moe-di-gen",
    "zalig": "za-lig",
    "zingen": "zin-gen",
    "zullen": "zul-len",
}

VOWELS = "aeiouyáéíóúàèëïöü"
DIPHTHONGS = (
    "aa", "ee", "oo", "uu", "ie", "ei", "ij", "ou", "au", "ui", "eu", "oe",
)
# Niet splitsen midden in deze clusters (VC-CV zou ch/ng stukmaken).
_CONS_KEEP = ("sch", "ch", "ng", "nk")


def strip_punct(token: str) -> tuple[str, str, str]:
    m = re.match(r"^(\W*)(.*?)(\W*)$", token, flags=re.U)
    if not m:
        return "", token, ""
    return m.group(1), m.group(2), m.group(3)


def _letter_units(stem: str) -> list[tuple[str, int, int]]:
    """('v'|'c', start, end) met tweeklanken als een klinker."""
    w = stem.lower()
    units: list[tuple[str, int, int]] = []
    i = 0
    while i < len(w):
        if w[i : i + 2] in DIPHTHONGS:
            units.append(("v", i, i + 2))
            i += 2
        elif w[i] in VOWELS:
            units.append(("v", i, i + 1))
            i += 1
        else:
            j = i
            while (
                j < len(w)
                and w[j] not in VOWELS
                and w[j : j + 2] not in DIPHTHONGS
            ):
                j += 1
            units.append(("c", i, j))
            i = j
    return units


def naive_hyphen(stem: str) -> list[str]:
    """Eenvoudige NL-splitsing: prefix, dubbele cons, V-CV / VC-CV."""
    w = stem.lower()
    if len(w) < 4:
        return [stem]
    prefixes = (
        "neder",
        "achter",
        "onder",
        "over",
        "voor",
        "aarts",
        "ge",
        "be",
        "ver",
        "ont",
        "aan",
        "her",
        "neer",
        "op",
        "uit",
        "toe",
        "mis",
        "wan",
    )
    for pref in prefixes:
        if w.startswith(pref) and len(w) - len(pref) >= 3:
            rest = stem[len(pref) :]
            return _restore_case(stem[: len(pref)], stem) + naive_hyphen(rest)

    m = re.search(r"([^aeiouyáéíóúàèëïöü])\1", w)
    if m and 0 < m.start() < len(w) - 1:
        i = m.start() + 1
        return _restore_case(stem[:i], stem) + naive_hyphen(stem[i:])

    units = _letter_units(stem)
    for i in range(len(units) - 2):
        kind0, _, _ = units[i]
        kind1, c0, c1 = units[i + 1]
        kind2, _, _ = units[i + 2]
        if kind0 != "v" or kind1 != "c" or kind2 != "v":
            continue
        cluster = w[c0:c1]
        if cluster in _CONS_KEEP or len(cluster) == 1:
            cut = c0
        else:
            cut = c0 + 1
        if 0 < cut < len(stem):
            return _restore_case(stem[:cut], stem) + naive_hyphen(stem[cut:])
    return [stem]


def _restore_case(part: str, original: str) -> list[str]:
    if original.isupper():
        return [part.upper()]
    if original[:1].isupper():
        return [part[:1].upper() + part[1:].lower()]
    return [part]


def _apply_case(parts: list[str], stem: str) -> list[str]:
    if stem.isupper():
        return [p.upper() for p in parts]
    if stem[:1].isupper():
        out = [p.lower() for p in parts]
        out[0] = out[0][:1].upper() + out[0][1:]
        return out
    return [p.lower() for p in parts]


def hyphenate_token(token: str) -> list[str]:
    raw = (token or "").replace("\xa0", " ").strip()
    if not raw:
        return []
    lead, stem, trail = strip_punct(raw)
    if not stem:
        return [raw]
    key = stem.lower()
    if key in HYPHEN_EXCEPTIONS:
        parts = HYPHEN_EXCEPTIONS[key].split("-")
        parts = _apply_case(parts, stem)
    else:
        groups = re.findall(rf"[{VOWELS}]+", stem, flags=re.I)
        if len(groups) < 2 or len(stem) < 4:
            return [raw]
        parts = naive_hyphen(stem)
        if len(parts) == 1:
            return [raw]
    if lead:
        parts[0] = lead + parts[0]
    if trail:
        parts[-1] = parts[-1] + trail
    return parts


def split_syllabic(orig: str, i: int, n: int) -> str:
    """MuseScore/MusicXML syllabic na splitsen van een bestaand lyric-token."""
    if n <= 1:
        return orig or "single"
    last = i == n - 1
    first = i == 0
    if orig == "begin":
        return "begin" if first else "middle"
    if orig == "middle":
        return "middle"
    if orig == "end":
        return "end" if last else "middle"
    if first:
        return "begin"
    if last:
        return "end"
    return "middle"
