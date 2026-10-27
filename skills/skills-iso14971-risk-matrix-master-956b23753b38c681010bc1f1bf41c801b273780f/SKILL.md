---
name: iso14971-risk-matrix
description: ISO 14971 risk-management helper for medical devices. Score a risk with
  a reference 5x5 severity x probability matrix (with an optional residual-risk comparison),
  print the risk-control option hierarchy of ISO 14971:2019 7.1 (inherently safe design
  / protective measures / information for safety), and check whether a risk-management
  file covers the elements ISO 14971:2019 requires (4.4 plan, 4.5 file, 5 analysis,
  6 evaluation, 7 control incl. 7.3/7.4, 8 overall residual risk, 9 review, 10 post-production).
version: 1.0.0
license: MIT
author: medxpert
tags:
- medical-device
- risk-management
- iso14971
- quality
- regulatory
permalink: workbuddy/2026-09-20-07-35-28/medxpert-skills/iso14971-risk-matrix/skill
---

# ISO 14971 Risk Matrix (风险矩阵计算与风险管理文件自查)

## When to Use

- You need to **turn a severity/probability pair into a risk level** consistently, in the vocabulary the standard itself uses.
- You are **building or auditing a risk management file** and need a clause-by-clause completeness pass against ISO 14971:2019 before a QMS audit or a submission.
- You are **training or checking a team's** use of the risk-control option hierarchy — the single most common audit finding is a file that jumps straight to "add a warning label".
- You want a **falsification check**: does the file show any evidence that the control measures actually reduced anything?

## Usage

```bash
# reference matrix
python scripts/risk_matrix.py matrix

# score one risk
python scripts/risk_matrix.py assess -s 4 -p 2

# score initial + post-control residual risk in one call
python scripts/risk_matrix.py assess -s 5 -p 5 --rs 2 --rp 1

# risk-control option hierarchy (ISO 14971:2019 7.1)
python scripts/risk_matrix.py options

# completeness check on a risk management file / its outline
python scripts/risk_matrix.py check risk_management_file.md
```

Exit code `0` = ok, `1` = blocking finding (residual risk still unacceptable, or critical RM elements missing), `2` = usage error.

## The Reference Matrix

Severity 1–5 (可忽略 / 轻度 / 严重 / 危重 / 灾难性) × probability 1–5 (极不可能 / 罕见 / 偶然 / 很可能 / 频繁); score = S × P.

| score | level | what it obliges |
|---|---|---|
| 1–4 | **L** 低 / 可接受 | record and monitor; evaluate residual risk per 7.3 |
| 5–9 | **M** 中 / ALARP | reduce to as low as reasonably practicable; verify the measure works |
| 10–25 | **H** 高 / 不可接受 | redesign or add protective measures; if the residual risk is still unacceptable, a benefit-risk analysis (7.4) is required |

> ⚠️ **This matrix is a convention, not the standard.** ISO 14971:2019 §4.4 requires *the manufacturer* to define, in its risk management plan, the policy for determining acceptable risk. A formal document must cite your own plan's criteria. This tool states that limit in its own output rather than quietly implying authority it does not have.

## What `assess` Also Does

- Prints the **ISO 14971:2019 clause 3 vocabulary chain** — hazard → sequence of events → hazardous situation → harm — as a completeness prompt. Analyses that skip a link are the usual root cause of "we found no risk".
- With `--rs/--rp`, compares the residual risk against the initial risk and **flags suspicious patterns**: residual still `H`, residual worse than initial, or residual *identical* to initial (i.e. the file claims control measures but the numbers never moved).

## What `check` Looks For

16 elements across ISO 14971:2019 clauses 4–10, each with EN and ZH keyword alternatives. Critical elements (plan, file, intended use, hazards, estimation, evaluation, control-option analysis, implementation, residual risk, overall residual risk, review, post-production) are reported separately from optional ones (safety characteristics, benefit-risk, risks from control measures, completeness).

**Keyword hits mean "the document mentions this", not "this is done."** The tool says so in its output; use it to find holes, then read.

## Known Limits (be explicit with users)

- ISO 14971 does not mandate a specific matrix; the 5×5 shipped here is one common convention. If your risk management plan defines different bands, **the plan wins** — reband the tool's mapping to match.
- Probability anchors (1e-6 … 1e-2 per device lifetime) are indicative only and are **not** from the standard.
- `check` is keyword-based and language-limited (EN + ZH). A file written in another language, or one using unusual headings, will produce false "missing" results.
- This tool does not write the risk file, does not decide acceptability for you, and does not constitute a regulatory opinion.

## Output Discipline

- Always show the arithmetic (S × P = score → band), never a bare band name.
- When the residual risk is worse than or equal to the initial risk, say plainly that the file shows no evidence of effective risk reduction — do not soften it.
- When a risk management file is checked, list the missing critical clauses individually so they can be closed one by one.