import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

MULTI_MONTH_CSV = """Timestamp,Date,Category,Description,Amount,Type
2026-09-15 10:00:00,2026-09-15,Food,Groceries,500,Expense
2026-09-20 12:00:00,2026-09-20,Shopping,Clothes,1200,Expense
2026-10-05 09:00:00,2026-10-05,Food,Restaurant,300,Expense
2026-10-15 15:00:00,2026-10-15,Bike Fuel,Petrol,150,Expense
2026-10-25 18:00:00,2026-10-25,Income,Salary,50000,Income
2026-11-02 11:00:00,2026-11-02,Food,Coffee,80,Expense
2026-11-10 14:00:00,2026-11-10,Shopping,Gadget,2500,Expense
"""

def test_upload_all_months():
    files = {"file": ("multi_month.csv", io.BytesIO(MULTI_MONTH_CSV.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload?month=all", files=files)
    assert response.status_code == 200
    data = response.json()
    meta = data["metadata"]
    assert meta["selected_month"] == "all"
    assert "2026-09" in meta["available_months"]
    assert "2026-10" in meta["available_months"]
    assert "2026-11" in meta["available_months"]
    assert meta["row_count"] == 7
    assert data["summary"]["total_income"] == 50000.0


def test_upload_filter_specific_month():
    files = {"file": ("multi_month.csv", io.BytesIO(MULTI_MONTH_CSV.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload?month=2026-10", files=files)
    assert response.status_code == 200
    data = response.json()
    meta = data["metadata"]
    assert meta["selected_month"] == "2026-10"
    assert meta["row_count"] == 3
    assert data["summary"]["total_income"] == 50000.0
    assert data["summary"]["total_expenses"] == 450.0  # 300 + 150


def test_upload_filter_invalid_month():
    files = {"file": ("multi_month.csv", io.BytesIO(MULTI_MONTH_CSV.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload?month=2025-01", files=files)
    assert response.status_code == 400
    assert "not present in the dataset" in response.json()["detail"]


def test_demo_with_month_filter():
    response = client.post("/api/upload/demo?month=2026-10")
    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["selected_month"] == "2026-10"
    assert "2026-10" in data["metadata"]["available_months"]

