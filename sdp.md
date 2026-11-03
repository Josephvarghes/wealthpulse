# Software Development Plan (SDP)
## Personal Finance Intelligence & Recommendation System

## 1. Project Overview

Build a personal finance web application that accepts exported Google Sheets data in CSV/Excel format, processes the financial transactions, analyzes spending behavior, and provides financial insights and recommendations.

Current workflow:

Google Form → Google Sheet → Export → Manual analysis

Target workflow:

Google Form → Google Sheet → Export CSV/Excel → Upload → Automatic Analysis → Dashboard → Recommendations

The application is primarily for personal use.

## 2. Core Principle

Use code for all calculations, data processing, statistics, trends, and rule-based analysis.

Use AI only for:
- Explaining calculated results
- Summarizing financial behavior
- Prioritizing recommendations
- Giving practical recommendations based on calculated data
- Answering questions using the calculated financial context

Do NOT send the complete raw Excel/CSV data to the AI.

Only send a small structured summary after Python calculations to reduce token usage and improve reliability.

AI must never be responsible for calculating financial numbers.

---

# 3. Input Data

The application must support CSV and Excel files exported from Google Sheets.

Current data structure:

| Timestamp | Date | Category | Description | Amount | Type |
|---|---|---|---|---:|---|
| 10/27/2026 9:27:16 | 10/27/2026 | Bike Maintance | Splendour-puc | 80 | Expense |
| 10/27/2026 13:02:41 | 10/27/2026 | shopping | Books | 309 | Expense |
| 10/27/2026 22:54:51 | 10/27/2026 | Food | Fruits | 54 | Expense |
| 10/27/2026 22:55:23 | 10/27/2026 | Bike Fuel | | 100 | Expense |
| 10/28/2026 9:28:32 | 10/28/2026 | Food | Tea | 27 | Expense |
| 10/28/2026 9:34:23 | 10/28/2026 | Food | Banana | 30 | Expense |
| 10/28/2026 14:17:33 | 10/28/2026 | Bike Maintance | Splendour insurance | 1000 | Expense |

### Required columns

- Timestamp
- Date
- Category
- Description
- Amount
- Type

### Type

Initially support:

- Income
- Expense

Do not invent additional transaction types unless required later.

### Data handling

Normalize:

- Dates
- Timestamp
- Category casing
- Amount values
- Empty descriptions
- Empty cells

Example:

`shopping`, `Shopping`, `SHOPPING`

should be normalized to the same category for analysis.

Do not modify the original uploaded data.

---

# 4. MVP User Flow

## Step 1 — Upload

User uploads:

- CSV
- XLSX

## Step 2 — Validate

Check:

- File format
- Required columns
- Empty required values
- Invalid dates
- Invalid amounts
- Invalid transaction types

If invalid, show a clear error and do not continue analysis.

## Step 3 — Process

Backend reads the file using Python/Pandas.

Normalize and validate the data.

## Step 4 — Analyze

Run the finance analysis engine.

## Step 5 — Generate Dashboard

Display calculated financial metrics and charts.

## Step 6 — Generate Recommendations

First use deterministic rule-based recommendations.

Then send only the calculated summary to the AI for explanation and additional recommendations.

---

# 5. Architecture

```text
User
 |
 v
React Frontend
 |
 | CSV/XLSX upload
 v
FastAPI Backend
 |
 +--> File Validation
 |
 +--> Pandas Data Processing
 |
 +--> Finance Calculation Engine
 |
 +--> Behavior Analysis Engine
 |
 +--> Rule-Based Recommendation Engine
 |
 +--> Small AI Context Generator
 |          |
 |          v
 |        Grok
 |
 +--> API Response
 |
 v
Dashboard
```

Keep the architecture simple.

Do not introduce microservices, queues, Redis, Kubernetes, RAG, vector databases, or other unnecessary infrastructure for the MVP.

---

# 6. Recommended Tech Stack

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- Recharts

## Backend

- Python
- FastAPI
- Pandas
- OpenPyXL
- Pydantic

## Database

Database is optional for the first MVP.

