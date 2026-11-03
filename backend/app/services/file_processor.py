import io
import pandas as pd
from typing import Tuple, List, Optional
from datetime import datetime


REQUIRED_COLUMNS = ["Timestamp", "Date", "Category", "Description", "Amount", "Type"]


class FileProcessingError(Exception):
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.errors = errors or []


class FileProcessor:
    @staticmethod
    def read_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
        """
        Reads CSV or XLSX from bytes into a Pandas DataFrame.
        """
        if not file_bytes:
            raise FileProcessingError("Uploaded file is empty.")

        ext = filename.lower().split(".")[-1]
        try:
            if ext == "csv":
                df = pd.read_csv(io.BytesIO(file_bytes))
            elif ext in ["xlsx", "xls"]:
                df = pd.read_excel(io.BytesIO(file_bytes))
            else:
                raise FileProcessingError(f"Unsupported file format: .{ext}. Please upload a CSV or XLSX file.")
        except Exception as e:
            if isinstance(e, FileProcessingError):
                raise
            raise FileProcessingError(f"Failed to parse file '{filename}': {str(e)}")

        if df.empty:
            raise FileProcessingError("Uploaded file contains no transaction data.")

        return df

    @classmethod
    def validate_and_normalize(cls, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Validates columns, amounts, types, and normalizes casing, dates, and empty cells.
        Returns (normalized_df, warnings).
        Raises FileProcessingError on critical validation errors.
        """
        errors = []
        warnings = []

        # 1. Match columns case-insensitively
        col_mapping = {}
        df_cols_lower = {str(col).strip().lower(): col for col in df.columns}

        for req in REQUIRED_COLUMNS:
            req_lower = req.lower()
            if req_lower in df_cols_lower:
                col_mapping[df_cols_lower[req_lower]] = req
            else:
                errors.append(f"Missing required column: '{req}'")

        if errors:
            raise FileProcessingError("File validation failed due to missing columns.", errors=errors)

        # Rename columns to standard casing
        df = df.rename(columns=col_mapping)
        df = df[REQUIRED_COLUMNS].copy()

        # Drop rows where all required columns are null
        df = df.dropna(how="all")
        if df.empty:
            raise FileProcessingError("Uploaded file contains only empty rows.")

        # 2. Normalize and validate 'Amount'
        try:
            # Remove any currency symbols, commas or whitespace
            df["Amount"] = df["Amount"].astype(str).str.replace(r"[^\d.-]", "", regex=True)
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        except Exception as e:
            errors.append(f"Failed to process Amount column: {str(e)}")

        invalid_amount_rows = df["Amount"].isna() | (df["Amount"] <= 0)
        if invalid_amount_rows.any():
            invalid_count = int(invalid_amount_rows.sum())
            errors.append(f"Found {invalid_count} row(s) with invalid, zero, or negative amounts.")

        # 3. Normalize and validate 'Type'
        df["Type"] = df["Type"].astype(str).str.strip().str.capitalize()
        invalid_type_rows = ~df["Type"].isin(["Income", "Expense"])
        if invalid_type_rows.any():
            invalid_types = df.loc[invalid_type_rows, "Type"].unique().tolist()
            errors.append(f"Invalid transaction type(s) found: {invalid_types}. Only 'Income' or 'Expense' are allowed.")

        # 4. Normalize and validate 'Date'
        # Convert date to standard YYYY-MM-DD
        try:
            parsed_dates = pd.to_datetime(df["Date"], errors="coerce", dayfirst=False)
            invalid_dates = parsed_dates.isna()
            if invalid_dates.any():
                # Attempt alternative dayfirst=True for ambiguous formats
                fallback = pd.to_datetime(df.loc[invalid_dates, "Date"], errors="coerce", dayfirst=True)
                parsed_dates.loc[invalid_dates] = fallback
                still_invalid = parsed_dates.isna().sum()
                if still_invalid > 0:
                    errors.append(f"Found {int(still_invalid)} row(s) with invalid date format.")
            df["DateObj"] = parsed_dates
            df["Date"] = parsed_dates.dt.strftime("%Y-%m-%d")
        except Exception as e:
            errors.append(f"Date parsing failed: {str(e)}")

        # 5. Normalize and validate 'Timestamp'
        try:
            parsed_ts = pd.to_datetime(df["Timestamp"], errors="coerce")
            df["Timestamp"] = parsed_ts.dt.strftime("%Y-%m-%d %H:%M:%S")
            # If timestamp parsing fails for some rows, fallback to Date
            missing_ts = df["Timestamp"].isna()
            if missing_ts.any():
                df.loc[missing_ts, "Timestamp"] = df.loc[missing_ts, "Date"] + " 00:00:00"
        except Exception:
            df["Timestamp"] = df["Date"] + " 00:00:00"

        # 6. Normalize 'Category' (trim and Title Case)
        df["Category"] = df["Category"].fillna("Uncategorized").astype(str).str.strip()
        # Title case, handling special words
        df["Category"] = df["Category"].apply(lambda c: c.title() if c else "Uncategorized")
        # Ensure category is not empty
        empty_cat = df["Category"] == ""
        if empty_cat.any():
            df.loc[empty_cat, "Category"] = "Uncategorized"

        # 7. Normalize 'Description'
        df["Description"] = df["Description"].fillna("").astype(str).str.strip()

        # If any validation errors occurred, raise error
        if errors:
            raise FileProcessingError("File validation failed.", errors=errors)

        # Sort chronologically
        df = df.sort_values(by=["DateObj", "Timestamp"]).reset_index(drop=True)
        df["id"] = range(1, len(df) + 1)

        return df, warnings

