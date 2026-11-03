import pandas as pd
from typing import List
from backend.app.schemas.analysis import (
    BehaviorFinding,
    FinancialSummary,
    CategoryItem,
    TrendItem,
    UnusualExpense,
)


class BehaviorAnalyzer:
    @staticmethod
    def analyze_behavior(
        df: pd.DataFrame,
        summary: FinancialSummary,
        categories: List[CategoryItem],
        trends: List[TrendItem],
        unusual_expenses: List[UnusualExpense],
    ) -> List[BehaviorFinding]:
        """
        Analyzes deterministic behavioral patterns based purely on calculated data.
        Returns a list of structured findings.
        """
        findings: List[BehaviorFinding] = []

        if df.empty:
            return findings

        expense_df = df[df["Type"] == "Expense"].copy()
        if "DateObj" not in expense_df.columns:
            expense_df["DateObj"] = pd.to_datetime(expense_df["Date"])

        total_expense = summary.total_expenses

        # 1. Savings Behavior
        if summary.total_income > 0:
            if summary.savings_rate >= 30:
                findings.append(
                    BehaviorFinding(
                        id="healthy_savings_rate",
                        title="Strong Savings Discipline",
                        description=f"Your savings rate is {summary.savings_rate:.1f}%, which comfortably exceeds the standard 20% benchmark.",
                        severity="positive",
                        metric=f"{summary.savings_rate:.1f}%",
                    )
                )
            elif summary.savings_rate < 15 and summary.savings_rate >= 0:
                findings.append(
                    BehaviorFinding(
                        id="low_savings_rate",
                        title="Narrow Savings Buffer",
                        description=f"Your current savings rate is {summary.savings_rate:.1f}%. Increasing your buffer will protect against unexpected costs.",
                        severity="warning",
                        metric=f"{summary.savings_rate:.1f}%",
                    )
                )
            elif summary.savings < 0:
                findings.append(
                    BehaviorFinding(
                        id="negative_savings",
                        title="Spending Exceeds Income",
                        description=f"Expenses surpass total recorded income by ₹{abs(summary.savings):,.0f}. Immediate expense trimming recommended.",
                        severity="warning",
                        metric=f"-₹{abs(summary.savings):,.0f}",
                    )
                )

        # 2. Dominant Spending Categories (> 30% of total expenses)
        for cat in categories:
            if cat.percentage_of_total_expenses >= 30:
                findings.append(
                    BehaviorFinding(
                        id=f"dominant_cat_{cat.category.lower().replace(' ', '_')}",
                        title=f"High {cat.category} Concentration",
                        description=f"{cat.category} accounts for {cat.percentage_of_total_expenses:.1f}% of your total spending (₹{cat.total_amount:,.0f} across {cat.transaction_count} transactions).",
                        severity="warning" if cat.percentage_of_total_expenses >= 45 else "info",
                        metric=f"{cat.percentage_of_total_expenses:.1f}%",
                    )
                )

        # 3. Fast-Growing Expense Categories (> 20% increase)
        for trend in trends:
            if trend.trend_direction == "increasing" and trend.change_percent >= 20.0 and trend.current_period_amount >= 200:
                findings.append(
                    BehaviorFinding(
                        id=f"growing_cat_{trend.category.lower().replace(' ', '_')}",
                        title=f"Rising {trend.category} Outflow",
                        description=f"{trend.category} spending increased by {trend.change_percent:.1f}% compared to the prior period.",
                        severity="warning",
                        metric=f"+{trend.change_percent:.1f}%",
                    )
                )

        # 4. Weekend vs Weekday Spending Behavior
        if not expense_df.empty:
            expense_df["DayOfWeek"] = expense_df["DateObj"].dt.dayofweek
            is_weekend = expense_df["DayOfWeek"].isin([5, 6])
            weekend_total = float(expense_df.loc[is_weekend, "Amount"].sum())
            weekday_total = float(expense_df.loc[~is_weekend, "Amount"].sum())

            weekend_days = expense_df.loc[is_weekend, "Date"].nunique() or 1
            weekday_days = expense_df.loc[~is_weekend, "Date"].nunique() or 1

            weekend_daily_avg = weekend_total / weekend_days if weekend_days > 0 else 0
            weekday_daily_avg = weekday_total / weekday_days if weekday_days > 0 else 0

            if weekend_daily_avg > (weekday_daily_avg * 1.5) and weekend_total > 0 and weekday_total > 0:
                findings.append(
                    BehaviorFinding(
                        id="weekend_spending_surge",
                        title="Weekend Spending Spike",
                        description=f"Daily spending averages ₹{weekend_daily_avg:,.0f} on weekends compared to ₹{weekday_daily_avg:,.0f} on weekdays.",
                        severity="info",
                        metric=f"₹{weekend_daily_avg:,.0f}/day",
                    )
                )

        # 5. Frequent Small Transactions (< ₹100)
        if not expense_df.empty:
            small_tx = expense_df[expense_df["Amount"] <= 100]
            if len(small_tx) >= 4:
                small_sum = float(small_tx["Amount"].sum())
                pct_small = (len(small_tx) / len(expense_df)) * 100
                findings.append(
                    BehaviorFinding(
                        id="micro_transactions",
                        title="Frequent Micro-Expenses",
                        description=f"{len(small_tx)} small transactions under ₹100 total ₹{small_sum:,.0f} ({pct_small:.0f}% of all transactions). These small daily leaks accumulate quickly.",
                        severity="info",
                        metric=f"{len(small_tx)} txs",
                    )
                )

        # 6. Outlier / Unusual Spikes
        if unusual_expenses:
            top_unusual = unusual_expenses[0]
            findings.append(
                BehaviorFinding(
                    id="unusual_spike_detected",
                    title="Significant Outlier Transaction",
                    description=f"₹{top_unusual.amount:,.0f} spent on '{top_unusual.description}' in {top_unusual.category} represents an unusual peak in your records.",
                    severity="warning",
                    metric=f"₹{top_unusual.amount:,.0f}",
                )
            )

        return findings

