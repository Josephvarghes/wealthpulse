import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import httpx
from backend.app.schemas.analysis import (
    FinancialSummary,
    CategoryItem,
    TrendItem,
    UnusualExpense,
    BehaviorFinding,
    RuleRecommendation,
    AIRecommendation,
)
from backend.app.config import get_settings

logger = logging.getLogger(__name__)


def build_compact_ai_context(
    summary: FinancialSummary,
    categories: List[CategoryItem],
    trends: List[TrendItem],
    unusual_expenses: List[UnusualExpense],
    behavior_findings: List[BehaviorFinding],
    rule_recommendations: List[RuleRecommendation],
) -> Dict[str, Any]:
    """
    Constructs a small structured context object strictly adhering to Section 18 of SDP.
    Never includes raw transaction lines.
    """
    top_categories = [
        {
            "name": c.category,
            "amount": c.total_amount,
            "percentage": c.percentage_of_total_expenses,
        }
        for c in categories[:5]
    ]

    # Map trends to top categories if available
    trend_map = {t.category: t.change_percent for t in trends}
    for cat in top_categories:
        if cat["name"] in trend_map:
            cat["change_percent"] = trend_map[cat["name"]]

    return {
        "income": summary.total_income,
        "expenses": summary.total_expenses,
        "savings": summary.savings,
        "savings_rate": summary.savings_rate,
        "top_categories": top_categories,
        "behavior_findings": [b.title + ": " + b.description for b in behavior_findings[:5]],
        "unusual_expenses": [
            {"category": u.category, "amount": u.amount, "reason": u.reason}
            for u in unusual_expenses[:3]
        ],
        "rule_recommendations": [r.title for r in rule_recommendations[:4]],
    }


SYSTEM_PROMPT = """You are a personal finance analysis assistant.
Analyze only the structured financial data provided.
The numbers have already been calculated by the application. Do not recalculate or invent financial values.
Explain the user's financial behavior clearly.

You must respond in valid JSON matching this exact structure:
{
  "ai_financial_summary": "1-2 sentence overall summary of cash flow and health.",
  "key_observation": "The single most important observation from the numbers.",
  "positive_behavior": "A positive financial discipline observed (or prudent tracking noted).",
  "main_concern": "The primary area of financial risk or spending leakage.",
  "practical_recommendation": "One practical, realistic recommendation based strictly on the data.",
  "short_term_action": "One immediate next step the user can take today or this week."
}

Do not provide guaranteed financial outcomes. Keep responses concise and realistic. Do not invent transactions.
"""


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_recommendations(self, context: Dict[str, Any]) -> Optional[AIRecommendation]:
        pass


class MockAIProvider(BaseAIProvider):
    """
    Local fallback provider used when no API key is provided or network is offline.
    Adheres strictly to the SDP schema without requiring remote API access.
    """
    async def generate_recommendations(self, context: Dict[str, Any]) -> Optional[AIRecommendation]:
        income = context.get("income", 0.0)
        expenses = context.get("expenses", 0.0)
        top_cats = context.get("top_categories", [])
        top_cat_name = top_cats[0]["name"] if top_cats else "General"
        top_cat_pct = top_cats[0]["percentage"] if top_cats else 0.0

        if income > 0:
            savings_rate = context.get("savings_rate", 0.0)
            summary_txt = f"Out of ₹{income:,.0f} income, you spent ₹{expenses:,.0f}, preserving a {savings_rate:.1f}% savings rate."
            positive = f"Maintaining a positive savings margin while tracking daily expenses."
        else:
            summary_txt = f"Recorded expenses total ₹{expenses:,.0f} across {len(top_cats)} categories."
            positive = "Consistently tracking expenses at a granular level creates clear visibility."

        unusual = context.get("unusual_expenses", [])
        if unusual:
            outlier = unusual[0]
            concern = f"A high-value transaction in {outlier['category']} (₹{outlier['amount']:,.0f}) drove up total outflows."
            action = f"Review the ₹{outlier['amount']:,.0f} expense in {outlier['category']} and create a dedicated sinking fund."
        else:
            concern = f"{top_cat_name} constitutes {top_cat_pct:.1f}% of total spending, representing the primary cash outflow."
            action = f"Set a spending limit for {top_cat_name} for the next 7 days."

        return AIRecommendation(
            ai_financial_summary=summary_txt,
            key_observation=f"Spending is heavily concentrated in {top_cat_name} ({top_cat_pct:.1f}% of total).",
            positive_behavior=positive,
            main_concern=concern,
            practical_recommendation=f"Review your top spending category ({top_cat_name}) and audit smaller discretionary items.",
            short_term_action=action,
            provider_used="mock",
            is_fallback=True,
        )


