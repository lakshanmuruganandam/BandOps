#!/bin/bash
echo "Starting BandOps Protocol..."

# Start backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8002 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev -- --port 5175 &
FRONTEND_PID=$!

echo "BandOps is running! Access the UI at http://localhost:5175"
echo "Press Ctrl+C to terminate."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
