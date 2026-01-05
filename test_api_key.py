#!/usr/bin/env python3
"""
测试 OpenAI API Key
"""
import sys
from openai import OpenAI

def test_api_key(api_key: str):
    """测试 API Key 是否可用"""
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': 'Hello, just say "OK"'}],
            max_tokens=10
        )
        print('✓ API Key 测试成功！')
        print(f'响应: {response.choices[0].message.content}')
        return True
    except Exception as e:
        print(f'✗ API Key 测试失败: {e}')
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("请输入新的 OpenAI API Key: ").strip()
    
    if not api_key:
        print("错误：API Key 不能为空")
        sys.exit(1)
    
    print(f"\n正在测试 API Key: {api_key[:20]}...\n")
    
    if test_api_key(api_key):
        print("\n✓ API Key 可用！可以使用以下方式运行程序：")
        print(f"\n方式1: 使用命令行参数")
        print(f'python3 company_story.py "LULU" --api-key "{api_key}"')
        print(f"\n方式2: 设置环境变量（临时）")
        print(f'export OPENAI_API_KEY="{api_key}"')
        print(f'python3 company_story.py "LULU"')
        sys.exit(0)
    else:
        print("\n✗ API Key 不可用，请检查：")
        print("1. Key 是否正确")
        print("2. 账户是否有配额")
        print("3. 是否有模型访问权限")
        sys.exit(1)

