# 🎨 AI Vision Agent Pro

**Professional-grade Agentic Image Generation Platform**

Powered by LangGraph, SiliconFlow, and Langfuse.

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- SiliconFlow API Key

### Installation

1. **Clone the repository** (if not already done)
```bash
git clone <repo_url>
cd ai-vision-agent-pro
```

2. **Configure environment**
Create `backend/.env` based on `backend/.env` (it should be already there) and add your keys:
```env
SILICONFLOW_API_KEY=your_key_here
LANGFUSE_ENABLED=true # Optional
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

3. **Launch with Docker**
```bash
docker-compose up --build
```
This will start:
- Frontend at http://localhost:5173
- Backend at http://localhost:8000

---

### 🧷 Azure Deployment & Common Pitfalls

When you push the project to Azure (App Service, Container Instance, etc.), remember:

1. **Set environment variables** in the App Settings (don’t rely on a `.env` file):
   ```
   SILICONFLOW_API_KEY=...
   LANGFUSE_ENABLED=true
   LANGFUSE_PUBLIC_KEY=...
   LANGFUSE_SECRET_KEY=...
   PORT=8000  # Azure provides this automatically for Web Apps
   ```
2. **Protocol alignment** – the frontend now uses `window.location.protocol` so that
   HTTPS sites will call the backend over HTTPS. If you hardcode `http://` you’ll
   see mixed‑content errors and image generation requests will be blocked.
3. **Outbound network** – ensure the service is allowed to reach `api.siliconflow.cn`.
   App Service might require explicit networking rules or use of a vNet.
4. **Logs** – check the container logs for startup messages like `🔑 API Key Loaded` and
   HTTP errors from the image service. Most generation failures are simply missing or
   invalid API keys.

After deployment, open the browser dev tools and look for network errors if images
aren’t appearing. When deploying via Docker Compose, the `backend` container respects
the `$PORT` variable and can be used on any host.


---

## 🏗️ Architecture

- **Backend**: FastAPI app serving LangGraph agent.
- **Agent**: 3-node graph (Planner -> Generator -> Critic).
- **Frontend**: React + Vite + Tailwind CSS.

## 🛠️ Development

If you want to run locally without Docker:

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```