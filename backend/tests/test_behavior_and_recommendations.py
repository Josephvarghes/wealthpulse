import pytest
from backend.app.services.file_processor import FileProcessor
from backend.app.services.finance_analyzer import FinanceAnalyzer
from backend.app.services.behavior_analyzer import BehaviorAnalyzer
from backend.app.services.recommendation_engine import RecommendationEngine


def test_behavior_and_recommendations(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    norm_df, _ = FileProcessor.validate_and_normalize(df)

    summary = FinanceAnalyzer.calculate_summary(norm_df)
    categories = FinanceAnalyzer.calculate_categories(norm_df)
    trends = FinanceAnalyzer.calculate_trends(norm_df)
    unusual = FinanceAnalyzer.detect_unusual_expenses(norm_df)
    recurring = FinanceAnalyzer.detect_recurring_expenses(norm_df)

    findings = BehaviorAnalyzer.analyze_behavior(
        df=norm_df,
        summary=summary,
        categories=categories,
        trends=trends,
        unusual_expenses=unusual,
    )
    assert len(findings) > 0

    recs = RecommendationEngine.generate_recommendations(
        summary=summary,
        categories=categories,
        trends=trends,
        unusual_expenses=unusual,
        recurring_expenses=recurring,
    )
    assert len(recs) > 0
    # Bike Maintance is > 40%, should have a recommendation
    assert any(r.category == "Bike Maintance" for r in recs)
    # Outlier transaction recommendation
    assert any("Audit High-Value Transaction" in r.title for r in recs)

