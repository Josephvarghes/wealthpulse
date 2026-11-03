# FinPulse — Project Context & Session Memory
> **Last Updated:** 2026-11-03  
> **Location:** Local Workspace (`Persoonal Finance Sass/SESSION_MEMORY.md`)  
> **Status:** MVP Complete & Tested Locally  

---

## ⚠️ STRICT SECURITY & PRIVACY DIRECTIVE
> **NEVER READ, OPEN, DISPLAY, OR PRINT ANY `.env` FILE (`backend/.env` or any other `.env`).**
> - `.env` contains confidential user credentials and sensitive API keys.
> - Always respect user privacy: inspect only `.env.example` or schemas for configuration structure.
> - Ensure all `.env` files remain strictly in `.gitignore` and are never committed or logged.

---

## 1. Project Overview & Core Mission

- **Project Name:** FinPulse (Personal Finance Intelligence & Recommendation System)
- **Primary Source of Truth:** [`sdp.md`](./sdp.md)
- **Primary Workflow:** Google Form → Google Sheet → Export CSV/XLSX → Web Upload → Python Financial Processing → Deterministic Behavior & Rule Engine → AI Context Generation (Groq/Grok/Safeguard) → Comprehensive Interactive Dashboard.
- **Core Design Rule:**
  > **Code calculates. AI explains.**  
  > 100% of financial calculations, statistics, trends, outlier detection, and rule-based thresholds are computed strictly via deterministic Python/Pandas. AI **never** calculates or invents financial numbers, and raw transaction datasets are **never** sent to AI. Only a compact JSON summary is passed to the AI for behavioral summarization and actionable advice.

---

## 2. Architecture & File Structure

```text
Persoonal Finance Sass/
├── sdp.md                               # Software Development Plan (Specification)
├── README.md                            # High-level documentation & run guide
├── SESSION_MEMORY.md                    # This persistent project memory file
│
├── backend/
│   ├── run_server.py                    # Server launcher script (Uvicorn + FastAPI)
│   ├── demo_data.csv                    # Official SDP Section 25 demo dataset
│   ├── requirements.txt                 # Python dependencies
│   ├── Dockerfile                       # Container deployment setup
│   ├── .env                             # Environment variables & API keys
│   ├── .env.example                     # Environment template
│   │
│   ├── app/
│   │   ├── main.py                      # FastAPI app entry point & CORS
│   │   ├── config.py                    # Pydantic Settings config
│   │   │
│   │   ├── api/
│   │   │   └── upload.py                # Endpoints: /api/upload, /api/upload/demo, /api/health
│   │   │
│   │   ├── services/
│   │   │   ├── file_processor.py        # CSV/XLSX reading, casing normalization & validation
│   │   │   ├── finance_analyzer.py      # Numerical calculations, categories, trends, outliers
│   │   │   ├── behavior_analyzer.py     # Deterministic behavior detection (habits, spikes)
│   │   │   ├── recommendation_engine.py # Rule-based recommendation engine (priority-based)
│   │   │   └── ai_service.py            # AI abstraction (Groq, Grok, & built-in offline Mock)
│   │   │
│   │   └── schemas/
│   │       ├── transaction.py           # Raw & Normalized transaction models
│   │       └── analysis.py              # Full response payload schema
│   │
│   └── tests/
│       ├── conftest.py                  # Pytest fixtures
│       ├── test_file_processor.py       # Validation & normalization test suite
│       ├── test_finance_analyzer.py     # Financial math verification
│       └── test_behavior_and_recommendations.py # Rules & behaviors tests
│
└── frontend/
    ├── package.json                     # Frontend dependencies (React 18, Vite, Lucide, Recharts)
    ├── vite.config.ts                   # Vite configuration with /api proxy to backend:8000
    ├── tailwind.config.js               # Tailwind styling config
    ├── tsconfig.json                    # TypeScript compiler config
    │
    └── src/
        ├── main.tsx                     # React DOM entry
        ├── App.tsx                      # Main dashboard layout & state management
        ├── index.css                    # Tailwind directives & styles
        │
        ├── components/
        │   ├── Header.tsx               # Brand, metadata & currency switcher (₹, $, €)
        │   ├── UploadSection.tsx        # Drag & drop upload + 1-click SDP demo loader
        │   ├── SummaryCards.tsx         # Total Income, Expenses, Savings, Savings Rate Gauge
        │   ├── BehaviorFindings.tsx     # Deterministic habit & pattern cards
        │   ├── RuleRecommendations.tsx  # Priority-based rule recommendations
        │   ├── UnusualExpensesList.tsx  # Statistical outlier expenses
        │   └── AIRecommendationsCard.tsx # 5-point AI advisory breakdown
        │
        ├── charts/
        │   ├── CategoryChart.tsx        # Recharts Donut + Ranked category list
        │   └── TrendsChart.tsx          # Recharts Cash-flow Area Chart (Daily/Weekly/Monthly)
        │
        ├── services/
        │   └── api.ts                   # Fetch API client
        │
        ├── types/
        │   └── index.ts                 # TypeScript interfaces
        │
        └── utils/
            └── formatters.ts            # Currency & percentage formatting utilities
```

