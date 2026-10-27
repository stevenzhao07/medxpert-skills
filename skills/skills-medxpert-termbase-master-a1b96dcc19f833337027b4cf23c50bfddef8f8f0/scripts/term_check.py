#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""term_check.py — medical-device regulatory terminology checker.

Modes
-----
  lookup <term>              search the bilingual termbase (EN<->ZH, substring)
  stats                      termbase size by category
  check <file>               single-document lint: forbidden renderings,
                             non-canonical standard numbers
  pair <en_file> <zh_file>   bilingual QA: warning-level and modal-verb
                             distribution, plus standard-number parity

Stdlib only. Exit code 0 = no findings, 1 = findings, 2 = usage error.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "references"
TERMBASE = REF / "termbase.tsv"
MISTRANSLATIONS = REF / "mistranslations.tsv"

LEVEL_WORDS_EN = ["DANGER", "WARNING", "CAUTION", "NOTE"]
LEVEL_WORDS_ZH = {
    "DANGER": ["危险"],
    "WARNING": ["警告"],
    "CAUTION": ["注意", "小心"],
    "NOTE": ["提示", "说明"],
}
MODAL_ZH = {"shall": ["应", "须"], "should": ["宜"], "may": ["可以"]}

#: compounds that contain a modal character but are not modal usage
ZH_NOISE = {
    "应": ["反应", "响应", "供应", "相应", "对应", "适应", "照应", "效应",
           "应用", "回应", "感应", "应邀", "应诉", "应聘"],
    "宜": ["便宜", "适宜", "事宜", "宜昌", "宜人"],
}


# ---------------------------------------------------------------- data loading

def _read_tsv(path: Path):
    if not path.exists():
        sys.exit(f"missing data file: {path}")
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines:
        return []
    head = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        if not ln.strip():
            continue
        cells = ln.split("\t")
        cells += [""] * (len(head) - len(cells))
        rows.append(dict(zip(head, cells)))
    return rows


# ------------------------------------------------------------ standard numbers

_CODE_RE = re.compile(r"\b([A-Z]{2,5}(?:/[A-Z]{1,2})?)\s*(\d{2,5}(?:\.\d+)*)\b")


def canonical_codes(termbase) -> list[str]:
    """Canonical standard codes extracted from the keep-as-is column."""
    out = []
    for r in termbase:
        if r.get("kind") != "keep-as-is":
            continue
        for org, num in _CODE_RE.findall(r.get("en", "")):
            code = f"{org} {num}"
            if code not in out:
                out.append(code)
    return out


def standard_variants(code: str):
    """Regex variants that should have been written as `code`."""
    org, num = code.split(" ", 1)
    esc = re.escape
    return [
        (re.compile(rf"\b{esc(org)}\s*{esc(num)}\b"), f"{org}{num}（缺空格）"),
        (re.compile(rf"\b{esc(org.lower())}\s*{esc(num)}\b"), f"{org.lower()} {num}（机构缩写小写）"),
        (re.compile(rf"\b{esc(org)}[\uFF1A:]\s*{esc(num)}\b"), f"{org}:{num}（多余冒号）"),
    ]


# ---------------------------------------------------------------- check mode

def lint_text(text: str, termbase):
    findings = []  # (severity, line_no, kind, message)

    def line_of(idx: int) -> int:
        return text.count("\n", 0, idx) + 1

    for rule in _read_tsv(MISTRANSLATIONS):
        bad, good, reason, sev = rule["bad"], rule["good"], rule["reason"], rule["severity"]
        # if `good` merely extends `bad` (e.g. 一次性 -> 一次性使用), an occurrence
        # already followed by that extension is not a finding.
        suffix = good[len(bad):] if good.startswith(bad) else ""
        for m in re.finditer(re.escape(bad), text):
            end = m.end()
            if suffix and text[end:end + len(suffix)] == suffix:
                continue
            findings.append((sev, line_of(m.start()), bad,
                             f"「{bad}」→ 应为「{good}」（{reason}）"))

    for code in canonical_codes(termbase):
        for rx, why in standard_variants(code):
            for m in rx.finditer(text):
                if m.group(0) == code:
                    continue
                findings.append(("info", line_of(m.start()), code,
                                 f"标准号写法「{m.group(0)}」→ 规范写法「{code}」（{why}）"))
    return findings


# ---------------------------------------------------------- pair (bilingual)

def _count_zh(text: str, words) -> int:
    total = 0
    for w in words:
        t = text
        for noise in ZH_NOISE.get(w, []):
            t = t.replace(noise, "")
        total += len(re.findall(re.escape(w), t))
    return total


