<div align="center">

# 💎 WealthPulse
### Personal Finance Intelligence & Deterministic Analytics Engine

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

<p align="center">
  <strong>Transform raw spreadsheet transactions into deterministic financial intelligence, behavioral profiling, and contextual AI advice.</strong>
</p>

[Key Features](#-key-features) •
[Core Principle](#-core-principle) •
[Architecture](#-system-architecture) •
[Tech Stack](#-tech-stack) •
[Getting Started](#-getting-started) •
[Deployment Guide](DEPLOYMENT.md) •
[API Specification](#-api-specification) •
[Security & Privacy](#-security--privacy-first)

---

</div>

## 📖 Overview

**WealthPulse** is an enterprise-grade personal finance intelligence application engineered strictly around privacy and mathematical integrity. It ingests transaction logs exported from Google Forms / Google Sheets in `.csv` or `.xlsx` format, performs deterministic mathematical and statistical analysis in Python, identifies behavioral spending patterns and statistical outliers, and synthesizes actionable recommendations via high-performance LLM explainers (**Groq LLaMA 3.3 70B** / **xAI Grok** / **Offline Mock Safeguard**).

---

## 🌟 Core Principle

<div align="center">
  <blockquote>
    <h3>« Code calculates. AI explains. »</h3>
  </blockquote>
</div>

Large Language Models (LLMs) are stochastic pattern engines prone to arithmetic hallucinations, calculation drift, and privacy risks when fed raw transactional ledgers. WealthPulse enforces an uncompromising architectural boundary:

| Layer | Responsibility | Technology |
| :--- | :--- | :--- |
| **Deterministic Engine** | 100% of arithmetic, sums, savings rates, categorical aggregations, multi-period trends, outlier detection, and priority-ranked rules. | Python 3.12, Pandas |
| **Privacy Perimeter** | Raw transaction rows, timestamps, merchant strings, and personal entries **never** leave your machine. Only compact, aggregated statistical summaries cross the network. | In-Memory Processing |
| **AI Advisory Layer** | Pure linguistic synthesis, contextual behavioral explanation, and disciplined action planning based strictly on verified numbers. | Groq (`llama-3.3-70b-versatile`), xAI Grok, or Local Safeguard |

---

## ✨ Key Features

- **📂 Resilient Ingestion Pipeline:**
  - Automated casing normalization (`shopping` → `Shopping`, `Food` → `Food`).
  - Dual support for `.csv` and `.xlsx` file streams.
  - Robust multi-format timestamp and date parsing with automatic invalid row dropping.
  - 1-click official demo dataset loader for instant verification.

- **🧮 Deterministic Financial Math:**
  - Accurate income, expense, net savings, and savings rate percentage computation.
  - Categorical distribution with ranking and percentage contributions.
  - Multi-period timeline analysis (configurable between Daily, Weekly, and Monthly aggregations).

- **🔍 Behavioral & Anomaly Detection:**
  - **Category Concentration:** Detects when any single expense category consumes >30% of total outlay.
  - **Micro-Transaction Tracking:** Flags high-frequency minor transactions (<₹100) that erode savings.
  - **Temporal Surges:** Detects weekend vs. weekday spending imbalances.
  - **Statistical Outlier Detection:** Identifies unusually large single-ticket expenses.

- **🎯 Priority-Ranked Rule Engine:**
  - Deterministic recommendation engine ranking action items into **High**, **Medium**, and **Low** priorities.
  - Triggers alerts for zero income records, negative savings rates, and unbudgeted lump-sums.

- **🤖 Zero-Hallucination AI Explainer:**
  - Sends a compact JSON schema (SDP Section 18) to high-speed inference engines (**Groq LLaMA 3.3 70B** or **xAI Grok**).
  - Returns a structured 5-part advisory breakdown: *Summary, Key Observation, Positive Discipline, Concern, and Next Action*.
  - **Built-in Offline Safeguard:** Seamless local fallback explainer when offline or without an API key—guaranteeing 0% downtime.

- **🎨 Modern Interactive Dashboard:**
  - Real-time interactive currency switcher (**₹ INR** default, **$ USD**, **€ EUR**).
  - Responsive visual charts powered by **Recharts** (donut breakdowns, timeline area charts, savings gauges).
  - Clean card layouts with priority badges and intuitive typography.

---

## 🏗️ System Architecture

```text
 User / Google Forms Export (.csv / .xlsx)
                  │
                  ▼
       ┌────────────────────────┐
       │ React + Vite Frontend  │  Port 5173 (Vite Proxy: /api -> 8000)
       │ - Currency Toggle      │  Tailwind CSS + Recharts + Lucide
       │ - Drag & Drop / Demo   │
       └───────────┬────────────┘
                   │ Multipart Form-Data / Direct POST
                   ▼
       ┌────────────────────────┐
       │    FastAPI Backend     │  Port 8000, Python 3.12+
       └───────────┬────────────┘
                   │
      ┌────────────┼─────────────────────────────┐
      ▼            ▼                             ▼
┌──────────────┐ ┌────────────────────────┐ ┌─────────────────────────┐
│FileProcessor │ │    FinanceAnalyzer     │ │    BehaviorAnalyzer     │
│- Casing Norm │ │- Income / Expense Totals│ │- >30% Dominant Category │
│- Date Parser │ │- Category Aggregations │ │- Micro-txs (<₹100)      │
│- Validation  │ │- Multi-period Trends   │ │- Statistical Outliers   │
└──────────────┘ └───────────┬────────────┘ └────────────┬────────────┘
                             │                           │
                             └─────────────┬─────────────┘
                                           ▼
                         ┌───────────────────────────────────┐
                         │   Deterministic Rule Engine       │
                         │   - Priority Ranking (High/Med/Low)│
                         └─────────────────┬─────────────────┘
                                           ▼
                         ┌───────────────────────────────────┐
                         │  Compact Context Generator        │
                         │  (SDP Sec 18 Aggregated Payload)  │
                         └─────────────────┬─────────────────┘
                                           ▼
                         ┌───────────────────────────────────┐
                         │         AI Service Layer          │
                         │ ┌───────────────┐ ┌─────────────┐ │
                         │ │ Groq LLaMA    │ │ Offline     │ │
                         │ │ 3.3-70B       │ │ Safeguard   │ │
                         │ └───────────────┘ └─────────────┘ │
                         └─────────────────┬─────────────────┘
                                           ▼
                         ┌───────────────────────────────────┐
                         │    Unified JSON Response Payload  │
                         │    ➔ Rendered on UI Dashboard     │
                         └───────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.12+` | Core execution runtime |
| **FastAPI** | `^0.115` | High-performance asynchronous REST API framework |
| **Uvicorn** | `^0.32` | ASGI server implementation |
| **Pandas** | `^2.2` | High-speed tabular processing, aggregations, and normalization |
| **OpenPyXL** | `^3.1` | Native Microsoft Excel (`.xlsx`) parsing engine |
| **Pydantic** | `^2.9` | Strict data validation and schema serialization |
| **HTTPX** | `^0.27` | Async client for external LLM inference |
| **Pytest** | `^8.3` | Test suite runner and automated verification |

### Frontend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| **React** | `^18.3` | Component-based UI library |
| **TypeScript** | `^5.5` | Type-safe enterprise JavaScript |
| **Vite** | `^5.4` | Next-generation frontend build tooling & dev server |
| **Tailwind CSS**| `^3.4` | Utility-first responsive styling framework |
| **Recharts** | `^2.13` | Composable SVG data visualization charts |
| **Lucide React**| `^0.454`| Consistent iconography |

---

## 🚀 Getting Started

### Prerequisites
- **Python**: `3.12+` ([Download Python](https://www.python.org/downloads/))
- **Node.js**: `18.0+` ([Download Node.js](https://nodejs.org/))
- **Git**: Installed and configured

### 1. Clone the Repository
```bash
git clone https://github.com/Josephvarghes/wealthpulse.git
cd wealthpulse
```

---

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# (Optional but recommended) Create and activate a virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

> [!NOTE]
> Open `backend/.env` and optionally provide your `GROQ_API_KEY`. If left empty, WealthPulse automatically operates in **Offline Safeguard Mode** with zero degradation to core analytics.

```bash
# Start backend server
python run_server.py
```
* Backend API live at: `http://127.0.0.1:8000`
* Interactive OpenAPI Swagger docs at: `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup
In a new terminal window:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
* Frontend Dashboard live at: `http://localhost:5173`

---

## 🧪 Testing & Verification

The backend includes a dedicated test suite verifying file validation, financial calculations, behavior identification, and recommendation priority ordering:

```bash
# Run pytest suite
python -m pytest backend/tests -v
```

### 1-Click Verification
Once the dashboard is running on `http://localhost:5173`, click the **"Load SDP Demo Dataset"** button on the upload card. It runs the official benchmark dataset and generates immediate analytics:

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

---

## 📡 API Specification

| Endpoint | Method | Description | Payload / Response |
| :--- | :--- | :--- | :--- |
| `/api/health` | `GET` | Health check and service readiness probe | Returns `{"status": "healthy"}` |
| `/api/upload` | `POST` | Ingests `.csv` or `.xlsx` multipart stream | Returns complete `AnalysisResult` JSON |
| `/api/upload/demo` | `POST` | Ingests the benchmark SDP demo dataset | Returns complete `AnalysisResult` JSON |

---

## ⚙️ Environment Variables

Defined in `backend/.env.example`:

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `AI_PROVIDER` | `string` | `groq` | AI provider selector (`groq`, `grok`, or `mock`) |
| `GROQ_API_KEY` | `string` | `""` | API key for Groq Cloud inference |
| `GROQ_MODEL` | `string` | `llama-3.3-70b-versatile` | LLaMA model checkpoint hosted on Groq |
| `XAI_API_KEY` | `string` | `""` | Optional xAI API key for Grok |
| `XAI_MODEL` | `string` | `grok-beta` | xAI Grok model checkpoint |
| `HOST` | `string` | `127.0.0.1` | Local backend listening address |
| `PORT` | `integer` | `8000` | Local backend listening port |
| `CORS_ORIGINS` | `string` | `http://localhost:5173,...` | Allowed CORS origins for web clients |

---

## 🔒 Security & Privacy First

- **Zero Data Exposure**: Raw transaction items, timestamps, and merchant notes are strictly processed in-memory and are never stored or sent to remote LLMs.
- **Fail-Safe Offline Mode**: If external AI APIs fail or network drops, the offline safeguard automatically synthesizes deterministic explanations with no crash or disruption.
- **Secret Isolation**: Configuration secrets are managed exclusively through environment variables. All `.env` files are strictly excluded from version control via `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository (`https://github.com/Josephvarghes/wealthpulse/fork`).
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes with descriptive commit messages (`git commit -m 'feat: add monthly date range selector'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure all unit tests pass before submitting your PR:
```bash
python -m pytest backend/tests -v
```

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).

<div align="center">
  <sub>Built with mathematical precision and privacy-first engineering.</sub>
</div>
