---
name: reg-citation-normalizer
description: 医疗器械法规引用编号的识别、解析与规范化。将 21 CFR、ISO/IEC、中国国标行标（GB/YY/T）、NMPA 部令公告等各种写法解析为规范结构并给出标准书写建议。零依赖，可离线运行。适用于注册文档审校、IFU/技术文件编写、法规翻译一致性检查。
version: 1.0.0
license: MIT
metadata:
  author: StevenZhao26
  category: other
  tags:
  - medical-device
  - regulatory
  - citation
  - FDA
  - NMPA
  - ISO
permalink: workbuddy/2026-09-20-07-35-28/medxpert-skills/reg-citation-normalizer/skill
---

# reg-citation-normalizer

医疗器械法规引用编号识别与规范化工具。把文档里五花八门的法规引用写法，解析成规范结构并给出标准书写建议。

## 覆盖的引用类型

| 类型 | 示例输入 | 规范化输出 |
|------|---------|-----------|
| 美国 21 CFR | `21 CFR 820.30 (a)(6)` | `21 CFR 820.30(a)(6)` |
| ISO/IEC | `ISO 13485:2016 clause 7.5.1` | `ISO 13485:2016, 7.5.1` |
| 中国行标 | `YY/T 0287-2017 7.5.1` | `YY/T 0287-2017，第7.5.1条` |
| 部令 | `国家市场监督管理总局令第47号` | 机构归一化（含 SFDA→CFDA→NMPA 历史沿革） |
| 公告 | `国家药监局公告 2021年第76号` | `国家药监局公告 2021年第76号` |

## 使用方法

```bash
# 规范化（人读输出）
python scripts/cite_normalize.py normalize "21 CFR 820.30(a)(6)"

# 结构化解析（JSON）
python scripts/cite_normalize.py parse "ISO 13485:2016 clause 7.5.1" --json

# 批量检查文件中的引用书写问题（发现问题时 exit 1）
python scripts/cite_normalize.py check report.md

# 输出 JSON
python scripts/cite_normalize.py check report.md --json
```

## 勘误能力（check 模式）

- `ISO13485` → `ISO 13485`（代号与编号间缺空格）
- `iso 13485` → `ISO 13485`（代号应全大写）
- `YY/T0287` → `YY/T 0287`（代号与编号间缺空格）
- `21 CFR § 820.30` → `21 CFR 820.30`（CFR 官方写法无需 § 号）
- `21 CFR Part 820.30` → `21 CFR 820.30`（Part 后不应跟节号）
- `GB 9706.1:2020` → `GB 9706.1-2020`（中国标准年份用一字线不用冒号）
- ISO 引用具体条款未注日期 → 提示补年份（ISO/IEC Directives Part 2 §10.5）

## 典型工作流

1. **注册文档审校**：对 SRN/技术要求/CE 技术文件跑 `check`，发现引用书写不一致
2. **法规翻译**：中英对照时先 `parse --json` 拿到结构化引用，确保两边条款号对齐
3. **合规问答预处理**：从用户提问中提取法规引用，再做知识库精确检索

## 边界声明

- 本工具只做**格式识别与规范化**，不校验条款内容的正确性，不判断标准是否现行有效（查现行状态请用官方平台：openstd.samr.gov.cn / ecfr.gov / iso.org）
- 部令机构归一化基于历史沿革别名表，覆盖常见写法；极简写法（如"药监局令"）可能漏识
- 引用格式规则依据：ISO/IEC Directives Part 2 §10.4-10.5、GB/T 1.1-2020、GPO/eCFR 官方口径、NMPA 官网公告写法

## 环境要求

Python 3.8+，零第三方依赖。