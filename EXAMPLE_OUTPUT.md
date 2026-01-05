# 示例输出格式

本文档展示程序生成的输出格式示例。

## Markdown 文章示例（部分）

```markdown
# Lululemon 公司故事

## Open remarks（开篇导语）

在温哥华的一个瑜伽工作室里，一位名叫 Chip Wilson 的创业者发现了一个问题：传统的运动服在瑜伽练习中不够舒适，也不够时尚。这个简单的观察，催生了一个价值数百亿美元的运动休闲品牌——Lululemon（来源：[#1]）。

...

## Key financial driver（关键财务驱动因素）

根据公司最新财报，Lululemon 在 2023 财年的营收达到 81.1 亿美元（来源：[#12]），较上年增长 19%（来源：[#13]）。这一增长主要得益于...

**近 5 年关键财务指标**

| 指标 | 2023 | 2022 | 2021 | 2020 | 2019 |
|------|------|------|------|------|------|
| 营收（亿美元） | 81.1 | 68.1 | 58.3 | 44.0 | 39.7 |
| 净利润（亿美元） | 8.5 | 7.5 | 5.9 | 5.5 | 6.5 |

*数据来源：公司财报（来源：[#12], [#14], [#15]）*

...

## Sources

[#1] Lululemon 公司历史 — 公司官网 — 2023-01-15 — https://www.lululemon.com/about-us
[#2] Chip Wilson 创业故事 — Forbes — 2022-05-20 — https://...
[#3] Lululemon 2023 年财报 — SEC Filing — 2023-03-28 — https://...
...
```

## Sources JSON 示例

```json
{
  "company": "lululemon",
  "generated_at": "2024-01-15T10:30:00",
  "sources": [
    {
      "id": 1,
      "title": "Lululemon 公司历史",
      "url": "https://www.lululemon.com/about-us",
      "publisher": "Lululemon 官网",
      "published_date": null,
      "accessed_date": "2024-01-15",
      "used_for": ["company.founded_year", "timeline"]
    },
    {
      "id": 2,
      "title": "Lululemon 2023 Q4 财报",
      "url": "https://investor.lululemon.com/news-releases",
      "publisher": "Lululemon Investor Relations",
      "published_date": "2024-01-10",
      "accessed_date": "2024-01-15",
      "used_for": ["financials.revenue", "financials.net_income"]
    }
  ]
}
```

## 关键特性

1. **引用格式**：正文中使用 `（来源：[#12]）` 格式标注来源
2. **Sources 章节**：文章末尾自动生成完整的来源列表
3. **JSON 映射**：sources.json 文件包含所有来源的详细信息
4. **数据可追溯**：每个关键数字都能在 sources 中找到对应来源

