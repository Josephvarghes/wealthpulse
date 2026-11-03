import pandas as pd
import numpy as np
from typing import List, Dict, Any
from backend.app.schemas.analysis import (
    FinancialSummary,
    CategoryItem,
    TimeAnalysis,
    TimeAnalysisItem,
    TrendItem,
    UnusualExpense,
    RecurringExpense,
)


class FinanceAnalyzer:
    @staticmethod
    def calculate_summary(df: pd.DataFrame) -> FinancialSummary:
        """
        Calculates basic financial metrics:
        Income, expenses, savings, savings rate, counts, averages, min, max.
        """
        if df.empty:
            return FinancialSummary()

        income_df = df[df["Type"] == "Income"]
        expense_df = df[df["Type"] == "Expense"]

        total_income = float(income_df["Amount"].sum()) if not income_df.empty else 0.0
        total_expenses = float(expense_df["Amount"].sum()) if not expense_df.empty else 0.0

        savings = total_income - total_expenses
        net_balance = savings

        # Safe savings rate calculation
        if total_income > 0:
            savings_rate = round((savings / total_income) * 100, 2)
        else:
            savings_rate = 0.0

        tx_count = len(df)
        avg_tx = round(float(df["Amount"].mean()), 2) if tx_count > 0 else 0.0
        highest_tx = round(float(df["Amount"].max()), 2) if tx_count > 0 else 0.0
        lowest_tx = round(float(df["Amount"].min()), 2) if tx_count > 0 else 0.0

        return FinancialSummary(
            total_income=round(total_income, 2),
            total_expenses=round(total_expenses, 2),
            net_balance=round(net_balance, 2),
            savings=round(savings, 2),
            savings_rate=savings_rate,
            transaction_count=tx_count,
            average_transaction=avg_tx,
            highest_transaction=highest_tx,
            lowest_transaction=lowest_tx,
        )

    @staticmethod
    def calculate_categories(df: pd.DataFrame) -> List[CategoryItem]:
        """
        Calculates category breakdown for expenses.
        """
        expense_df = df[df["Type"] == "Expense"]
        if expense_df.empty:
            return []

        total_expense = float(expense_df["Amount"].sum())
        grouped = expense_df.groupby("Category").agg(
            total_amount=("Amount", "sum"),
            transaction_count=("Amount", "count"),
            average_transaction=("Amount", "mean"),
        ).reset_index()

        grouped = grouped.sort_values(by="total_amount", ascending=False)

        results = []
        for _, row in grouped.iterrows():
            cat_total = float(row["total_amount"])
            pct = round((cat_total / total_expense) * 100, 2) if total_expense > 0 else 0.0
            results.append(
                CategoryItem(
                    category=str(row["Category"]),
                    total_amount=round(cat_total, 2),
                    transaction_count=int(row["transaction_count"]),
                    percentage_of_total_expenses=pct,
                    average_transaction=round(float(row["average_transaction"]), 2),
                )
            )
        return results

    @staticmethod
    def calculate_time_analysis(df: pd.DataFrame) -> TimeAnalysis:
        """
        Calculates daily, weekly, and monthly spending and income breakdowns.
        """
        if df.empty:
            return TimeAnalysis()

        df_copy = df.copy()
        if "DateObj" not in df_copy.columns:
            df_copy["DateObj"] = pd.to_datetime(df_copy["Date"])

        # Daily aggregation
        daily_items = []
        daily_grp = df_copy.groupby("Date")
        for date_str, group in daily_grp:
            inc = float(group.loc[group["Type"] == "Income", "Amount"].sum())
            exp = float(group.loc[group["Type"] == "Expense", "Amount"].sum())
            daily_items.append(
                TimeAnalysisItem(
                    period=str(date_str),
                    income=round(inc, 2),
                    expenses=round(exp, 2),
                    savings=round(inc - exp, 2),
                    transaction_count=len(group),
                )
            )
        daily_items.sort(key=lambda x: x.period)

        # Weekly aggregation
        df_copy["Week"] = df_copy["DateObj"].dt.strftime("%Y-W%U")
        weekly_items = []
        weekly_grp = df_copy.groupby("Week")
        for week_str, group in weekly_grp:
            inc = float(group.loc[group["Type"] == "Income", "Amount"].sum())
            exp = float(group.loc[group["Type"] == "Expense", "Amount"].sum())
            weekly_items.append(
                TimeAnalysisItem(
                    period=str(week_str),
                    income=round(inc, 2),
                    expenses=round(exp, 2),
                    savings=round(inc - exp, 2),
                    transaction_count=len(group),
                )
            )
        weekly_items.sort(key=lambda x: x.period)

        # Monthly aggregation
        df_copy["Month"] = df_copy["DateObj"].dt.strftime("%Y-%m")
        monthly_items = []
        monthly_grp = df_copy.groupby("Month")
        for month_str, group in monthly_grp:
            inc = float(group.loc[group["Type"] == "Income", "Amount"].sum())
            exp = float(group.loc[group["Type"] == "Expense", "Amount"].sum())
            monthly_items.append(
                TimeAnalysisItem(
                    period=str(month_str),
                    income=round(inc, 2),
                    expenses=round(exp, 2),
                    savings=round(inc - exp, 2),
                    transaction_count=len(group),
                )
            )
        monthly_items.sort(key=lambda x: x.period)

        return TimeAnalysis(
            daily=daily_items,
            weekly=weekly_items,
            monthly=monthly_items,
        )

    @staticmethod
    def calculate_trends(df: pd.DataFrame) -> List[TrendItem]:
        """
        Detects category spending trends.
        If dataset spans multiple months, compares latest month to previous month.
        If single month or small dataset, splits by mid-date to detect emerging trends.
        """
        expense_df = df[df["Type"] == "Expense"].copy()
        if expense_df.empty:
            return []

        if "DateObj" not in expense_df.columns:
            expense_df["DateObj"] = pd.to_datetime(expense_df["Date"])

        months = sorted(expense_df["DateObj"].dt.strftime("%Y-%m").unique())

        if len(months) >= 2:
            curr_month = months[-1]
            prev_month = months[-2]
            curr_df = expense_df[expense_df["DateObj"].dt.strftime("%Y-%m") == curr_month]
            prev_df = expense_df[expense_df["DateObj"].dt.strftime("%Y-%m") == prev_month]
        else:
            # Fallback for short date range: split by median date
            median_date = expense_df["DateObj"].median()
            prev_df = expense_df[expense_df["DateObj"] < median_date]
            curr_df = expense_df[expense_df["DateObj"] >= median_date]

        categories = set(expense_df["Category"].unique())
        trends = []

        for cat in sorted(categories):
            curr_amt = float(curr_df.loc[curr_df["Category"] == cat, "Amount"].sum())
            prev_amt = float(prev_df.loc[prev_df["Category"] == cat, "Amount"].sum())

            if prev_amt == 0 and curr_amt > 0:
                change_pct = 100.0
                direction = "new"
            elif prev_amt > 0:
                change_pct = round(((curr_amt - prev_amt) / prev_amt) * 100, 2)
                if change_pct > 5.0:
                    direction = "increasing"
                elif change_pct < -5.0:
                    direction = "decreasing"
                else:
                    direction = "stable"
            else:
                change_pct = 0.0
                direction = "stable"

            trends.append(
                TrendItem(
                    category=cat,
                    current_period_amount=round(curr_amt, 2),
                    previous_period_amount=round(prev_amt, 2),
                    change_percent=change_pct,
                    trend_direction=direction,
                )
            )

        # Sort by highest spending first
        trends.sort(key=lambda t: t.current_period_amount, reverse=True)
        return trends

    @staticmethod
    def detect_unusual_expenses(df: pd.DataFrame) -> List[UnusualExpense]:
        """
        Rule-based statistical outlier detection for individual expenses.
        Flags transactions significantly higher than category or global average.
        """
        expense_df = df[df["Type"] == "Expense"].copy()
        if expense_df.empty:
            return []

        unusual = []
        global_mean = float(expense_df["Amount"].mean())
        global_std = float(expense_df["Amount"].std()) if len(expense_df) > 1 else 0.0
        global_threshold = global_mean + (1.5 * global_std if global_std > 0 else global_mean)

        # Category level means
        cat_stats = expense_df.groupby("Category")["Amount"].agg(["mean", "count"]).to_dict("index")

        for _, row in expense_df.iterrows():
            amt = float(row["Amount"])
            cat = str(row["Category"])
            desc = str(row["Description"])
            date_str = str(row["Date"])

            cat_info = cat_stats.get(cat, {"mean": amt, "count": 1})
            cat_mean = cat_info["mean"]
            cat_count = cat_info["count"]

            is_unusual = False
            reason = ""

            # Check if transaction is significantly higher than category average
            if cat_count >= 2 and amt > (cat_mean * 1.8) and amt > 300:
                is_unusual = True
                reason = f"Significantly higher than average for {cat} (₹{amt:,.0f} vs avg ₹{cat_mean:,.0f})"
            # Or if it is a major outlier globally
            elif amt > global_threshold and amt >= 500:
                is_unusual = True
                reason = f"Large transaction well above typical spending level (₹{amt:,.0f})"

            if is_unusual:
                unusual.append(
                    UnusualExpense(
                        date=date_str,
                        description=desc if desc else f"{cat} expense",
                        amount=round(amt, 2),
                        category=cat,
                        reason=reason,
                    )
                )

        unusual.sort(key=lambda x: x.amount, reverse=True)
        return unusual

    @staticmethod
    def detect_recurring_expenses(df: pd.DataFrame) -> List[RecurringExpense]:
        """
        Detects potential recurring expenses based on same/similar Category,
        Description, or exact repeated amounts.
        """
        expense_df = df[df["Type"] == "Expense"].copy()
        if expense_df.empty:
            return []

        recurring = []
        # Group by Category and Description (non-empty)
        with_desc = expense_df[expense_df["Description"].str.strip() != ""]
        if not with_desc.empty:
            grouped = with_desc.groupby(["Category", "Description"]).agg(
                count=("Amount", "count"),
                avg_amount=("Amount", "mean"),
                min_amount=("Amount", "min"),
                max_amount=("Amount", "max"),
            ).reset_index()

            for _, row in grouped.iterrows():
                cnt = int(row["count"])
                if cnt >= 2:
                    recurring.append(
                        RecurringExpense(
                            category=str(row["Category"]),
                            description=str(row["Description"]),
                            average_amount=round(float(row["avg_amount"]), 2),
                            occurrence_count=cnt,
                            status="possible_recurring",
                        )
                    )

        return recurring

