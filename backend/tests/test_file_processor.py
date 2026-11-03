import io
import pytest
import pandas as pd
from backend.app.services.file_processor import FileProcessor, FileProcessingError


def test_valid_csv_processing(demo_csv_bytes):
    df = FileProcessor.read_file(demo_csv_bytes, "demo.csv")
    assert len(df) == 7
    norm_df, warnings = FileProcessor.validate_and_normalize(df)
    assert len(norm_df) == 7
    assert "Amount" in norm_df.columns
    assert "Category" in norm_df.columns
    assert "Type" in norm_df.columns
    # Check category casing normalization
    assert "Shopping" in norm_df["Category"].values
    assert "Bike Maintance" in norm_df["Category"].values


def test_valid_xlsx_processing(demo_csv_bytes):
    df_raw = pd.read_csv(io.BytesIO(demo_csv_bytes))
    xlsx_buffer = io.BytesIO()
    df_raw.to_excel(xlsx_buffer, index=False)
    xlsx_bytes = xlsx_buffer.getvalue()

    df = FileProcessor.read_file(xlsx_bytes, "test.xlsx")
    norm_df, warnings = FileProcessor.validate_and_normalize(df)
    assert len(norm_df) == 7


def test_missing_required_column():
    csv_missing = "Timestamp,Date,Category,Amount\n10/27/2026,10/27/2026,Food,50"
    df = FileProcessor.read_file(csv_missing.encode("utf-8"), "missing.csv")
    with pytest.raises(FileProcessingError) as exc_info:
        FileProcessor.validate_and_normalize(df)
    assert "Missing required column" in str(exc_info.value.errors)


def test_invalid_amount():
    csv_bad_amt = """Timestamp,Date,Category,Description,Amount,Type
10/27/2026 9:00:00,10/27/2026,Food,Snack,-50,Expense
"""
    df = FileProcessor.read_file(csv_bad_amt.encode("utf-8"), "bad_amt.csv")
    with pytest.raises(FileProcessingError) as exc_info:
        FileProcessor.validate_and_normalize(df)
    assert any("invalid, zero, or negative" in err for err in exc_info.value.errors)


def test_invalid_type():
    csv_bad_type = """Timestamp,Date,Category,Description,Amount,Type
10/27/2026 9:00:00,10/27/2026,Food,Snack,50,Investment
"""
    df = FileProcessor.read_file(csv_bad_type.encode("utf-8"), "bad_type.csv")
    with pytest.raises(FileProcessingError) as exc_info:
        FileProcessor.validate_and_normalize(df)
    assert any("Invalid transaction type" in err for err in exc_info.value.errors)


def test_empty_file():
    with pytest.raises(FileProcessingError) as exc_info:
        FileProcessor.read_file(b"", "empty.csv")
    assert "empty" in str(exc_info.value)

