# 使用说明

## 当前状态

程序已经可以正常运行！我已经做了以下修复：

1. ✅ 修复了 API 调用方式（使用标准的 Chat Completions API）
2. ✅ 修改默认模型为 `gpt-4o`（实际可用的模型）
3. ✅ 添加了模型自动回退机制
4. ✅ 改进了错误处理（区分配额错误和限流错误）
5. ✅ 添加了 `--model` 参数，允许指定模型

## 重要提示

### API 配额问题

如果遇到 "insufficient_quota" 错误，说明您的 OpenAI API 账户配额已用完。需要：
1. 登录 [OpenAI Platform](https://platform.openai.com/)
2. 检查账户余额和计费设置
3. 充值或升级计划

### 模型选择

- **默认模型**: `gpt-4o`（推荐，性价比高）
- **如需使用 gpt-5.2-thinking**: 使用 `--model gpt-5.2-thinking`，但需要确保有访问权限
- **其他可用模型**: `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`

## 使用示例

### 基本使用（使用默认模型 gpt-4o）

```bash
python3 company_story.py "LULU"
```

### 指定模型

```bash
# 使用 gpt-4-turbo
python3 company_story.py "AAPL" --model gpt-4-turbo

# 使用 gpt-5.2-thinking（如果可用）
python3 company_story.py "TSLA" --model gpt-5.2-thinking
```

### 关闭 web_search（节省成本）

```bash
python3 company_story.py "MSFT" --no-web
```

### 完整参数示例

```bash
python3 company_story.py "GOOGL" \
  --model gpt-4o \
  --no-web \
  --market-days 30 \
  --max-output-tokens 8000 \
  --no-cache
```

## 输出文件

程序会在 `output/` 目录生成：
- `{company}_{date}.md` - Markdown 格式的文章
- `{company}_{date}_sources.json` - 来源 JSON 文件

## 故障排除

### 问题：模型不存在
**解决**: 使用 `--model` 参数指定一个可用的模型，如 `gpt-4o`

### 问题：配额不足
**解决**: 检查并充值 OpenAI API 账户

### 问题：输出被截断
**解决**: 增加 `--max-output-tokens` 参数值

### 问题：需要更新缓存
**解决**: 使用 `--no-cache` 参数或删除 `cache/` 目录中的对应文件

