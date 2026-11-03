from typing import List, Optional
from pydantic import BaseModel, Field


class FinancialSummary(BaseModel):
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_balance: float = 0.0
    savings: float = 0.0
    savings_rate: float = 0.0
    transaction_count: int = 0
    average_transaction: float = 0.0
    highest_transaction: float = 0.0
    lowest_transaction: float = 0.0


class CategoryItem(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    percentage_of_total_expenses: float
    average_transaction: float


class TimeAnalysisItem(BaseModel):
    period: str
    income: float = 0.0
    expenses: float = 0.0
    savings: float = 0.0
    transaction_count: int = 0


class TimeAnalysis(BaseModel):
    daily: List[TimeAnalysisItem] = Field(default_factory=list)
    weekly: List[TimeAnalysisItem] = Field(default_factory=list)
    monthly: List[TimeAnalysisItem] = Field(default_factory=list)


class TrendItem(BaseModel):
    category: str
    current_period_amount: float
    previous_period_amount: float
    change_percent: float
    trend_direction: str  # "increasing", "decreasing", "stable", "new"


class UnusualExpense(BaseModel):
    date: str
    description: str
    amount: float
    category: str
    reason: str


class RecurringExpense(BaseModel):
    category: str
    description: str
    average_amount: float
    occurrence_count: int
    status: str = "possible_recurring"


class BehaviorFinding(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # "info", "positive", "warning"
    metric: Optional[str] = None


class RuleRecommendation(BaseModel):
    id: str
    category: str
    title: str
    message: str
    priority: str  # "high", "medium", "low"


class AIRecommendation(BaseModel):
    ai_financial_summary: str
    key_observation: str
    positive_behavior: str
    main_concern: str
    practical_recommendation: str
    short_term_action: str
    provider_used: str = "mock"
    is_fallback: bool = False


class FullAnalysisResponse(BaseModel):
    summary: FinancialSummary
    categories: List[CategoryItem]
    time_analysis: TimeAnalysis
    trends: List[TrendItem]
    unusual_expenses: List[UnusualExpense]
    recurring_expenses: List[RecurringExpense]
    behavior_findings: List[BehaviorFinding]
    rule_recommendations: List[RuleRecommendation]
    ai_recommendations: Optional[AIRecommendation] = None
    metadata: dict = Field(default_factory=dict)

