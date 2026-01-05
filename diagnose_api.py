#!/usr/bin/env python3
"""
诊断 OpenAI API 账户状态
"""
import sys
from openai import OpenAI
from datetime import datetime

def diagnose_api(api_key: str):
    """诊断 API 账户状态"""
    print("=" * 60)
    print("OpenAI API 诊断工具")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    client = OpenAI(api_key=api_key)
    
    # 1. 测试基本连接
    print("1. 测试 API 连接...")
    try:
        # 尝试获取模型列表（如果 API 支持）
        print("   尝试获取账户信息...")
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
    
    # 2. 测试不同模型
    print("\n2. 测试可用模型...")
    models = [
        ('gpt-3.5-turbo', '基础模型'),
        ('gpt-4', 'GPT-4'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
        ('gpt-4o', 'GPT-4o'),
        ('gpt-4o-mini', 'GPT-4o Mini')
    ]
    
    available_models = []
    for model, desc in models:
        try:
            print(f"   测试 {model} ({desc})...", end=' ')
            response = client.chat.completions.create(
                model=model,
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=1
            )
            print("✓ 可用")
            available_models.append(model)
        except Exception as e:
            error_str = str(e).lower()
            if 'quota' in error_str or '429' in error_str or 'insufficient' in error_str:
                print("✗ 配额不足")
            elif 'not found' in error_str or '404' in error_str or 'invalid' in error_str:
                print("✗ 模型不可用/无权限")
            elif 'rate limit' in error_str:
                print("✗ 速率限制")
            else:
                print(f"✗ 错误: {str(e)[:50]}")
    
    # 3. 总结
    print("\n" + "=" * 60)
    print("诊断结果:")
    print("=" * 60)
    
    if available_models:
        print(f"✓ 可用模型: {', '.join(available_models)}")
        print(f"\n建议使用以下命令运行程序:")
        print(f'python3 company_story.py "LULU" --api-key "{api_key[:20]}..." --model {available_models[0]}')
    else:
        print("✗ 没有可用的模型")
        print("\n可能的原因:")
        print("1. 账户配额已用完（即使 billing 显示 spending 为 0）")
        print("2. 账户有使用限制或需要验证")
        print("3. API key 权限不足")
        print("\n建议:")
        print("1. 检查 OpenAI Platform: https://platform.openai.com/usage")
        print("2. 检查账户设置和限制")
        print("3. 联系 OpenAI 支持")
        print("4. 尝试创建新的 API key")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("请输入 OpenAI API Key: ").strip()
    
    if not api_key:
        print("错误：API Key 不能为空")
        sys.exit(1)
    
    diagnose_api(api_key)

