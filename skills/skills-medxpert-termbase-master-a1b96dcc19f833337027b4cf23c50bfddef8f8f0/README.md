---
title: README
type: note
permalink: workbuddy/2026-09-20-07-35-28/medxpert-skills/medxpert-termbase/readme
---

# MedXpert Termbase — 医械法规术语库与译稿质检

给医疗器械注册/法规事务（RA）与质量团队用的**中英术语速查 + 译稿质检**小工具。

## 它解决什么

医械法规文档的中英互译里，有一批错误会**反复出现**，而它们恰好是审核员最容易抓的点：

| 常见写法 | 规范写法 | 为什么 |
|---|---|---|
| 过程验证 | **过程确认** | `process validation` = 确认；`verification` 才是验证 |
| 临床实验 | **临床试验** | `trial` 是试验，`experiment` 才是实验 |
| CE 认证 | **CE 标志** | CE 是标志（符合性评定），不是第三方"认证" |
| 不良事故 | **不良事件** | `adverse event` 规范译法 |
| 上市后监管 | **上市后监督** | `post-market surveillance` |
| 生产商 | **制造商** | `manufacturer` |
| ISO13485 | **ISO 13485** | 标准号原样保留，留空格 |

本技能把这些规则**做成了可执行检查**，而不是一份"请自行核对"的清单。

## 能力

```bash
# 术语速查（中英双向，子串匹配）
python scripts/term_check.py lookup biocompatibility
python scripts/term_check.py lookup 剩余风险

# 单文档体检：已知误译 + 标准号写法
python scripts/term_check.py check draft_zh.md

# 双语对照质检：警示语强度 / 情态动词 / 标准号一致性
python scripts/term_check.py pair ifu_en.md ifu_zh.md
```

双语质检会报出这类问题：

- 英文 `WARNING` ×3，中文只有 1 个「警告」→ **警示语漏译**
- 英文 `shall` 有 12 处，中文没有任何「应/须」→ **强制要求被弱化成建议**
- 英文 `CAUTION` 在中文里变成「提示」→ **警示强度被降级**
- 英文引了 `ISO 14971`，中文稿没有 → **标准号被翻译或省略**

## 数据规模

- 术语库 **164 条**（术语 135 / 标准号与法规名 19 / 警示级别 5 / 情态动词 5）
- 误译规则 **36 条**，每条带原因说明

## 使用须知（请注意）

- 术语库是**工作用精选表，不是官方术语标准**。涉及法规审评时，以适用国标/行标自身用语为准（如 ISO 13485 对应 GB/T 42061、ISO 14971 术语对应 YY/T 1437）。
- 双语质检是**计数对照**，不是逐句对齐——合理的句式重构可能触发提示，请当作"此处需复核"而非结论。
- 本技能**不做翻译**，只做质检。

## 许可

MIT。纯标准库实现，无第三方依赖，Python 3.9+。

---

由 [MedXpert](https://medxpert.cn) 出品 · 医疗器械法规与质量领域的 AI 专家团队