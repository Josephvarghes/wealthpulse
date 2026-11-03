import pytest
import io
import pandas as pd


DEMO_CSV = """Timestamp,Date,Category,Description,Amount,Type
10/27/2026 9:27:16,10/27/2026,Bike Maintance,Splendour-puc,80,Expense
10/27/2026 13:02:41,10/27/2026,shopping,Books,309,Expense
10/27/2026 22:54:51,10/27/2026,Food,Fruits,54,Expense
10/27/2026 22:55:23,10/27/2026,Bike Fuel,,100,Expense
10/28/2026 9:28:32,10/28/2026,Food,Tea,27,Expense
10/28/2026 9:34:23,10/28/2026,Food,Banana,30,Expense
10/28/2026 14:17:33,10/28/2026,Bike Maintance,Splendour insurance,1000,Expense
"""

DEMO_WITH_INCOME_CSV = """Timestamp,Date,Category,Description,Amount,Type
10/25/2026 10:00:00,10/25/2026,Salary,Monthly Salary,15000,Income
10/27/2026 9:27:16,10/27/2026,Bike Maintance,Splendour-puc,80,Expense
10/27/2026 13:02:41,10/27/2026,shopping,Books,309,Expense
10/27/2026 22:54:51,10/27/2026,Food,Fruits,54,Expense
10/27/2026 22:55:23,10/27/2026,Bike Fuel,,100,Expense
10/28/2026 9:28:32,10/28/2026,Food,Tea,27,Expense
10/28/2026 9:34:23,10/28/2026,Food,Banana,30,Expense
10/28/2026 14:17:33,10/28/2026,Bike Maintance,Splendour insurance,1000,Expense
"""


@pytest.fixture
def demo_csv_bytes():
    return DEMO_CSV.encode("utf-8")


@pytest.fixture
def demo_income_csv_bytes():
    return DEMO_WITH_INCOME_CSV.encode("utf-8")