If persistence is required:

- PostgreSQL
- Supabase PostgreSQL

Do not store anything in the database until the core upload → analysis → dashboard flow works.

## AI

Use Grok through a separate AI service abstraction.

Do not tightly couple the application to Grok.

Example:

```text
AIService
    |
    +-- GrokProvider
    |
    +-- FutureProvider
```

The AI provider must be replaceable.

## Deployment

Preferred initial setup:

Frontend:
- Cloudflare Pages

Backend:
- Koyeb or another suitable free-tier service

Database:
- Supabase free tier if required

Keep deployment configuration simple.

---

# 7. Backend Project Structure

Use a clean structure similar to:

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── upload.py
│   │   ├── analysis.py
│   │   └── recommendations.py
│   │
│   ├── services/
│   │   ├── file_processor.py
│   │   ├── finance_analyzer.py
│   │   ├── behavior_analyzer.py
│   │   ├── recommendation_engine.py
│   │   └── ai_service.py
│   │
│   ├── models/
│   ├── schemas/
│   └── utils/
│
├── tests/
├── requirements.txt
└── Dockerfile
```

---

# 8. Frontend Structure

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── charts/
│   ├── services/
│   ├── types/
│   ├── hooks/
│   └── utils/
│
├── App.tsx
└── main.tsx
```

---

# 9. Finance Analysis Engine

All numerical analysis must happen in Python.

## Basic metrics

Calculate:

- Total income
- Total expenses
- Net balance
- Savings
- Savings rate
- Transaction count
- Average transaction
- Highest transaction
- Lowest transaction

For:

```text
Savings = Income - Expenses

Savings Rate = (Savings / Income) * 100
```

Handle zero-income cases safely.

---

# 10. Category Analysis

Group expenses by category.

For each category calculate:

```text
category
total_amount
transaction_count
percentage_of_total_expenses
average_transaction
```

Example:

```json
{
  "category": "Food",
  "total_amount": 111,
  "transaction_count": 3,
  "percentage": 12.4
}
```

Category matching should be case-insensitive.

---

# 11. Description Analysis

Use Description for additional insights.

Examples:

```text
Food → Tea
Food → Banana
Food → Fruits

Bike Maintenance → Splendour-puc
Bike Maintenance → Splendour insurance
```

Do not depend on Description being present.

Empty descriptions must be valid.

---

# 12. Time Analysis

Support:

- Daily
- Weekly
- Monthly

Calculate:

- Daily spending
- Weekly spending
- Monthly spending
- Monthly income
- Monthly expenses
- Monthly savings
- Category spending by month

The application should automatically determine the date range from uploaded data.

Do not hardcode October 2026.

---

# 13. Spending Trend Detection

Detect:

- Increasing expenses
- Decreasing expenses
- Stable expenses
- Category growth
- Category reduction

For example:

```text
Food:
Previous period = ₹4,000
Current period = ₹5,000

Increase = 25%
```

Use code to calculate this.

---

# 14. Unusual Expense Detection

Identify potentially unusual transactions using a simple statistical/rule-based approach.

For example:

- Transaction significantly higher than the user's normal transaction amount
- Category transaction significantly above its normal amount

Do not call AI for detection.

Return structured data such as:

```json
{
  "description": "Splendour insurance",
  "amount": 1000,
  "category": "Bike Maintance",
  "reason": "Higher than normal Bike Maintance transaction"
}
```

The algorithm can be improved later.

---

# 15. Recurring Expense Detection

Attempt to detect recurring transactions based on:

- Similar description
- Similar category
- Similar amount
- Repeated time intervals

Do not assume every repeated transaction is recurring.

Mark results as:

```text
possible_recurring
```

rather than guaranteed recurring.

---

# 16. Financial Behavior Analysis

Create a structured behavior report.

Examples:

```text
High food spending
Increasing shopping spending
High weekend spending
Improving savings
Repeated bike-related expenses
Unusual transaction
Frequent small transactions
```

These are analytical findings, not AI-generated statements.

---

# 17. Rule-Based Recommendation Engine

