---
title: README
type: note
permalink: workbuddy/2026-09-20-07-35-28/medxpert-skills/reg-citation-normalizer/readme
---

# reg-citation-normalizer

医疗器械法规引用编号识别与规范化（Medical device regulatory citation normalizer）。

把 `21 CFR 820.30(a)(6)`、`ISO 13485:2016 clause 7.5.1`、`YY/T 0287-2017 7.5.1`、
`国家市场监督管理总局令第47号` 等各种写法，解析为规范结构并输出标准书写建议。

## 快速开始

```bash
python scripts/cite_normalize.py normalize "产品符合 ISO 13485:2016 clause 7.5.1 和 21 CFR 820.30 要求"
python scripts/cite_normalize.py parse "YY/T 0287-2017 7.5.1" --json
python scripts/cite_normalize.py check 你的文档.md
```

输出示例：

```
21 CFR 820.30  →  21 CFR 820.30
ISO 13485:2016 clause 7.5.1  →  ISO 13485:2016, 7.5.1
```

## 特性

- **四类文法**：美国 21 CFR / ISO·IEC / 中国国标行标（GB·YY·GB/T·YY/T 等）/ NMPA 部令公告
- **机构归一化**：SFDA → CFDA → NMPA 历史沿革别名表
- **勘误建议**：缺空格、大小写、§ 误用、年份连接符、注日期规则等 9 类常见书写问题
- **批量检查**：对整份文档跑 `check`，逐行定位问题，CI 可用（exit 1）
- **零依赖**：纯 Python 标准库，离线可用

## 规则依据

| 法域 | 规则出处 |
|------|---------|
| ISO/IEC | ISO/IEC Directives Part 2, clauses 10.4–10.5（注日期引用 `ISO 12345:2018, 4.3.9`） |
| 中国国标行标 | GB/T 1.1-2020（`代号 顺序号-年份`，一字线连接） |
| 美国 CFR | GPO / eCFR 官方引用口径（`title CFR part.section`） |
| NMPA 部令 | 官方写法 = 发布机关全称 + 令 + 第N号 |

## 与 MedXpert 系列技能的关系

- `udi-validator`：UDI 编码解析校验
- `medxpert-termbase`：中英术语对照
- `iso14971-risk-matrix`：风险管理矩阵
- `reg-citation-normalizer`：法规引用规范化（本工具）

## License

MIT