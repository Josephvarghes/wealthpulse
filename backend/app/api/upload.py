import os
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Query, HTTPException, status
from backend.app.services.file_processor import FileProcessor, FileProcessingError
from backend.app.services.finance_analyzer import FinanceAnalyzer
from backend.app.services.behavior_analyzer import BehaviorAnalyzer
from backend.app.services.recommendation_engine import RecommendationEngine
from backend.app.services.ai_service import AIService
from backend.app.schemas.analysis import FullAnalysisResponse

router = APIRouter(prefix="/api", tags=["Upload & Analysis"])
ai_service = AIService()


def execute_analysis_pipeline(
    df,
    source_filename: str,
    available_months: Optional[List[str]] = None,
    selected_month: str = "all",
    total_file_rows: Optional[int] = None,
) -> dict:
    # 1. Financial summary
    summary = FinanceAnalyzer.calculate_summary(df)

    # 2. Categories
    categories = FinanceAnalyzer.calculate_categories(df)

    # 3. Time analysis
    time_analysis = FinanceAnalyzer.calculate_time_analysis(df)

    # 4. Spending trends
    trends = FinanceAnalyzer.calculate_trends(df)

    # 5. Outliers / Unusual expenses
    unusual_expenses = FinanceAnalyzer.detect_unusual_expenses(df)

    # 6. Recurring expenses
    recurring_expenses = FinanceAnalyzer.detect_recurring_expenses(df)

    # 7. Analytical Behavior Findings
    behavior_findings = BehaviorAnalyzer.analyze_behavior(
        df=df,
        summary=summary,
        categories=categories,
        trends=trends,
        unusual_expenses=unusual_expenses,
    )

    # 8. Deterministic Rule Recommendations
    rule_recommendations = RecommendationEngine.generate_recommendations(
        summary=summary,
        categories=categories,
        trends=trends,
        unusual_expenses=unusual_expenses,
        recurring_expenses=recurring_expenses,
    )

    return {
        "summary": summary,
        "categories": categories,
        "time_analysis": time_analysis,
        "trends": trends,
        "unusual_expenses": unusual_expenses,
        "recurring_expenses": recurring_expenses,
        "behavior_findings": behavior_findings,
        "rule_recommendations": rule_recommendations,
        "metadata": {
            "filename": source_filename,
            "row_count": len(df),
            "total_file_rows": total_file_rows if total_file_rows is not None else len(df),
            "date_start": df["Date"].min() if not df.empty else None,
            "date_end": df["Date"].max() if not df.empty else None,
            "available_months": available_months or [],
            "selected_month": selected_month,
        },
    }


@router.post("/upload", response_model=FullAnalysisResponse)
async def upload_file(
    file: UploadFile = File(...),
    month: Optional[str] = Query(None, description="Optional month filter in YYYY-MM format (e.g. 2026-10) or 'all'"),
):
    """
    Accepts CSV or XLSX exported from Google Sheets, normalizes, validates,
    optionally filters by month, and computes financial analytics and recommendations.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    ext = file.filename.lower().split(".")[-1]
    if ext not in ["csv", "xlsx", "xls"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format (.{ext}). Only CSV and XLSX formats are supported.",
        )

    try:
        contents = await file.read()
        # Max file size 10MB
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum allowed limit (10MB).",
            )

        raw_df = FileProcessor.read_file(contents, file.filename)
        normalized_df, warnings = FileProcessor.validate_and_normalize(raw_df)

        available_months = sorted(normalized_df["Date"].str.slice(0, 7).unique().tolist())
        selected_month = month.strip() if month and month.strip().lower() != "all" else "all"

        if selected_month != "all":
            if selected_month in available_months:
                target_df = normalized_df[normalized_df["Date"].str.slice(0, 7) == selected_month].copy()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Requested month '{selected_month}' is not present in the dataset. Available months: {available_months}",
                )
        else:
            target_df = normalized_df

        pipeline_data = execute_analysis_pipeline(
            df=target_df,
            source_filename=file.filename,
            available_months=available_months,
            selected_month=selected_month,
            total_file_rows=len(normalized_df),
        )

        # AI Recommendations
        ai_recs = await ai_service.get_recommendations(
            summary=pipeline_data["summary"],
            categories=pipeline_data["categories"],
            trends=pipeline_data["trends"],
            unusual_expenses=pipeline_data["unusual_expenses"],
            behavior_findings=pipeline_data["behavior_findings"],
            rule_recommendations=pipeline_data["rule_recommendations"],
        )

        return FullAnalysisResponse(
            summary=pipeline_data["summary"],
            categories=pipeline_data["categories"],
            time_analysis=pipeline_data["time_analysis"],
            trends=pipeline_data["trends"],
            unusual_expenses=pipeline_data["unusual_expenses"],
            recurring_expenses=pipeline_data["recurring_expenses"],
            behavior_findings=pipeline_data["behavior_findings"],
            rule_recommendations=pipeline_data["rule_recommendations"],
            ai_recommendations=ai_recs,
            metadata=pipeline_data["metadata"],
        )

    except FileProcessingError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": e.message, "errors": e.errors},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing the file: {str(e)}",
        )


@router.post("/upload/demo", response_model=FullAnalysisResponse)
async def load_demo_data(
    month: Optional[str] = Query(None, description="Optional month filter in YYYY-MM format (e.g. 2026-10) or 'all'"),
):
    """
    Loads the official demo dataset specified in SDP Section 25 with optional month filtering.
    """
    demo_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "demo_data.csv")
    if not os.path.exists(demo_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo dataset not found.",
        )

    try:
        with open(demo_file_path, "rb") as f:
            file_bytes = f.read()

        raw_df = FileProcessor.read_file(file_bytes, "demo_data.csv")
        normalized_df, _ = FileProcessor.validate_and_normalize(raw_df)

        available_months = sorted(normalized_df["Date"].str.slice(0, 7).unique().tolist())
        selected_month = month.strip() if month and month.strip().lower() != "all" else "all"

        if selected_month != "all":
            if selected_month in available_months:
                target_df = normalized_df[normalized_df["Date"].str.slice(0, 7) == selected_month].copy()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Requested month '{selected_month}' is not present in the demo dataset. Available months: {available_months}",
                )
        else:
            target_df = normalized_df

        pipeline_data = execute_analysis_pipeline(
            df=target_df,
            source_filename="demo_data.csv (SDP Section 25)",
            available_months=available_months,
            selected_month=selected_month,
            total_file_rows=len(normalized_df),
        )

        ai_recs = await ai_service.get_recommendations(
            summary=pipeline_data["summary"],
            categories=pipeline_data["categories"],
            trends=pipeline_data["trends"],
            unusual_expenses=pipeline_data["unusual_expenses"],
            behavior_findings=pipeline_data["behavior_findings"],
            rule_recommendations=pipeline_data["rule_recommendations"],
        )

        return FullAnalysisResponse(
            summary=pipeline_data["summary"],
            categories=pipeline_data["categories"],
            time_analysis=pipeline_data["time_analysis"],
            trends=pipeline_data["trends"],
            unusual_expenses=pipeline_data["unusual_expenses"],
            recurring_expenses=pipeline_data["recurring_expenses"],
            behavior_findings=pipeline_data["behavior_findings"],
            rule_recommendations=pipeline_data["rule_recommendations"],
            ai_recommendations=ai_recs,
            metadata=pipeline_data["metadata"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load demo data: {str(e)}",
        )

