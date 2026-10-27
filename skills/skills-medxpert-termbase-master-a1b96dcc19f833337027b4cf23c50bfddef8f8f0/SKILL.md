---
name: medxpert-termbase
description: Bilingual terminology base and translation QA for medical-device regulatory
  documents. Look up the standard EN<->ZH rendering of ~160 regulatory terms (ISO
  13485 / ISO 14971 / ISO 10993, IEC 62304 / 62366, EU MDR 2017/745, 21 CFR 820),
  lint a draft for known mistranslations and non-canonical standard numbers, and run
  a cross-language QA on an EN/ZH document pair (warning-level weakening, shall/should
  modality loss, standard-number parity).
version: 1.0.0
license: MIT
author: medxpert
tags:
- medical-device
- regulatory
- terminology
- translation
- quality
permalink: workbuddy/2026-09-20-07-35-28/medxpert-skills/medxpert-termbase/skill
---

# MedXpert Termbase (医械法规术语库与译稿质检)

## When to Use

- You are drafting or reviewing a bilingual medical-device document (IFU, label, CER, technical file, test report, audit report) and need the **standard Chinese/English rendering** of a regulatory term.
- You want to **catch known mistranslations** before submission — the traps that repeatedly show up in Chinese medical-device translation (`过程验证` vs `过程确认`, `临床实验` vs `临床试验`, `CE 认证` vs `CE 标志`, …).
- You have an EN source and a ZH translation and need a **cross-language QA pass**: did every `WARNING` survive, did `shall` become a suggestion, did a standard number get translated away.
- You need a **standard number written correctly** (`ISO 13485`, `GB 9706.1`, `510(k)`) rather than in a half-translated or malformed form.

## Bundled Assets

| Path | What it is |
|---|---|
| `references/termbase.tsv` | 164 entries: `en`, `zh`, `note`, `kind` (`term` / `keep-as-is` / `warning-level` / `modal-verb`) |
| `references/mistranslations.tsv` | 36 high-frequency mistranslation rules: `bad` → `good`, reason, severity |
| `scripts/term_check.py` | The tool (stdlib only, no dependencies) |

## Usage

```bash
# 1) term lookup (substring, EN or ZH)
python scripts/term_check.py lookup biocompatibility
python scripts/term_check.py lookup 风险

# 2) termbase inventory
python scripts/term_check.py stats

# 3) single-document lint (Chinese or English draft)
python scripts/term_check.py check draft_zh.md

# 4) bilingual QA on an EN/ZH pair
python scripts/term_check.py pair ifu_en.md ifu_zh.md
```

Exit code `0` = clean, `1` = findings, `2` = usage error.

## What the Checks Actually Do

`check <file>`

1. **Forbidden renderings** — every rule in `mistranslations.tsv` is matched literally against the draft, reporting `「bad」→ 应为「good」` with the reason. Severity: `error` / `info`.
2. **Standard-number form** — for each canonical code in the `keep-as-is` set (`ISO 13485`, `ISO 14971`, `IEC 62304`, `GB/T 16886`, …) it flags missing spaces, lowercased agency prefixes and stray colons (`ISO13485`, `iso 13485`, `ISO：13485`).

`pair <en_file> <zh_file>`

1. **Warning-level ledger** — counts `DANGER / WARNING / CAUTION / NOTE` in the EN source against `危险 / 警告 / 注意·小心 / 提示·说明` in the ZH translation. Flags: a level present in EN but absent in ZH (dropped warning), a level whose ZH count falls short (partial loss), a level the ZH side invented, and — the recurring one — `CAUTION` silently downgraded to `提示/说明`.
2. **Modality ledger** — `shall` vs `应/须`, `should` vs `宜`, `may` vs `可以`. Flags `shall` with no ZH obligation word (a requirement weakened into advice).
3. **Standard-number parity** — any standard code cited in the EN but absent from the ZH (standards are never translated or dropped).

Chinese modal counting strips non-modal compounds (`反应`, `相应`, `应用`, `适宜`, …) so `应` and `宜` counts are not inflated by ordinary vocabulary.

## Translation Rules This Skill Enforces

| Rule | Why |
|---|---|
| Standard numbers, regulation names and agency names are **never translated** | `ISO 13485` stays `ISO 13485`; writing `国际标准化组织13485` breaks traceability |
| One term, one rendering — do not vary within a document | Regulators read consistency as a proxy for control |
| Warning strength may be **equal or stronger**, never weaker | `WARNING` may not become `注意`; `CAUTION` may not become `提示` |
| `validation` → 确认, `verification` → 验证 | `process validation` = 过程确认; mixing them is the most common QA finding |
| `must` → `应` (shall) in formal documents | `必须` is conversational emphasis, not specification language |
| Recall wording follows the target market | US Recall / EU FSCA / CN 召回 — do not mix |

## Known Limits (be explicit with users)

- The termbase is a **curated working list (~164 entries), not an official glossary**. There is no ISO-endorsed Chinese translation of ISO 13485 vocabulary; always defer to the applicable national standard's own wording (e.g. GB/T 42061 for ISO 13485, YY/T 1437 for ISO 14971 terminology) when a regulator will read it.
- The `pair` mode is a **statistical parity check, not an alignment**. It compares counts, not sentence-by-sentence correspondence — a legitimate restructuring can produce a flag. Treat findings as "go look here", not as verdicts.
- `check` only finds *listed* traps. A clean run means "none of the 36 known traps and no malformed standard number", not "correct translation".
- The skill does not translate. It reviews.

## Output Discipline

- Report the finding with its line number, the offending text and the suggested replacement — never a bare "translation has issues".
- Distinguish `error` (contradicts a published convention) from `info` (house style / writing preference).
- If a term is not in the termbase, say so and suggest confirming against the applicable standard's own vocabulary instead of inventing an entry.