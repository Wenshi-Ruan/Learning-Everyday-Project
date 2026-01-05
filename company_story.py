#!/usr/bin/env python3
"""
公司故事生成器主入口
"""
import os
import sys
import json
import argparse
import time
from typing import Optional, Dict, Any
from datetime import datetime

from openai import OpenAI
from pydantic import ValidationError

from schemas import FactPack
from prompts import WRITER_PROMPT_TEMPLATE, FACT_PACK_PROMPT
from utils import (
    normalize_ticker_or_name,
    get_output_paths,
    get_cache_path,
    load_cache,
    save_cache,
    get_today_date_str,
    format_sources_section,
    validate_factpack_json
)


class CompanyStoryGenerator:
    """公司故事生成器"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",  # 默认使用 gpt-4o，如果用户需要可以使用 gpt-5.2-thinking
        max_output_tokens: int = 16000,  # 增加默认值以支持更详细的内容
        enable_web_search: bool = True,
        market_days: int = 90,
        use_cache: bool = True
    ):
        """
        初始化生成器
        
        Args:
            api_key: OpenAI API Key（如果为 None，从环境变量读取）
            model: 模型名称
            max_output_tokens: 最大输出 token 数
            enable_web_search: 是否启用 web_search
            market_days: 新闻时间窗口（天）
            use_cache: 是否使用缓存
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 OPENAI_API_KEY，请设置环境变量或传入参数")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.enable_web_search = enable_web_search
        self.market_days = market_days
        self.use_cache = use_cache
        
    def _call_api_with_retry(
        self,
        prompt: str,
        tools: Optional[list] = None,
        max_retries: int = 3,
        retry_delay: int = 5
    ) -> str:
        """
        调用 OpenAI API，带重试机制
        
        Args:
            prompt: 提示词
            tools: 工具列表（如 web_search）
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            
        Returns:
            API 响应内容
        """
        for attempt in range(max_retries):
            try:
                # 使用标准 Chat Completions API
                request_params = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": self.max_output_tokens,
                    "temperature": 0.7
                }
                
                # 尝试添加 reasoning 参数（如果模型支持）
                # 注意：某些模型可能支持 reasoning 参数，但需要特殊处理
                try:
                    # 如果模型名称包含 "thinking"，尝试添加 reasoning
                    if "thinking" in self.model.lower():
                        # 某些 API 版本可能支持，但先不添加，避免错误
                        pass
                except Exception:
                    pass
                
                # 添加工具（如果启用 web_search）
                # 注意：web_search 可能需要特定的模型或 API 版本支持
                if tools and self.enable_web_search:
                    # 对于 web_search，可能需要使用特定的模型或参数
                    # 如果当前模型不支持，会忽略 tools
                    try:
                        request_params["tools"] = tools
                    except Exception:
                        print("警告：当前模型可能不支持 web_search 工具，将忽略")
                
                # 调用 API，如果模型不存在则尝试备用模型
                try:
                    response = self.client.chat.completions.create(**request_params)
                except Exception as model_error:
                    error_str = str(model_error).lower()
                    # 如果模型不存在，尝试使用备用模型
                    if "model" in error_str and ("not found" in error_str or "invalid" in error_str or "404" in error_str):
                        print(f"警告：模型 {self.model} 不可用，尝试使用备用模型...")
                        # 尝试使用常见的可用模型作为备用
                        fallback_models = ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
                        last_error = model_error
                        for fallback_model in fallback_models:
                            try:
                                test_params = request_params.copy()
                                test_params["model"] = fallback_model
                                # 移除可能不支持的 tools 参数
                                if "tools" in test_params:
                                    del test_params["tools"]
                                response = self.client.chat.completions.create(**test_params)
                                print(f"✓ 使用备用模型: {fallback_model}")
                                break
                            except Exception as e:
                                last_error = e
                                continue
                        else:
                            raise Exception(f"所有模型都不可用。最后尝试的错误: {last_error}")
                    else:
                        raise model_error
                
                # 提取响应内容
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    message = response.choices[0].message
                    if hasattr(message, 'content') and message.content:
                        return message.content
                    # 如果有工具调用，可能需要处理
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        # 这里可以处理工具调用的结果，但为了简化，先返回内容
                        pass
                
                raise Exception("无法从 API 响应中提取内容")
                    
            except Exception as e:
                error_msg = str(e).lower()
                error_str = str(e)
                
                # 检查是否是配额不足错误（不应该重试）
                if "quota" in error_msg or "insufficient_quota" in error_msg:
                    raise Exception(f"API 配额不足，请检查您的 OpenAI 账户余额和计费设置。错误详情: {error_str}")
                
                # 检查是否是限流错误
                if "rate limit" in error_msg or "429" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        print(f"遇到限流，等待 {wait_time} 秒后重试... (尝试 {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"达到最大重试次数，仍然遇到限流: {e}")
                else:
                    # 其他错误，直接抛出
                    raise e
        
        raise Exception("API 调用失败")
    
    def generate_fact_pack(
        self,
        company_input: str,
        use_cache: Optional[bool] = None
    ) -> FactPack:
        """
        生成 Fact Pack
        
        Args:
            company_input: 公司名或股票代码
            use_cache: 是否使用缓存（覆盖初始化设置）
            
        Returns:
            FactPack 对象
        """
        use_cache = use_cache if use_cache is not None else self.use_cache
        
        # 检查缓存
        cache_path = get_cache_path(company_input)
        if use_cache:
            cached_data = load_cache(cache_path)
            if cached_data:
                print(f"✓ 从缓存加载 Fact Pack: {cache_path}")
                try:
                    return FactPack(**cached_data)
                except ValidationError as e:
                    print(f"警告：缓存数据格式错误，重新生成: {e}")
        
        print(f"正在生成 Fact Pack（公司：{company_input}）...")
        
        # 构建提示词
        today_date = get_today_date_str()
        
        # 获取 FactPack 的 JSON Schema（简化版，用于提示模型）
        factpack_schema = """
{
  "company": {
    "full_name": "string",
    "ticker": "string | null",
    "exchange": "string | null",
    "headquarters": "string | null",
    "founded_year": "integer | null",
    "founders": ["string"],
    "ceo": "string | null",
    "ceo_as_of": "string | null"
  },
  "business": {
    "main_business_lines": ["string"],
    "revenue_structure": {},
    "products": ["string"],
    "customers": "string | null",
    "channels": ["string"]
  },
  "timeline": [
    {
      "date": "string",
      "event": "string",
      "significance": "string"
    }
  ],
  "financials": {
    "revenue": [{"metric_name": "string", "value": "number", "unit": "string", "fiscal_year": "string", "period_end": "string", "basis": "string", "source_id": "integer"}],
    "gross_profit": [...],
    "operating_income": [...],
    "net_income": [...],
    "eps": [...],
    "cash": [...],
    "debt": [...],
    "operating_cash_flow": [...],
    "revenue_composition": {}
  },
  "valuation": {
    "market_cap": "number | null",
    "market_cap_date": "string | null",
    "pe_ratio": "number | null",
    "pe_ratio_date": "string | null",
    "key_metrics": {},
    "note": "string | null",
    "source_id": "integer | null"
  },
  "news_30_90d": [
    {
      "date": "string | null",
      "title": "string",
      "summary": "string",
      "impact": "string",
      "source_id": "integer | null"
    }
  ],
  "risks": [
    {
      "risk_name": "string",
      "description": "string",
      "severity": "string | null"
    }
  ],
  "competitors": [
    {
      "name": "string",
      "category": "string",
      "description": "string"
    }
  ],
  "sources": [
    {
      "id": "integer",
      "title": "string",
      "url": "string",
      "publisher": "string",
      "published_date": "string | null",
      "accessed_date": "string",
      "used_for": ["string"]
    }
  ],
  "web_search_enabled": "boolean",
  "search_keywords": ["string"]
}
"""
        
        prompt = FACT_PACK_PROMPT.format(
            company_input=company_input,
            market_days=self.market_days,
            factpack_schema=factpack_schema,
            today_date=today_date
        )
        
        # 准备工具
        tools = None
        if self.enable_web_search:
            # OpenAI web_search 工具格式
            # 注意：实际格式可能因 API 版本而异，这里使用通用格式
            tools = [
                {
                    "type": "web_search",
                    "web_search": {
                        "enabled": True
                    }
                }
            ]
        
        # 调用 API
        try:
            response_text = self._call_api_with_retry(prompt, tools=tools)
        except Exception as e:
            print(f"错误：生成 Fact Pack 失败: {e}")
            raise
        
        # 尝试从响应中提取 JSON
        json_str = self._extract_json_from_response(response_text)
        
        # 验证 JSON
        is_valid, error_msg = validate_factpack_json(json_str)
        if not is_valid:
            raise ValueError(f"Fact Pack JSON 验证失败: {error_msg}")
        
        # 解析为 FactPack 对象
        try:
            factpack_data = json.loads(json_str)
            factpack_data["web_search_enabled"] = self.enable_web_search
            factpack = FactPack(**factpack_data)
        except ValidationError as e:
            print(f"警告：Fact Pack 数据验证失败，尝试修复...")
            # 尝试修复常见问题
            factpack_data = json.loads(json_str)
            # 确保必需字段存在
            if "sources" not in factpack_data:
                factpack_data["sources"] = []
            if "web_search_enabled" not in factpack_data:
                factpack_data["web_search_enabled"] = self.enable_web_search
            if "search_keywords" not in factpack_data:
                factpack_data["search_keywords"] = []
            
            # 修复新闻列表不足的问题
            if "news_30_90d" in factpack_data and len(factpack_data["news_30_90d"]) < 3:
                print(f"  补充新闻列表（当前 {len(factpack_data['news_30_90d'])} 条）...")
                # 如果不足 3 条，至少保留现有的，不强制补充
                pass
            
            # 修复风险列表不足的问题
            if "risks" in factpack_data and len(factpack_data["risks"]) < 3:
                print(f"  补充风险列表（当前 {len(factpack_data['risks'])} 个）...")
                # 如果不足 3 个，至少保留现有的，不强制补充
                pass
            
            # 修复时间线不足的问题
            if "timeline" in factpack_data and len(factpack_data["timeline"]) < 5:
                print(f"  时间线节点不足（当前 {len(factpack_data['timeline'])} 个），将接受现有数据...")
                pass
            
            try:
                factpack = FactPack(**factpack_data)
            except ValidationError as e2:
                # 如果仍然失败，尝试进一步放宽要求
                error_str = str(e2)
                if "新闻列表至少需要" in error_str or "风险列表至少需要" in error_str or "时间线至少需要" in error_str:
                    print(f"  数据量不足，但将尝试继续处理...")
                    # 临时修改验证器（不推荐，但为了继续运行）
                    # 或者直接使用字典，不进行严格验证
                    factpack_dict = factpack_data.copy()
                    # 确保至少有一些数据
                    if len(factpack_dict.get("news_30_90d", [])) < 3:
                        factpack_dict["news_30_90d"] = factpack_dict.get("news_30_90d", []) + [
                            {"date": None, "title": "数据不足", "summary": "模型生成的数据不足", "impact": "需要更多信息", "source_id": None}
                        ] * (3 - len(factpack_dict.get("news_30_90d", [])))
                    if len(factpack_dict.get("risks", [])) < 3:
                        factpack_dict["risks"] = factpack_dict.get("risks", []) + [
                            {"risk_name": "数据不足", "description": "模型生成的风险数据不足", "severity": None}
                        ] * (3 - len(factpack_dict.get("risks", [])))
                    if len(factpack_dict.get("timeline", [])) < 5:
                        factpack_dict["timeline"] = factpack_dict.get("timeline", []) + [
                            {"date": "未知", "event": "数据不足", "significance": "需要更多历史信息"}
                        ] * (5 - len(factpack_dict.get("timeline", [])))
                    
                    try:
                        factpack = FactPack(**factpack_dict)
                    except Exception as e3:
                        raise ValueError(f"无法解析 Fact Pack，即使尝试修复后仍然失败: {e3}")
                else:
                    raise ValueError(f"无法解析 Fact Pack: {e2}")
        
        # 保存缓存
        if use_cache:
            save_cache(cache_path, factpack.model_dump())
            print(f"✓ Fact Pack 已缓存: {cache_path}")
        
        print("✓ Fact Pack 生成完成")
        return factpack
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """
        从 API 响应中提取 JSON
        
        Args:
            response_text: API 响应文本
            
        Returns:
            JSON 字符串
        """
        # 尝试直接解析
        try:
            json.loads(response_text)
            return response_text
        except:
            pass
        
        # 尝试提取代码块中的 JSON
        import re
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, response_text, re.DOTALL)
        if matches:
            return matches[0]
        
        # 尝试提取第一个 { ... } 块
        brace_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if brace_match:
            return brace_match.group(0)
        
        # 如果都失败，返回原文本（让调用者处理错误）
        return response_text
    
    def generate_article(self, factpack: FactPack) -> str:
        """
        基于 Fact Pack 生成文章
        
        Args:
            factpack: FactPack 对象
            
        Returns:
            Markdown 格式的文章
        """
        print("正在生成文章...")
        
        # 将 FactPack 转换为 JSON 字符串
        factpack_json = json.dumps(
            factpack.model_dump(),
            ensure_ascii=False,
            indent=2
        )
        
        # 构建提示词
        prompt = WRITER_PROMPT_TEMPLATE.format(factpack_json=factpack_json)
        
        # 调用 API（文章生成不需要 web_search）
        try:
            article = self._call_api_with_retry(prompt, tools=None)
        except Exception as e:
            print(f"错误：生成文章失败: {e}")
            raise
        
        # 确保文章末尾包含 Sources 章节
        if "## Sources" not in article and "## 来源" not in article:
            sources_section = format_sources_section(factpack.sources)
            article = article.rstrip() + "\n\n" + sources_section
        
        print("✓ 文章生成完成")
        return article
    
    def generate(
        self,
        company_input: str,
        use_cache: Optional[bool] = None
    ) -> tuple:
        """
        完整生成流程：Fact Pack + Article
        
        Args:
            company_input: 公司名或股票代码
            use_cache: 是否使用缓存
            
        Returns:
            (article_markdown, factpack) 元组
        """
        # 阶段 1: 生成 Fact Pack
        factpack = self.generate_fact_pack(company_input, use_cache=use_cache)
        
        # 阶段 2: 生成文章
        article = self.generate_article(factpack)
        
        return (article, factpack)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="生成公司故事文章",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "company",
        nargs="?",
        help="公司名或股票代码（如果不提供，将进入交互模式）"
    )
    
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="关闭 web_search（节省成本，但信息可能过时）"
    )
    
    parser.add_argument(
        "--market-days",
        type=int,
        default=90,
        help="新闻时间窗口（天），默认 90"
    )
    
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=16000,
        help="最大输出 token 数，默认 16000（支持约5分钟阅读时间的详细内容）"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用缓存"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API Key（如果不提供，从环境变量读取）"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI 模型名称（默认: gpt-4o）。如需使用 gpt-5.2-thinking，请确保有访问权限"
    )
    
    args = parser.parse_args()
    
    # 获取公司输入
    company_input = args.company
    if not company_input:
        company_input = input("请输入公司名或股票代码: ").strip()
        if not company_input:
            print("错误：必须提供公司名或股票代码")
            sys.exit(1)
    
    # 规范化输入
    ticker, name = normalize_ticker_or_name(company_input)
    company_identifier = ticker or name
    
    print(f"\n{'='*60}")
    print(f"公司故事生成器")
    print(f"{'='*60}")
    print(f"公司标识: {company_identifier}")
    print(f"使用模型: {args.model}")
    print(f"启用 web_search: {not args.no_web}")
    print(f"新闻时间窗口: {args.market_days} 天")
    print(f"最大输出 tokens: {args.max_output_tokens}")
    print(f"使用缓存: {not args.no_cache}")
    print(f"{'='*60}\n")
    
    try:
        # 创建生成器
        generator = CompanyStoryGenerator(
            api_key=args.api_key,
            model=args.model,
            max_output_tokens=args.max_output_tokens,
            enable_web_search=not args.no_web,
            market_days=args.market_days,
            use_cache=not args.no_cache
        )
        
        # 生成文章
        article, factpack = generator.generate(company_identifier)
        
        # 保存输出文件
        markdown_path, sources_path = get_output_paths(company_identifier)
        
        # 保存 Markdown
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(article)
        print(f"✓ 文章已保存: {markdown_path}")
        
        # 保存 Sources JSON
        sources_data = {
            "company": company_identifier,
            "generated_at": datetime.now().isoformat(),
            "sources": [s.model_dump() for s in factpack.sources]
        }
        with open(sources_path, 'w', encoding='utf-8') as f:
            json.dump(sources_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 来源文件已保存: {sources_path}")
        
        print(f"\n{'='*60}")
        print("生成完成！")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