---

## 3. Configuration & AI Provider Details

### `backend/.env` Settings
```env
AI_PROVIDER=groq
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
XAI_API_KEY=
XAI_MODEL=grok-beta
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

- **Groq Integration:** Enabled by default. Once a key (`gsk_...`) is added to `GROQ_API_KEY`, it calls `llama-3.3-70b-versatile`.
- **Fail-Safe Offline Safeguard (`MockAIProvider`):** If no API key is supplied or the network is offline, the backend automatically uses a local rule-based explainer that returns the exact 5 items required by SDP Section 19 without failing or throwing errors.
- **xAI Grok Integration:** Also implemented in `backend/app/services/ai_service.py` (`grok-beta`) if user sets `AI_PROVIDER=grok` and provides `XAI_API_KEY`.

---

## 4. Key Decisions & Preferences Aligned With User

1. **AI Provider:** Configured for Groq AI (`llama-3.3-70b-versatile`) with seamless local fallback.
2. **Currency Display:** Defaults to Indian Rupee (**₹** INR) with an interactive top-bar toggle for **$** (USD) and **€** (EUR).
3. **One-Click Demo Button:** Provided on the upload card ("Load SDP Demo Dataset") to load and test the official SDP Section 25 dataset instantly.
4. **Local Execution Environment:**
   - Python: Installed globally at `C:\Python312\python.exe` (v3.12). All dependencies (`fastapi`, `uvicorn`, `pandas`, `openpyxl`, `pydantic`, `httpx`, `pytest`) are installed.
   - Node: Installed globally (`node` v24.2.0, `npm` v10.4.0). All frontend packages (`react`, `recharts`, `lucide-react`, `tailwindcss`) are installed in `frontend/node_modules`.
5. **Confidentiality / Security Rule:** Never read or inspect `.env` files — all sensitive API keys must remain strictly confidential and protected from version control.

---

## 5. Verification on Official SDP Demo Dataset

Tested against Section 25 fixture:
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
- **Results:**
  - Total Income: ₹0.0
  - Total Expenses: ₹1,600.0 across 4 categories:
    - Bike Maintance: ₹1,080.0 (67.5%)
    - Shopping: ₹309.0 (19.31%)
    - Food: ₹111.0 (6.94%)
    - Bike Fuel: ₹100.0 (6.25%)
  - Outlier: ₹1,000 for `Splendour insurance` flagged.
  - Behavior: Concentration in Bike Maintance detected, micro-expenses detected (5 txs < ₹100).
  - Rule recommendations generated: cap discretionary bike spend, budget for lump sums, record income.
  - Health check (`GET /api/health`) returns HTTP 200 `{"status": "healthy"}`.
  - Frontend HTTP status returns 200 OK.

---

## 6. How to Run Locally

Whenever resuming work, open two terminals in the workspace root:

### Terminal 1: Backend
```powershell
python backend/run_server.py
```
*API runs at:* `http://127.0.0.1:8000`  
*Swagger Docs:* `http://127.0.0.1:8000/docs`

### Terminal 2: Frontend
```powershell
cd frontend
npm run dev
```
*Web App runs at:* `http://localhost:5173`

---

## 7. Future Scope & Boundary Rules (From SDP Section 28)
*Do NOT implement unless explicitly asked:*
- Direct Google Sheets OAuth API synchronization
- Multi-user authentication & user databases
- WhatsApp / Voice bot integrations
- Complex microservices or Redis caching
- The current MVP architecture satisfies all requirements cleanly and efficiently without unnecessary bloat.

