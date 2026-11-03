# 🌐 WealthPulse — Cloud Deployment Guide
> Step-by-step instructions to deploy the **FastAPI Backend on Render** and the **React + Vite Frontend on Vercel** using 100% free-tier infrastructure.

---

## 🏛️ Target Deployment Architecture

```text
       User's Browser (Desktop / Mobile)
                       │
                       ▼
         ┌───────────────────────────┐
         │     Frontend on Vercel    │   (Global Edge CDN)
         │  https://<app>.vercel.app │
         └─────────────┬─────────────┘
                       │ HTTPS API Requests (/api/...)
                       ▼
         ┌───────────────────────────┐
         │     Backend on Render     │   (FastAPI Python 3.12 Engine)
         │ https://<api>.onrender.com│
         └─────────────┬─────────────┘
                       │ Aggregated Context Only (SDP Sec 18)
                       ▼
         ┌───────────────────────────┐
         │      Groq Cloud LLM       │   (qwen/qwen3.8-27b)
         └───────────────────────────┘
```

---

## Part 1: Deploy Backend on Render (Free Tier)

Deploy the backend first so you have your live backend URL to configure in the frontend.

### Method A: Automatic Deployment via Blueprint (Recommended)
1. Go to **[dashboard.render.com](https://dashboard.render.com/)** and log in (or sign up with GitHub).
2. Click **New +** in the top bar and select **Blueprint**.
3. Connect your GitHub repository: `Josephvarghes/wealthpulse`.
4. Render will automatically detect the [`render.yaml`](./render.yaml) file in the root.
5. Enter your **`GROQ_API_KEY`** when prompted.
6. Click **Apply**. Render will build and deploy your backend service.

---

### Method B: Manual Web Service Setup
If you prefer manual configuration:
1. Go to **[dashboard.render.com](https://dashboard.render.com/)** → **New +** → **Web Service**.
2. Select **Build and deploy from a Git repository** and pick `Josephvarghes/wealthpulse`.
3. Configure the settings:
   - **Name:** `wealthpulse-backend`
   - **Region:** Choose the region closest to you (e.g., Singapore, Frankfurt, or Oregon).
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
4. Expand **Environment Variables** and add:
   | Key | Value | Notes |
   | :--- | :--- | :--- |
   | `PYTHON_VERSION` | `3.12.4` | Enforces modern Python runtime |
   | `AI_PROVIDER` | `groq` | Directs AI requests to Groq |
   | `GROQ_API_KEY` | `gsk_...` | Your secret Groq API key |
   | `GROQ_MODEL` | `qwen/qwen3.8-27b` | Model configured for your tier |
   | `CORS_ORIGINS` | `*` | Allows requests from your Vercel URL |
5. Click **Create Web Service**.

### Verify Backend Health
Once Render finishes building, it will display your service URL (e.g. `https://wealthpulse-backend.onrender.com`).
Visit:
👉 `https://<your-render-url>/api/health`

You should see:
```json
{
  "status": "healthy",
  "service": "Personal Finance Intelligence API",
  "configured_ai_provider": "groq",
  "has_groq_key": true
}
```

---

## Part 2: Deploy Frontend on Vercel (Free Tier)

Now that you have your live backend URL, deploy the React + Vite frontend to Vercel.

1. Go to **[vercel.com](https://vercel.com/)** and log in with your GitHub account.
2. Click **Add New…** → **Project**.
3. Import your repository: **`Josephvarghes/wealthpulse`**.
4. In the **Configure Project** screen:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click **Edit** and select **`frontend`** (important!).
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `dist` (default)
5. Expand **Environment Variables** and add:
   | Variable Name | Value |
   | :--- | :--- |
   | `VITE_API_BASE_URL` | `https://<your-render-url>/api` |

   > **Note:** Replace `<your-render-url>` with your actual Render URL from Part 1, followed by `/api` (e.g., `https://wealthpulse-backend.onrender.com/api`).

6. Click **Deploy**.
7. Vercel will install dependencies, build the TypeScript bundle, and publish your site in ~45 seconds.

---

## Part 3: Live Verification

1. Open your new Vercel deployment URL (e.g. `https://wealthpulse.vercel.app`).
2. Click **"Load SDP Demo Dataset"**.
3. Confirm that:
   - Numerical summaries (Income, Expense, Net Savings) populate immediately.
   - Recharts Donut & Timeline charts render smoothly.
   - The **Date Range Selector** displays the available months and allows toggling.
   - The **AI Financial Intelligence** card displays live observations from Groq (`qwen/qwen3.8-27b`).

---

## 💡 Free-Tier Tips & Notes

- **Render Cold Starts:** Free-tier services on Render spin down into a sleeping state after 15 minutes of inactivity. If you haven't opened the dashboard in a while, the very first request might take ~30–45 seconds while the backend wakes up. Subsequent requests will be near-instant.
- **Vercel CDN:** The frontend on Vercel is served through global edge servers and will always load instantly with 100% uptime.
- **Privacy:** Your raw transaction data is sent encrypted over HTTPS directly to your Render instance, processed in-memory, and immediately discarded. Only the compact Section 18 numerical summary is sent to Groq.