Create recommendations using code before calling AI.

Examples:

### High spending

```text
IF category_percentage > configured_threshold
THEN generate high-category-spending finding
```

### Increasing spending

```text
IF category_growth > configured_threshold
THEN generate spending-growth finding
```

### Low savings

```text
IF savings_rate < configured_threshold
THEN generate savings recommendation
```

### Unusual transaction

```text
IF unusual_transaction_detected
THEN generate review recommendation
```

Thresholds should be configurable.

Do not hardcode financial advice as absolute truth.

---

# 18. AI Context

After all calculations, create a small structured object.

Example:

```json
{
  "period": "2026-10",
  "income": 45000,
  "expenses": 28400,
  "savings": 16600,
  "savings_rate": 36.89,
  "top_categories": [
    {
      "name": "Food",
      "amount": 6200,
      "percentage": 21.83,
      "change_percent": 24
    },
    {
      "name": "Shopping",
      "amount": 5100,
      "percentage": 17.96,
      "change_percent": 31
    }
  ],
  "behavior_findings": [
    "Food spending increased",
    "Shopping spending increased"
  ],
  "unusual_expenses": [
    {
      "category": "Bike Maintance",
      "amount": 1000
    }
  ],
  "rule_recommendations": [
    "Review increasing food expenses",
    "Review shopping expenses"
  ]
}
```

Only send this compact context to AI.

Never send the complete transaction dataset unless explicitly required for a future feature.

---

# 19. AI Prompt Requirements

The AI should receive a system instruction similar to:

```text
You are a personal finance analysis assistant.

Analyze only the structured financial data provided.

The numbers have already been calculated by the application.
Do not recalculate or invent financial values.

Explain the user's financial behavior clearly.

Provide:
1. Most important observation
2. Positive financial behavior
3. Main concern
4. Practical recommendation
5. Short-term action

Keep recommendations realistic and based only on the provided data.

Do not provide guaranteed financial outcomes.

Do not invent transactions, income, expenses, or trends.
```

AI output should be concise.

Avoid unnecessary long responses to reduce token usage.

---

# 20. Dashboard

Main dashboard should show:

## Summary Cards

```text
Total Income
Total Expenses
Savings
Savings Rate
```

## Charts

- Income vs expenses
- Monthly savings
- Spending by category
- Category trends
- Daily/weekly spending

## Insights

Show:

```text
Positive Trends
Warnings
Behavior Patterns
Unusual Expenses
```

## AI Recommendations

Display:

```text
AI Financial Summary

Key Observation

Main Concern

Recommendation

Next Action
```

---

# 21. Upload UI

Keep the upload flow very simple.

There should NOT be a separate unnecessary upload page.

Preferred flow:

```text
Dashboard
   |
   v
Upload Data
   |
   +--> Select CSV/XLSX
   |
   +--> Upload
   |
   +--> Automatically process
   |
   +--> Automatically generate report
```

The user should not need to navigate through multiple pages.

---

# 22. Error Handling

Handle:

- Unsupported file
- Missing columns
- Empty file
- Invalid amount
- Invalid date
- Invalid type
- Duplicate rows
- Large file
- AI unavailable
- Backend failure

If AI fails, the dashboard must still work.

Example:

```text
Financial analysis completed.

AI recommendations are temporarily unavailable.
```

The application must never depend entirely on AI.

---

# 23. Privacy

Financial data is sensitive.

Requirements:

- Never expose API keys in frontend
- Store secrets only in environment variables
- Do not log raw financial transactions
- Limit uploaded file size
- Validate uploaded files
- Use HTTPS in production
- Do not send unnecessary financial information to AI
- Do not expose another user's data
- Delete temporary uploaded files after processing when persistence is not required

---

# 24. Testing

Create tests for:

### File processing

- Valid CSV
- Valid XLSX
- Missing columns
- Invalid amount
- Invalid date
- Empty file

### Finance calculations

- Income
- Expense
- Savings
- Savings rate
- Category totals
- Monthly totals

### Analysis

