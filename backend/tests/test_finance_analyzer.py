import pytest
from backend.app.services.file_processor import FileProcessor
from backend.app.services.finance_analyzer import FinanceAnalyzer


def test_finance_summary_expense_only(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    summary = FinanceAnalyzer.calculate_summary(norm_df)
    # 80 + 309 + 54 + 100 + 27 + 30 + 1000 = 1600
    assert summary.total_expenses == 1600.0
    assert summary.total_income == 0.0
    assert summary.savings == -1600.0
    assert summary.savings_rate == 0.0
    assert summary.transaction_count == 7
    assert summary.highest_transaction == 1000.0
    assert summary.lowest_transaction == 27.0


def test_finance_summary_with_income(demo_income_csv_bytes):
    df = FileProcessor.read_file(demo_income_csv_bytes, "income.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    summary = FinanceAnalyzer.calculate_summary(norm_df)
    assert summary.total_income == 15000.0
    assert summary.total_expenses == 1600.0
    assert summary.savings == 13400.0
    assert summary.savings_rate == round((13400.0 / 15000.0) * 100, 2)


def test_category_breakdown(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    categories = FinanceAnalyzer.calculate_categories(norm_df)
    assert len(categories) > 0
    # Bike Maintance should be highest: 80 + 1000 = 1080 (67.5%)
    bike_maint = next(c for c in categories if c.category == "Bike Maintance")
    assert bike_maint.total_amount == 1080.0
    assert bike_maint.transaction_count == 2
    assert bike_maint.percentage_of_total_expenses == round((1080 / 1600) * 100, 2)


def test_time_analysis(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    time_analysis = FinanceAnalyzer.calculate_time_analysis(norm_df)
    assert len(time_analysis.daily) == 2  # 10/27 and 10/28
    assert len(time_analysis.monthly) == 1  # 2026-10


def test_unusual_expense_detection(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    unusual = FinanceAnalyzer.detect_unusual_expenses(norm_df)
    # The 1000 Splendour insurance expense should be flagged
    assert len(unusual) >= 1
    assert any(u.amount == 1000.0 for u in unusual)

