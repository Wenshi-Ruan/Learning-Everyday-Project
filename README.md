# 公司故事生成器

一个基于 OpenAI GPT-5.2 Thinking 模型的智能公司故事生成工具，能够自动生成杂志人物特写式的中文公司故事文章。

## 功能特点

- 🎯 **两阶段生成**：先收集事实（Fact Pack），再生成文章（Article）
- 📊 **数据可追溯**：所有关键数字和事实都有明确来源标注
- 🔍 **智能搜索**：支持 OpenAI 内置 web_search 工具（可开关）
- 💾 **结果缓存**：避免重复搜索，节省成本
- 📝 **严格结构**：按照 11 章模板输出，确保内容完整
- 📖 **深度内容**：每章都有足够的篇幅和深度分析，目标阅读时间约5分钟
- 💡 **洞察力强**：不仅描述事实，更提供"为什么"和"意味着什么"的深度分析

## 安装

```bash
pip install -r requirements.txt
```

## 配置

设置环境变量 `OPENAI_API_KEY`：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

或在 `.env` 文件中配置（需要安装 python-dotenv）。

## 使用方法

### 基本用法

```bash
# 使用股票代码
python company_story.py "LULU"

# 使用公司名
python company_story.py "lululemon"

# 交互式输入
python company_story.py
```

### 高级参数

```bash
# 关闭 web_search（节省成本，但可能信息过时）
python company_story.py "AAPL" --no-web

# 控制新闻时间窗口（默认 90 天）
python company_story.py "TSLA" --market-days 30

# 设置最大输出 token 数（默认 16000，支持约5分钟阅读时间）
python company_story.py "MSFT" --max-output-tokens 20000

# 启用缓存（默认开启）
python company_story.py "GOOGL" --cache

# 禁用缓存
python company_story.py "GOOGL" --no-cache
```

## 输出文件

程序会在 `output/` 目录下生成两个文件：

1. **Markdown 文章**：`{company}_{YYYY-MM-DD}.md`
   - 包含完整的 11 章公司故事
   - 正文中使用脚注式引用：`（来源：[#12]）`
   - 文末包含完整的 Sources 列表

2. **来源文件**：`{company}_{YYYY-MM-DD}_sources.json`
   - JSON 格式，包含所有事实的来源信息
   - 每条来源包含：id、title、url、publisher、日期、引用位置等

## 示例

### 生成 Lululemon 公司故事

```bash
python company_story.py "LULU"
```

输出：
- `output/lululemon_2024-01-15.md`
- `output/lululemon_2024-01-15_sources.json`

### 生成 Apple 公司故事（不使用 web_search）

```bash
python company_story.py "AAPL" --no-web
```

## 注意事项

### 成本控制

- **web_search 成本**：启用 web_search 会增加 API 调用成本，建议：
  - 使用 `--cache` 避免重复搜索同一公司
  - 使用 `--no-web` 关闭搜索（但信息可能过时）
  - 缓存文件保存在 `cache/` 目录，可按需清理

### 数据可靠性

- 所有关键数字和事实都会标注来源
- 如果无法核实，文章会明确标注"未能核实/暂无可靠来源"
- 建议在使用 `--no-web` 时，检查生成的关键词提示，手动验证重要信息

### API 限制

- 模型 `gpt-5.2-thinking` 需要 OpenAI API 访问权限
- 如果遇到限流，程序会自动重试（最多 3 次）
- 推理强度 `reasoning={"effort":"high"}` 可能需要较长时间

### 常见问题

**Q: 提示 "模型不支持 reasoning 参数"？**  
A: 程序会自动降级，使用标准调用方式，不影响功能。

**Q: 输出被截断？**  
A: 增加 `--max-output-tokens` 参数值，或检查模型的最大输出限制。

**Q: 缓存文件在哪里？**  
A: `cache/` 目录下，格式为 `{ticker}_{date}.json`。

**Q: 如何更新已缓存的公司信息？**  
A: 删除对应的缓存文件，或使用 `--no-cache` 参数。

## 项目结构

```
.
├── company_story.py    # 主入口文件
├── prompts.py          # 提示词模板
├── schemas.py          # 数据模型定义
├── utils.py            # 工具函数
├── requirements.txt    # 依赖包
├── README.md           # 本文件
├── output/             # 输出目录（自动创建）
└── cache/              # 缓存目录（自动创建）
```

## 许可证

MIT License

