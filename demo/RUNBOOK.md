# BandOps Runbook

## Setup
1. `cd backend`
2. Configure `.env` with your 6 Agent UUIDs and API Keys.
3. `uv pip install -r requirements.txt` (or pip)
4. `fastapi dev main.py`

5. `cd frontend`
6. `npm install`
7. `npm run dev`

## Execution
1. Open http://localhost:5173
2. Click "Inject Chaos" to start the simulation.
3. Observe agents collaborating in the War Room.
4. Finalize the resolution via the Commander.
