<div align="center">

# 🩺 MedXpert Skills

**Medical Device Regulatory Skills for AI Agents.**

ISO 13485, ISO 14971, EU MDR, 21 CFR 820 — all in one skill pack.


<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/offline-yes-success" alt="Offline">
  <img src="https://img.shields.io/badge/dependencies-zero-success" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</p>

</div>

---

## ✨ What's Included

| Skill | What It Does |
|-------|--------------|
| ✅ **medxpert-termbase** | Bilingual terminology base & translation QA (164 terms, 36 mistranslation rules) |
| ✅ **iso14971-risk-matrix** | ISO 14971 risk matrix calculation & risk management file completeness check |
| ✅ **reg-citation-normalizer** | Normalize regulatory citations (21 CFR / ISO / NMPA) to standard format |

---

## 🚀 Quick Start

Install with one command:

```bash
npx skills add stevenzhao07/medxpert-skills
```

Then ask your AI agent:
- "Help me calculate this ISO 14971 risk"
- "Check my IFU translation for common mistakes"
- "Normalize this regulatory citation"

---

## 📄 License

[MIT](LICENSE) — open source, free for everyone.

---

<div align="center">

**Built for medical device regulatory professionals.**

⭐ If this helps you, give us a star!

</div>

---

## FHIR Terminology Contribution Package (fhir-contribution/)

MedXpert 医械法规中英双语术语的 **FHIR R5 资源包**，可直接服务于 FHIR 术语服务（`$lookup` / `$translate`）与 HL7/FHIR 生态贡献。

| Item | Value |
|---|---|
| 命名空间 | https://stevenzhao07.github.io/medxpert-fhir/ |
| 资源 | CodeSystem ×4（EN 164 / ZH 159 / 误译 36 / designation-use 4）、ValueSet ×4、ConceptMap ×2、ImplementationGuide ×1 |
| 数据源 | `skills/skills-medxpert-termbase-master-*/references/`（termbase.tsv 164 条 + mistranslations.tsv 36 条） |
| 复现 | `python build_fhir.py && python generate_ig.py && python validate_all_schema.py` |
| 校验 | FHIR R5 官方 JSON Schema **11/11 PASS**（2026-10-28） |
| 提交说明 | `fhir-contribution/CONTRIBUTION.md`（含原创性声明与提交通道） |
| 状态 | draft · 发布前审查"须修后发"进行中，正式提交前将发布 GitHub Pages 并提供可访问 IG 页面 |

**为什么贡献给 HL7/FHIR：** FHIR 公开术语空间缺少"医械法规领域 + 中英双语 + 误译纠正规则"的系统性资源；本包填补该空白，且已通过 HL7 IG 指南确认的合法外部贡献路径（自建 CodeSystem 纳入 IG）准备提交。