def pair_report(en_text: str, zh_text: str, termbase):
    findings, notes = [], []

    levels, modals = [], []
    for lv in LEVEL_WORDS_EN:
        levels.append((lv, len(re.findall(re.escape(lv), en_text)),
                       _count_zh(zh_text, LEVEL_WORDS_ZH[lv])))
    for k in ("shall", "should", "may"):
        modals.append((k, len(re.findall(rf"\b{k}\b", en_text, re.I)),
                       _count_zh(zh_text, MODAL_ZH[k])))

    for lv, en_n, zh_n in levels:
        zh_word = LEVEL_WORDS_ZH[lv][0]
        if en_n and zh_n == 0:
            findings.append(("error", 0, "warning-level",
                             f"英文出现 {lv} ×{en_n}，中文稿无对应「{zh_word}」——警示语被遗漏或弱化"))
        elif en_n and zh_n > en_n:
            findings.append(("warn", 0, "warning-level",
                             f"{lv}：英文 {en_n} 处 / 中文 {zh_n} 处，中文多于英文——核对是否新增或重复"))
        elif en_n and zh_n < en_n:
            findings.append(("warn", 0, "warning-level",
                             f"{lv}：英文 {en_n} 处 / 中文 {zh_n} 处，中文少于英文——核对是否漏译警示语"))
        elif lv in ("DANGER", "WARNING") and en_n == 0 and zh_n:
            findings.append(("warn", 0, "warning-level",
                             f"中文出现「{zh_word}」×{zh_n}，英文稿无 {lv}——核对是否自造警示级别"))

    caution_en = dict((l, e) for l, e, _ in levels)["CAUTION"]
    if caution_en and _count_zh(zh_text, ["注意", "小心"]) == 0 and _count_zh(zh_text, ["提示", "说明"]):
        findings.append(("error", 0, "warning-level",
                         "CAUTION 在中文稿疑似降级为「提示/说明」——警示强度只可等值或增强，不可弱化"))

    for k, en_n, zh_n in modals:
        if k == "shall" and en_n and zh_n == 0:
            findings.append(("error", 0, "modal-verb",
                             f"英文 shall ×{en_n}，中文稿无「应/须」——强制要求被弱化为建议"))
        if k == "should" and en_n and zh_n == 0:
            findings.append(("info", 0, "modal-verb",
                             f"英文 should ×{en_n}，中文稿无「宜」——建议性表述未用规范用语"))

    for code in canonical_codes(termbase):
        en_hit = len(re.findall(rf"\b{re.escape(code)}\b", en_text))
        zh_hit = len(re.findall(rf"\b{re.escape(code)}\b", zh_text))
        if en_hit and zh_hit == 0:
            findings.append(("error", 0, "standard-no",
                             f"英文稿引用「{code}」×{en_hit}，中文稿未出现——标准号不得翻译或省略"))
        elif en_hit and zh_hit and en_hit != zh_hit:
            notes.append(f"「{code}」出现次数不一致：英文 {en_hit} / 中文 {zh_hit}")

    return levels, modals, findings, notes


# ------------------------------------------------------------------- command

def cmd_lookup(term: str) -> int:
    tb = _read_tsv(TERMBASE)
    t = term.strip().lower()
    hits = [r for r in tb if t in r["en"].lower() or t in r["zh"]]
    if not hits:
        print(f"no match for {term!r} in termbase ({len(tb)} entries)")
        return 1
    print(f"{len(hits)} match(es) for {term!r}:")
    for r in hits:
        print(f"  {r['en']:<44} | {r['zh']:<26} | {r['note']} [{r['kind']}]")
    return 0


def cmd_stats() -> int:
    tb = _read_tsv(TERMBASE)
    print(f"termbase: {TERMBASE}")
    print(f"total entries: {len(tb)}")
    for k, v in Counter(r["kind"] for r in tb).most_common():
        print(f"  {k:<15} {v}")
    print(f"mis-translation rules: {len(_read_tsv(MISTRANSLATIONS))}")
    print(f"canonical standard codes: {len(canonical_codes(tb))}")
    return 0


def cmd_check(path: str) -> int:
    tb = _read_tsv(TERMBASE)
    p = Path(path)
    if not p.exists():
        sys.exit(f"no such file: {path}")
    text = p.read_text(encoding="utf-8", errors="replace")
    findings = lint_text(text, tb)
    if not findings:
        print(f"OK — no findings in {p.name} ({len(text)} chars checked)")
        return 0
    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (order.get(f[0], 3), f[1]))
    print(f"FINDINGS in {p.name}: "
          + ", ".join(f"{k}={v}" for k, v in Counter(f[0] for f in findings).items()))
    for sev, ln, kind, msg in findings:
        print(f"  [{sev:<5}] {'L' + str(ln) if ln else '--':>6}  {msg}")
    return 1


def cmd_pair(en_path: str, zh_path: str) -> int:
    tb = _read_tsv(TERMBASE)
    en_p, zh_p = Path(en_path), Path(zh_path)
    for p in (en_p, zh_p):
        if not p.exists():
            sys.exit(f"no such file: {p}")
    levels, modals, findings, notes = pair_report(
        en_p.read_text(encoding="utf-8", errors="replace"),
        zh_p.read_text(encoding="utf-8", errors="replace"),
        tb,
    )
    print(f"bilingual QA: {en_p.name}  <->  {zh_p.name}\n")
    print("warning levels (EN / ZH):")
    for lv, a, b in levels:
        print(f"  {lv:<8} {a:>4} / {b:<4}{'' if a == b else '   <-- check'}")
    print("\nmodal verbs (EN / ZH):")
    for k, a, b in modals:
        print(f"  {k:<8} {a:>4} / {b:<4}{'' if a == b else '   <-- check'}")
    if notes:
        print("\nnotes:")
        for n in notes:
            print(f"  - {n}")
    if findings:
        print(f"\nfindings ({len(findings)}):")
        for sev, _, kind, msg in findings:
            print(f"  [{sev:<5}] {kind:<15} {msg}")
        return 1
    print("\nOK — no cross-language findings")
    return 0


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "lookup" and len(argv) == 3:
        return cmd_lookup(argv[2])
    if cmd == "stats":
        return cmd_stats()
    if cmd == "check" and len(argv) == 3:
        return cmd_check(argv[2])
    if cmd == "pair" and len(argv) == 4:
        return cmd_pair(argv[2], argv[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