- Spending increase
- Spending decrease
- Unusual transaction
- Recurring transaction

### Recommendations

- High spending
- Low savings
- Increasing category
- Unusual expense

Use the provided demo data as an initial test fixture.

---

# 25. Demo Dataset

Use this dataset for development/testing:

```csv
Timestamp,Date,Category,Description,Amount,Type
10/27/2026 9:27:16,10/27/2026,Bike Maintance,Splendour-puc,80,Expense
10/27/2026 13:02:41,10/27/2026,shopping,Books,309,Expense
10/27/2026 22:54:51,10/27/2026,Food,Fruits,54,Expense
10/27/2026 22:55:23,10/27/2026,Bike Fuel,,100,Expense
10/28/2026 9:28:32,10/28/2026,Food,Tea,27,Expense
10/28/2026 9:34:23,10/28/2026,Food,Banana,30,Expense
10/28/2026 14:17:33,10/28/2026,Bike Maintance,Splendour insurance,1000,Expense
```

Do not add fake income transactions to this dataset.

---

# 26. Development Order

Implement strictly in this order:

```text
1. Project setup
2. Backend setup
3. Frontend setup
4. File upload
5. File validation
6. Data normalization
7. Finance calculation engine
8. Category analysis
9. Time analysis
10. Behavior analysis
11. Rule-based recommendations
12. Dashboard
13. AI service abstraction
14. Grok integration
15. AI recommendations
16. Testing
17. Production configuration
18. Deployment
```

Do not start AI integration before the calculation and recommendation engines work correctly.

---

# 27. MVP Completion Criteria

The MVP is complete when:

- User can upload the provided CSV/XLSX structure.
- File is validated automatically.
- Data is processed with Pandas.
- Financial metrics are calculated correctly.
- Categories are analyzed.
- Trends are detected.
- Basic behavior patterns are detected.
- Rule-based recommendations are generated.
- Dashboard displays the analysis.
- AI receives only compact calculated context.
- AI generates concise recommendations.
- Application continues working if AI is unavailable.
- No API keys are exposed.
- Tests cover the main calculation logic.
- Application can be deployed using free-tier infrastructure.

---

# 28. Future Features — DO NOT IMPLEMENT IN MVP

Consider later:

- Direct Google Sheets synchronization
- Google authentication
- Multiple users
- Historical database
- Automatic daily sync
- Budget planning
- Savings goals
- Investment tracking
- Financial forecasting
- WhatsApp integration
- Voice-based finance assistant
- Mobile application
- Advanced anomaly detection
- Personalized financial scoring

These should not be implemented unless explicitly requested.

---

# 29. Development Rules for AI IDE

When developing this project:

1. Follow this SDP as the source of truth.
2. Do not add unnecessary features.
3. Do not change the input data structure without asking.
4. Do not introduce unnecessary dependencies.
5. Prefer simple Python calculations over AI.
6. Keep AI calls minimal.
7. Never send raw financial data to AI when aggregated data is sufficient.
8. Keep frontend and backend responsibilities separate.
9. Write reusable services instead of putting logic inside API routes.
10. Add tests for financial calculations.
11. Do not hardcode demo data into production logic.
12. Use environment variables for secrets.
13. Keep AI provider replaceable.
14. Do not expose API keys in frontend code.
15. Preserve existing functionality when making changes.
16. Before implementing a major architectural change, explain the reason and ask for approval.
17. Keep the UI simple and focused on financial insights.
18. Do not over-engineer the MVP.

## Final Development Goal

Build a simple, reliable personal finance intelligence system where:

```text
USER DATA
   ↓
PYTHON PROCESSING
   ↓
FINANCIAL CALCULATIONS
   ↓
BEHAVIOR ANALYSIS
   ↓
RULE-BASED RECOMMENDATIONS
   ↓
SMALL AI CONTEXT
   ↓
GROK
   ↓
CLEAR FINANCIAL INSIGHTS
```

The system should help the user answer:

> "Where is my money going?"

> "What financial behavior do I have?"

> "What is changing?"

> "What should I pay attention to?"

> "What should I do next?"