class GroqProvider(BaseAIProvider):
    """
    Ultra-fast LLM inference using Groq API (OpenAI compatible endpoint).
    """
    def __init__(self, api_key: str, model: str = "qwen/qwen3.8-27b"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    async def generate_recommendations(self, context: Dict[str, Any]) -> Optional[AIRecommendation]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        # Candidate models to try in case of model_not_found / deprecation
        candidate_models = [self.model]
        for fallback in ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "llama-3.3-70b-versatile"]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        async with httpx.AsyncClient(timeout=15.0) as client:
            last_exception = None
            for model_candidate in candidate_models:
                payload = {
                    "model": model_candidate,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Structured Financial Context:\n{json.dumps(context, indent=2)}"},
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.2,
                    "max_tokens": 600,
                }
                try:
                    response = await client.post(self.endpoint, headers=headers, json=payload)
                    if response.status_code == 404 and "model_not_found" in response.text:
                        logger.warning(f"Groq model '{model_candidate}' not found, trying next available model.")
                        continue
                    response.raise_for_status()
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)

                    return AIRecommendation(
                        ai_financial_summary=parsed.get("ai_financial_summary", "Summary unavailable."),
                        key_observation=parsed.get("key_observation", "No observation available."),
                        positive_behavior=parsed.get("positive_behavior", "Consistent tracking."),
                        main_concern=parsed.get("main_concern", "Review high expense items."),
                        practical_recommendation=parsed.get("practical_recommendation", "Track all outgoings daily."),
                        short_term_action=parsed.get("short_term_action", "Audit top category expenses."),
                        provider_used=f"groq ({model_candidate})",
                        is_fallback=False,
                    )
                except httpx.HTTPStatusError as e:
                    last_exception = e
                    if e.response.status_code == 404:
                        continue
                    raise
                except Exception as e:
                    last_exception = e
                    raise

            if last_exception:
                raise last_exception
            return None


class GrokProvider(BaseAIProvider):
    """
    xAI Grok provider.
    """
    def __init__(self, api_key: str, model: str = "grok-beta"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.x.ai/v1/chat/completions"

    async def generate_recommendations(self, context: Dict[str, Any]) -> Optional[AIRecommendation]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Structured Financial Context:\n{json.dumps(context, indent=2)}"},
            ],
            "temperature": 0.2,
            "max_tokens": 600,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            # Parse json from markdown fences if any
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            parsed = json.loads(content)

            return AIRecommendation(
                ai_financial_summary=parsed.get("ai_financial_summary", "Summary unavailable."),
                key_observation=parsed.get("key_observation", "No observation available."),
                positive_behavior=parsed.get("positive_behavior", "Consistent tracking."),
                main_concern=parsed.get("main_concern", "Review high expense items."),
                practical_recommendation=parsed.get("practical_recommendation", "Track all outgoings daily."),
                short_term_action=parsed.get("short_term_action", "Audit top category expenses."),
                provider_used=f"grok ({self.model})",
                is_fallback=False,
            )


class AIService:
    """
    Service abstraction orchestrating AI recommendation generation with graceful fallback.
    """
    def __init__(self):
        self.settings = get_settings()
        self.mock_provider = MockAIProvider()

    def _get_configured_provider(self) -> BaseAIProvider:
        # Check Groq
        if self.settings.GROQ_API_KEY and self.settings.AI_PROVIDER.lower() in ["groq", "all"]:
            return GroqProvider(self.settings.GROQ_API_KEY, self.settings.GROQ_MODEL)
        # Check xAI Grok
        if self.settings.XAI_API_KEY and self.settings.AI_PROVIDER.lower() in ["grok", "xai"]:
            return GrokProvider(self.settings.XAI_API_KEY, self.settings.XAI_MODEL)

        # Fallback to Mock provider
        return self.mock_provider

    async def get_recommendations(
        self,
        summary: FinancialSummary,
        categories: List[CategoryItem],
        trends: List[TrendItem],
        unusual_expenses: List[UnusualExpense],
        behavior_findings: List[BehaviorFinding],
        rule_recommendations: List[RuleRecommendation],
    ) -> AIRecommendation:
        context = build_compact_ai_context(
            summary=summary,
            categories=categories,
            trends=trends,
            unusual_expenses=unusual_expenses,
            behavior_findings=behavior_findings,
            rule_recommendations=rule_recommendations,
        )

        provider = self._get_configured_provider()
        try:
            result = await provider.generate_recommendations(context)
            if result:
                return result
        except Exception as e:
            logger.warning(f"AI Provider call failed: {e}. Falling back to rule-based explainer.", exc_info=True)

        # Graceful fallback per Section 22
        fallback_res = await self.mock_provider.generate_recommendations(context)
        return fallback_res or AIRecommendation(
            ai_financial_summary="Financial analysis completed. AI recommendations are temporarily unavailable.",
            key_observation="Calculated metrics are available in the dashboard charts.",
            positive_behavior="Data successfully loaded and validated.",
            main_concern="Ensure all expenses and incomes are recorded.",
            practical_recommendation="Review the category distributions above.",
            short_term_action="Check the highest spending categories.",
            provider_used="system_fallback",
            is_fallback=True,
        )

