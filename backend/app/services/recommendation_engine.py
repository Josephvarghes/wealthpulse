from typing import List
from backend.app.schemas.analysis import (
    RuleRecommendation,
    FinancialSummary,
    CategoryItem,
    TrendItem,
    UnusualExpense,
    RecurringExpense,
)


class RecommendationThresholds:
    HIGH_CATEGORY_PERCENTAGE: float = 25.0
    CRITICAL_CATEGORY_PERCENTAGE: float = 40.0
    HIGH_GROWTH_PERCENTAGE: float = 20.0
    LOW_SAVINGS_RATE: float = 20.0
    CRITICAL_SAVINGS_RATE: float = 10.0


class RecommendationEngine:
    @staticmethod
    def generate_recommendations(
        summary: FinancialSummary,
        categories: List[CategoryItem],
        trends: List[TrendItem],
        unusual_expenses: List[UnusualExpense],
        recurring_expenses: List[RecurringExpense],
        thresholds: RecommendationThresholds = RecommendationThresholds(),
    ) -> List[RuleRecommendation]:
        """
        Generates deterministic, actionable rule-based recommendations.
        """
        recs: List[RuleRecommendation] = []

        # 1. Savings Rate Checks
        if summary.total_income > 0:
            if summary.savings_rate < thresholds.CRITICAL_SAVINGS_RATE:
                recs.append(
                    RuleRecommendation(
                        id="rec_boost_savings_critical",
                        category="Savings",
                        title="Establish a 20% Emergency Savings Target",
                        message=f"Current savings rate is {summary.savings_rate:.1f}%. Aim to build an emergency fund covering 3-6 months of essential living expenses by curtailing non-essential discretionary expenses.",
                        priority="high",
                    )
                )
            elif summary.savings_rate < thresholds.LOW_SAVINGS_RATE:
                recs.append(
                    RuleRecommendation(
                        id="rec_boost_savings_moderate",
                        category="Savings",
                        title="Target 20% Savings Benchmark",
                        message=f"Your savings rate is {summary.savings_rate:.1f}%. Diverting a further 5-10% of income into savings will significantly accelerate financial security.",
                        priority="medium",
                    )
                )
        elif summary.total_expenses > 0 and summary.total_income == 0:
            recs.append(
                RuleRecommendation(
                    id="rec_record_income",
                    category="Income",
                    title="Record Income Streams for Complete Cash Flow",
                    message="Only expense records were detected. Recording your salary or revenue will unlock net savings rates and cash-flow health metrics.",
                    priority="medium",
                )
            )

        # 2. High Category Concentration Checks
        for cat in categories:
            if cat.percentage_of_total_expenses >= thresholds.CRITICAL_CATEGORY_PERCENTAGE:
                recs.append(
                    RuleRecommendation(
                        id=f"rec_curtail_{cat.category.lower().replace(' ', '_')}",
                        category=cat.category,
                        title=f"Cap Discretionary Spending in {cat.category}",
                        message=f"{cat.category} takes up {cat.percentage_of_total_expenses:.1f}% of all expenses. Set a monthly sub-budget to prevent this category from crowding out other goals.",
                        priority="high",
                    )
                )
            elif cat.percentage_of_total_expenses >= thresholds.HIGH_CATEGORY_PERCENTAGE:
                recs.append(
                    RuleRecommendation(
                        id=f"rec_monitor_{cat.category.lower().replace(' ', '_')}",
                        category=cat.category,
                        title=f"Monitor {cat.category} Allocations",
                        message=f"{cat.category} accounts for {cat.percentage_of_total_expenses:.1f}% of outgoings. Audit upcoming planned purchases in this area.",
                        priority="medium",
                    )
                )

        # 3. Category Growth Checks
        for trend in trends:
            if trend.trend_direction == "increasing" and trend.change_percent >= thresholds.HIGH_GROWTH_PERCENTAGE:
                recs.append(
                    RuleRecommendation(
                        id=f"rec_growth_{trend.category.lower().replace(' ', '_')}",
                        category=trend.category,
                        title=f"Review Recent Spike in {trend.category}",
                        message=f"{trend.category} spending grew by {trend.change_percent:.1f}% period-over-period (₹{trend.current_period_amount:,.0f}). Check if this was a one-off necessity or lifestyle creep.",
                        priority="medium",
                    )
                )

        # 4. Outlier Transaction Checks
        if unusual_expenses:
            top_outlier = unusual_expenses[0]
            recs.append(
                RuleRecommendation(
                    id="rec_audit_outlier",
                    category=top_outlier.category,
                    title=f"Audit High-Value Transaction ({top_outlier.description})",
                    message=f"A transaction of ₹{top_outlier.amount:,.0f} occurred in {top_outlier.category}. If this is an annual/lump-sum bill (e.g. insurance or maintenance), consider setting aside a monthly sinking fund.",
                    priority="high" if top_outlier.amount >= 1000 else "medium",
                )
            )

        # 5. Recurring Subscriptions / Expenses
        if recurring_expenses:
            recs.append(
                RuleRecommendation(
                    id="rec_review_recurring",
                    category="Subscriptions",
                    title="Audit Recurring Commitments",
                    message=f"{len(recurring_expenses)} potentially recurring expense item(s) detected. Regularly evaluate whether all recurring subscriptions and automated payments continue to provide equivalent value.",
                    priority="low",
                )
            )

        return recs

