# API 配额问题解决方案

## 当前状态

✅ **程序运行正常** - 代码没有问题，可以正常执行
❌ **API 配额不足** - OpenAI API 账户需要充值

## 解决步骤

### 1. 检查账户状态

访问 OpenAI Platform：
- 网址：https://platform.openai.com/
- 登录您的账户
- 查看 "Billing" 或 "Usage" 页面

### 2. 充值账户

1. 进入 "Billing" 页面
2. 点击 "Add payment method" 或 "Add credits"
3. 添加支付方式并充值
4. 确保账户有足够余额

### 3. 验证配额

充值后，可以运行以下命令测试：

```bash
# 测试 API 连接（使用小 token 数）
python3 company_story.py "AAPL" --no-web --max-output-tokens 1000
```

## 程序已就绪

一旦配额充足，程序将自动：

1. ✅ 生成 Fact Pack（收集公司信息）
2. ✅ 生成文章（11 章结构）
3. ✅ 保存 Markdown 文件到 `output/` 目录
4. ✅ 保存来源 JSON 文件

## 运行示例（配额充足后）

```bash
# 基本使用
python3 company_story.py "LULU"

# 完整参数
python3 company_story.py "AAPL" \
  --model gpt-4o \
  --no-web \
  --market-days 30 \
  --max-output-tokens 8000
```

## 预期输出

运行成功后，您将看到：

```
============================================================
公司故事生成器
============================================================
公司标识: lulu
使用模型: gpt-4o
启用 web_search: False
新闻时间窗口: 90 天
最大输出 tokens: 4000
使用缓存: True
============================================================

正在生成 Fact Pack（公司：lulu）...
✓ Fact Pack 生成完成
正在生成文章...
✓ 文章生成完成
✓ 文章已保存: output/lulu_2024-01-15.md
✓ 来源文件已保存: output/lulu_2024-01-15_sources.json

============================================================
生成完成！
============================================================
```

## 注意事项

- 首次运行会调用 API，产生费用
- 使用 `--cache` 可以避免重复调用（默认开启）
- 使用 `--no-web` 可以节省成本
- 建议先用小 token 数测试（如 2000-4000）

## 如果仍有问题

1. 确认 API Key 正确：`echo $OPENAI_API_KEY`
2. 检查网络连接
3. 查看 OpenAI 平台的状态页面
4. 联系 OpenAI 支持

