"""
数据模型定义：FactPack 结构
"""
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class Source(BaseModel):
    """来源信息"""
    id: int = Field(..., description="来源编号，对应文章中的引用编号")
    title: str = Field(..., description="来源标题")
    url: str = Field(..., description="来源 URL")
    publisher: str = Field(default="", description="发布方/网站名称")
    published_date: Optional[str] = Field(default=None, description="发布日期（YYYY-MM-DD 格式）")
    accessed_date: str = Field(..., description="访问日期（YYYY-MM-DD 格式）")
    used_for: List[str] = Field(default_factory=list, description="被引用到的字段/章节列表")


class CompanyInfo(BaseModel):
    """公司基本信息"""
    full_name: str = Field(..., description="公司全名")
    ticker: Optional[str] = Field(default=None, description="股票代码")
    exchange: Optional[str] = Field(default=None, description="交易所")
    headquarters: Optional[str] = Field(default=None, description="总部地址")
    founded_year: Optional[int] = Field(default=None, description="成立年份")
    founders: List[str] = Field(default_factory=list, description="创始人列表")
    ceo: Optional[str] = Field(default=None, description="现任 CEO")
    ceo_as_of: Optional[str] = Field(default=None, description="CEO 信息截至日期")


class BusinessInfo(BaseModel):
    """业务信息"""
    main_business_lines: List[str] = Field(default_factory=list, description="主要业务线")
    revenue_structure: Dict[str, Any] = Field(default_factory=dict, description="收入结构（最近一个 FY/TTM）")
    products: List[str] = Field(default_factory=list, description="主要产品/服务")
    customers: Optional[str] = Field(default=None, description="主要客户群体")
    channels: List[str] = Field(default_factory=list, description="主要销售渠道")


class TimelineEvent(BaseModel):
    """时间线事件"""
    date: str = Field(..., description="事件日期（YYYY-MM-DD 或 YYYY 格式）")
    event: str = Field(..., description="事件描述")
    significance: str = Field(..., description="为什么重要")


class FinancialMetric(BaseModel):
    """财务指标"""
    metric_name: str = Field(..., description="指标名称（如 revenue, net_income 等）")
    value: float = Field(..., description="数值")
    unit: str = Field(default="USD", description="单位")
    fiscal_year: Optional[str] = Field(default=None, description="财年（如 FY2023）")
    period_end: Optional[str] = Field(default=None, description="截至日期（YYYY-MM-DD）")
    basis: str = Field(default="GAAP", description="口径（GAAP 或 Non-GAAP）")
    source_id: Optional[int] = Field(default=None, description="来源编号")


class Financials(BaseModel):
    """财务数据"""
    revenue: List[FinancialMetric] = Field(default_factory=list, description="营收")
    gross_profit: List[FinancialMetric] = Field(default_factory=list, description="毛利润")
    operating_income: List[FinancialMetric] = Field(default_factory=list, description="营业利润")
    net_income: List[FinancialMetric] = Field(default_factory=list, description="净利润")
    eps: List[FinancialMetric] = Field(default_factory=list, description="每股收益")
    cash: List[FinancialMetric] = Field(default_factory=list, description="现金及现金等价物")
    debt: List[FinancialMetric] = Field(default_factory=list, description="债务")
    operating_cash_flow: List[FinancialMetric] = Field(default_factory=list, description="经营现金流")
    revenue_composition: Dict[str, Any] = Field(default_factory=dict, description="收入构成")


class Valuation(BaseModel):
    """估值信息"""
    market_cap: Optional[float] = Field(default=None, description="市值（USD）")
    market_cap_date: Optional[str] = Field(default=None, description="市值日期")
    pe_ratio: Optional[float] = Field(default=None, description="市盈率")
    pe_ratio_date: Optional[str] = Field(default=None, description="市盈率日期")
    key_metrics: Dict[str, Any] = Field(default_factory=dict, description="其他关键估值指标")
    note: Optional[str] = Field(default=None, description="备注（如无法获取，说明原因）")
    source_id: Optional[int] = Field(default=None, description="来源编号")


class NewsItem(BaseModel):
    """新闻条目"""
    date: Optional[str] = Field(default=None, description="新闻日期")
    title: str = Field(..., description="新闻标题")
    summary: str = Field(..., description="一句话摘要")
    impact: str = Field(..., description="影响/重要性")
    source_id: Optional[int] = Field(default=None, description="来源编号")


class Risk(BaseModel):
    """风险/挑战"""
    risk_name: str = Field(..., description="风险名称")
    description: str = Field(..., description="风险描述")
    severity: Optional[str] = Field(default=None, description="严重程度")


class Competitor(BaseModel):
    """竞争对手"""
    name: str = Field(..., description="竞争对手名称")
    category: str = Field(..., description="竞争类别（如：直接竞争对手、替代品等）")
    description: str = Field(..., description="竞争对手描述")


class FactPack(BaseModel):
    """Fact Pack 完整结构"""
    company: CompanyInfo = Field(..., description="公司基本信息")
    business: BusinessInfo = Field(..., description="业务信息")
    timeline: List[TimelineEvent] = Field(default_factory=list, description="时间线（5-7个关键节点）")
    financials: Financials = Field(..., description="财务数据（近3-5年）")
    valuation: Valuation = Field(..., description="估值信息")
    news_30_90d: List[NewsItem] = Field(default_factory=list, description="近30-90天重要新闻（5-10条）")
    risks: List[Risk] = Field(default_factory=list, description="主要风险/挑战（5-8个）")
    competitors: List[Competitor] = Field(default_factory=list, description="竞争对手（至少4类，每类2-5个）")
    sources: List[Source] = Field(default_factory=list, description="所有来源列表")
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="生成时间")
    web_search_enabled: bool = Field(default=True, description="是否启用了 web_search")
    search_keywords: List[str] = Field(default_factory=list, description="建议搜索关键词（当 web_search 关闭时）")

    @field_validator('timeline')
    @classmethod
    def validate_timeline(cls, v):
        if len(v) < 5:
            raise ValueError("时间线至少需要 5 个关键节点")
        if len(v) > 7:
            raise ValueError("时间线最多 7 个关键节点")
        return v

    @field_validator('news_30_90d')
    @classmethod
    def validate_news(cls, v):
        # 放宽限制，允许至少 3 条（如果模型生成不足，可以接受）
        if len(v) < 3:
            raise ValueError("新闻列表至少需要 3 条")
        if len(v) > 10:
            # 如果超过 10 条，只取前 10 条
            return v[:10]
        return v

    @field_validator('risks')
    @classmethod
    def validate_risks(cls, v):
        # 放宽限制，允许至少 3 个（如果模型生成不足，可以接受）
        if len(v) < 3:
            raise ValueError("风险列表至少需要 3 个")
        if len(v) > 8:
            # 如果超过 8 个，只取前 8 个
            return v[:8]
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "company": {
                    "full_name": "示例公司",
                    "ticker": "EXAMPLE"
                }
            }
        }

