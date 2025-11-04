# FinAI: AI-Powered Personal Finance Tracker

This is a production-ready, microservice-based personal finance tracker built with React, FastAPI, Docker, and Google Gemini.

## Features

* **Modern Frontend:** React, TailwindCSS, Recharts, Framer Motion.
* **Microservice Backend:** FastAPI, Docker, PostgreSQL.
* **AI-Powered:**
    * **Auto-categorization:** Local scikit-learn model predicts categories for new transactions.
    * **Smart Insights:** Google Gemini API provides natural language summaries, insights, and goal planning.
* **Full Auth:** JWT-based authentication (signup, login, refresh tokens).
* **Data Management:** CSV import/export, pagination, and search.
* **CI/CD:** GitHub Actions for testing, with seamless deployment to Vercel (Frontend) and Render (Backend).

---

## 1. Local Development Setup

### Prerequisites

* Docker & Docker Compose
* Node.js (v18+) & npm
* Python (v3.11+)
* Git

### Step-by-Step Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd finai-tracker
    ```

2.  **Set Up Environment Variables:**
    Copy all `.env.example` files in each `services/*` directory to a new `.env` file in the *same* directory.

    * `services/auth-service/.env`
    * `services/transactions-service/.env`
    * `services/ai-insights-service/.env`
    * `services/worker-service/.env`

    **Crucially, fill them out:**
    * `DATABASE_URL`: The `docker-compose.yml` file sets up a Postgres database. The correct URL for all services will be:
        `postgresql+psycopg2://user:password@postgres:5432/finaidb`
    * `JWT_SECRET`: Generate a strong secret key (e.g., `openssl rand -hex 32`) and use the *same key* for `auth-service`, `transactions-service`, and `ai-insights-service`.
    * `GEMINI_API_KEY`: Get this from Google AI Studio and add it to `services/ai-insights-service/.env`.
    * `INTERNAL_API_KEY`: Generate another strong secret (e.g., `openssl rand -hex 32`) and use it for all services that need internal communication (Worker, AI, Transactions).

3.  **Train the ML Model:**
    The Transactions service needs a `model.joblib` file.
    ```bash
    # Ensure you have the dependencies (or run in a venv)
    pip install pandas scikit-learn joblib
    
    # Run the training script
    python ./services/transactions-service/ml/train_model.py
    
    # This will create 'services/transactions-service/ml/model.joblib'
    ```

4.  **Run the Backend (Docker Compose):**
    This command will build all Docker images, start all services, and the Postgres database.
    ```bash
    docker compose up --build
    ```
    * The services will be available at:
        * Auth Service: `http://localhost:8001`
        * Transactions Service: `http://localhost:8002`
        * AI Insights Service: `http://localhost:8003`
        * Worker Service: (Runs in background)

5.  **Run Database Migrations:**
    With the containers running, run the Alembic migrations for the `auth` and `transactions` services.
    ```bash
    # In a new terminal:
    docker compose exec auth-service alembic upgrade head
    docker compose exec transactions-service alembic upgrade head
    ```

6.  **Run the Frontend:**
    ```bash
    # In a new terminal:
    cd client
    npm install
    npm run dev
    ```
    Your application is now running at `http://localhost:5173`.

---

## 2. Deployment

### A. Backend Deployment (Render)

1.  **Create PostgreSQL Database:**
    * Go to your Render Dashboard.
    * Create a new **PostgreSQL** instance (Free tier is fine).
    * After it's created, copy the **Internal Database URL**.

2.  **Create Web Services (Auth, Transactions, AI):**
    * Create a new **Web Service** for *each* of the 3 API services (Auth, Transactions, AI).
    * Connect your GitHub repository.
    * **Build Settings:**
        * **Runtime:** Docker
        * **Root Directory:** `./services/auth-service` (and repeat for `transactions-service`, `ai-insights-service`)
        * **Dockerfile Path:** `./Dockerfile` (relative to the root directory)
    * **Environment Variables:**
        * Go to the "Environment" tab for each service.
        * Add `DATABASE_URL` and paste the **Internal Database URL** from Step 1.
        * Add `JWT_SECRET` (must be the same strong secret for all).
        * Add `GEMINI_API_KEY` (for `ai-insights-service` only).
        * Add `INTERNAL_API_KEY` (for services that need it).
        * Add `PYTHON_VERSION` (e.g., `3.11.5`).
    * **Health Check:** Render will use the Docker health check, or you can set a path like `/health` (which we've added).

3.  **Run Migrations (One-time):**
    * After the services are live, go to the "Shell" tab for `auth-service` and `transactions-service`.
    * Run: `alembic upgrade head`

4.  **Create Worker Service:**
    * Create a new **Background Worker**.
    * Use the same repo and Docker settings, but point the **Root Directory** to `./services/worker-service`.
    * Add its required Environment Variables.

5.  **Update Frontend Config:**
    * Once your Render services are deployed, they will have public URLs (e.g., `https://finai-auth.onrender.com`).
    * Go to your `client/src/config.ts` file, and update the `production` URLs to match your Render URLs. Commit and push this change.

### B. Frontend Deployment (Vercel)

1.  **Import Project:**
    * Go to your Vercel Dashboard.
    * Import your GitHub repository.
2.  **Configure Project:**
    * **Framework Preset:** Vercel will auto-detect **Vite**.
    * **Root Directory:** `client`
    * **Build Command:** `npm run build`
    * **Output Directory:** `dist`
3.  **Add Environment Variables:**
    * `VITE_API_AUTH_URL`: `https://your-auth-service.onrender.com`
    * `VITE_API_TRANSACTIONS_URL`: `https://your-transactions-service.onrender.com`
    * `VITE_API_AI_URL`: `https://your-ai-service.onrender.com`
4.  **Deploy:**
    * Click "Deploy". Vercel will automatically build and deploy your React app.
    * It will also automatically re-deploy on every push to the `main` branch.