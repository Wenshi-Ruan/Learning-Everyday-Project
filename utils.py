"""
工具函数
"""
import re
import os
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Tuple


def sanitize_filename(name: str) -> str:
    """
    清洗文件名，移除非法字符
    
    Args:
        name: 原始文件名
        
    Returns:
        清洗后的文件名
    """
    # 移除或替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # 移除前后空格
    name = name.strip()
    # 如果为空，使用默认值
    if not name:
        name = "unknown"
    return name.lower()


def normalize_ticker_or_name(input_str: str) -> Tuple[str, str]:
    """
    规范化股票代码或公司名
    
    Args:
        input_str: 用户输入的股票代码或公司名
        
    Returns:
        (ticker, name) 元组，如果无法确定则为 (None, normalized_name)
    """
    input_str = input_str.strip().upper()
    
    # 常见股票代码模式（1-5个大写字母+可选数字）
    ticker_pattern = re.match(r'^[A-Z]{1,5}\d?$', input_str)
    if ticker_pattern:
        return (input_str, input_str)
    
    # 否则当作公司名处理
    return (None, input_str.lower())


def get_output_paths(company_identifier: str, base_dir: str = "output") -> Tuple[str, str]:
    """
    生成输出文件路径
    
    Args:
        company_identifier: 公司标识（ticker 或 name）
        base_dir: 输出目录
        
    Returns:
        (markdown_path, sources_json_path) 元组
    """
    today = date.today().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(company_identifier)
    
    # 创建输出目录
    Path(base_dir).mkdir(exist_ok=True)
    
    markdown_path = os.path.join(base_dir, f"{safe_name}_{today}.md")
    sources_path = os.path.join(base_dir, f"{safe_name}_{today}_sources.json")
    
    return (markdown_path, sources_path)


def get_cache_path(ticker_or_name: str, base_dir: str = "cache") -> str:
    """
    生成缓存文件路径
    
    Args:
        ticker_or_name: 股票代码或公司名
        base_dir: 缓存目录
        
    Returns:
        缓存文件路径
    """
    today = date.today().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(ticker_or_name)
    
    # 创建缓存目录
    Path(base_dir).mkdir(exist_ok=True)
    
    return os.path.join(base_dir, f"{safe_name}_{today}.json")


def load_cache(cache_path: str) -> Optional[dict]:
    """
    加载缓存文件
    
    Args:
        cache_path: 缓存文件路径
        
    Returns:
        缓存的 FactPack 数据，如果不存在则返回 None
    """
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"警告：加载缓存失败：{e}")
        return None


def save_cache(cache_path: str, data: dict) -> bool:
    """
    保存缓存文件
    
    Args:
        cache_path: 缓存文件路径
        data: 要缓存的数据
        
    Returns:
        是否保存成功
    """
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"警告：保存缓存失败：{e}")
        return False


def get_today_date_str() -> str:
    """
    获取今天的日期字符串（YYYY-MM-DD）
    
    Returns:
        日期字符串
    """
    return date.today().strftime("%Y-%m-%d")


def format_sources_section(sources: list) -> str:
    """
    格式化 Sources 章节的 Markdown 文本
    
    Args:
        sources: Source 对象列表或字典列表
        
    Returns:
        格式化的 Markdown 文本
    """
    lines = ["## Sources", ""]
    
    # 按 id 排序
    sorted_sources = sorted(sources, key=lambda x: x.get('id', 0) if isinstance(x, dict) else x.id)
    
    for source in sorted_sources:
        if isinstance(source, dict):
            source_id = source.get('id', '?')
            title = source.get('title', '未知标题')
            publisher = source.get('publisher', '未知发布方')
            published_date = source.get('published_date', '未知日期')
            url = source.get('url', '#')
        else:
            source_id = getattr(source, 'id', '?')
            title = getattr(source, 'title', '未知标题')
            publisher = getattr(source, 'publisher', '未知发布方')
            published_date = getattr(source, 'published_date', '未知日期') or '未知日期'
            url = getattr(source, 'url', '#')
        
        line = f"[#{source_id}] {title} — {publisher} — {published_date} — {url}"
        lines.append(line)
    
    return "\n".join(lines)


def validate_factpack_json(json_str: str) -> Tuple[bool, Optional[str]]:
    """
    验证 FactPack JSON 字符串的基本结构
    
    Args:
        json_str: JSON 字符串
        
    Returns:
        (is_valid, error_message) 元组
    """
    try:
        data = json.loads(json_str)
        
        # 检查必需字段
        required_fields = ['company', 'business', 'financials', 'valuation', 'sources']
        for field in required_fields:
            if field not in data:
                return (False, f"缺少必需字段: {field}")
        
        return (True, None)
    except json.JSONDecodeError as e:
        return (False, f"JSON 格式错误: {e}")
    except Exception as e:
        return (False, f"验证失败: {e}")

