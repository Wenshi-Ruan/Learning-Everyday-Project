# API 配额问题排查指南

## 当前诊断结果

您的 API key 遇到了配额限制问题，即使 billing 显示 spending 为 0。

## 可能的原因

### 1. 免费额度已用完
- OpenAI 新账户通常有 $5 免费额度
- 即使 spending 为 0，免费额度可能已用完
- 需要添加支付方式并充值

### 2. 账户需要验证
- 新账户可能需要验证身份
- 检查邮箱是否有验证邮件
- 在 Platform 设置中完成验证

### 3. 使用限制（Rate Limits）
- 账户可能有速率限制
- 检查 "Usage" 页面查看限制
- 可能需要等待一段时间

### 4. 组织/项目限制
- 如果使用组织账户，可能有组织级别的限制
- 检查组织设置

## 解决步骤

### 步骤 1: 检查账户状态

访问以下页面：
1. **Usage**: https://platform.openai.com/usage
   - 查看使用量和限制
   - 检查是否有错误提示

2. **Billing**: https://platform.openai.com/account/billing
   - 确认支付方式已添加
   - 检查账户余额
   - 查看账单历史

3. **Settings**: https://platform.openai.com/account/settings
   - 检查账户验证状态
   - 查看 API 访问权限

### 步骤 2: 添加支付方式

即使有免费额度，某些情况下也需要添加支付方式：
1. 进入 Billing 页面
2. 点击 "Add payment method"
3. 添加信用卡或 PayPal
4. 设置使用限制（可选）

### 步骤 3: 充值账户

1. 在 Billing 页面点击 "Add credits"
2. 选择充值金额（建议至少 $10）
3. 完成支付
4. 等待几分钟让系统更新

### 步骤 4: 验证 API Key

充值后，运行诊断脚本：

```bash
python3 diagnose_api.py "你的API_KEY"
```

### 步骤 5: 运行程序

如果诊断显示有可用模型，运行：

```bash
python3 company_story.py "LULU" --api-key "你的API_KEY"
```

## 临时解决方案

如果急需使用，可以考虑：

1. **使用其他 API 服务**
   - Anthropic Claude API
   - Google Gemini API
   - 需要修改代码适配

2. **使用本地模型**
   - Ollama
   - LM Studio
   - 需要修改代码适配

3. **等待配额重置**
   - 某些限制可能是按时间重置的
   - 等待 24 小时后再试

## 联系支持

如果以上步骤都无法解决：
1. 访问 OpenAI 支持页面
2. 提交支持工单
3. 说明情况：billing 显示 spending 为 0 但遇到配额错误

## 测试命令

一旦配额问题解决，使用以下命令测试：

```bash
# 测试 API key
python3 test_api_key.py "你的API_KEY"

# 诊断账户
python3 diagnose_api.py "你的API_KEY"

# 运行程序（小 token 数测试）
python3 company_story.py "AAPL" --api-key "你的API_KEY" --no-web --max-output-tokens 2000

# 正式运行
python3 company_story.py "LULU" --api-key "你的API_KEY"
```

