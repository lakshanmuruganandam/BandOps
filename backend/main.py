from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time

app = FastAPI(title="BandOps: Regulated Crisis Operations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

import hashlib

manager = ConnectionManager()

# Global ledger for traceability
current_hash = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()

def append_to_ledger(payload: dict):
    global current_hash
    # Create an immutable hash chain
    content_str = str(payload.get("content", "")) + str(payload.get("agent", ""))
    new_hash = hashlib.sha256((current_hash + content_str).encode('utf-8')).hexdigest()
    current_hash = new_hash
    payload["tx_hash"] = new_hash
    return payload

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def simulate_aog_swarm(inject_chaos: bool = False):
    global current_hash
    current_hash = hashlib.sha256(b"GENESIS_BLOCK").hexdigest() # Reset ledger
    
    await asyncio.sleep(1)
    await manager.broadcast(append_to_ledger({"event": "system", "content": "Band Room 'AOG-FLIGHT-902' active. Aircraft: B787. Status: Grounded (Hydraulic Fault)."}))
    await asyncio.sleep(2)
    
    # Mechanic Agent
    await manager.broadcast(append_to_ledger({
        "agent": "Line Mechanic Agent",
        "framework": "LangChain",
        "role": "Diagnostics",
        "content": "Fault isolated to the Left Engine Hydraulic Pump. Part # HP-787-B is required. Aircraft cannot fly under Minimum Equipment List (MEL) regulations."
    }))
    await asyncio.sleep(3)
    
    # Supply Chain
    await manager.broadcast(append_to_ledger({
        "agent": "Supply Chain Agent",
        "framework": "CrewAI",
        "role": "Logistics",
        "content": "Searching global inventory. Part # HP-787-B is NOT available at current airport (JFK). Nearest part is at ATL. Shipping time: 4 hours. Estimated repair start: 16:00Z."
    }))
    await asyncio.sleep(3)
    
    # Flight Ops
    await manager.broadcast(append_to_ledger({
        "agent": "Flight Ops Agent",
        "framework": "AutoGen",
        "role": "Dispatcher",
        "content": "A 4-hour delay violates our passenger compensation thresholds ($12,000 estimated cost). Proposal: Swap aircraft with spare B777 at Gate 12. Re-accommodate passengers."
    }))
    await asyncio.sleep(3)
    
    if inject_chaos:
        # CHAOS EVENT
        await manager.broadcast(append_to_ledger({
            "event": "chaos",
            "agent": "SYSTEM ANOMALY",
            "framework": "ChaosEngine",
            "role": "Disruption",
            "content": "SEVERE WEATHER ALERT: Ground Stop at ATL. All flights grounded. Part shipping delayed by 12 hours."
        }))
        await asyncio.sleep(3)
        
        await manager.broadcast(append_to_ledger({
            "agent": "Supply Chain Agent",
            "framework": "CrewAI",
            "role": "Logistics",
            "content": "Re-routing parts. Repair timeline aborted. Aircraft swap is now mandatory."
        }))
        await asyncio.sleep(2)

    # FAA Compliance
    await manager.broadcast(append_to_ledger({
        "agent": "FAA Compliance Agent",
        "framework": "Pydantic AI",
        "role": "Safety",
        "content": "Aircraft swap approved. Warning: Crew assigned to B787 is not type-rated for B777. You must recruit a B777 flight crew or face severe FAA penalty."
    }))
    await asyncio.sleep(3)
    
    # Crew Scheduler
    await manager.broadcast(append_to_ledger({
        "agent": "Crew Scheduler Agent",
        "framework": "LlamaIndex",
        "role": "Roster",
        "content": "Locating reserve B777 crew at JFK. Captain Miller and FO Davis are on standby. Assigning to Flight 902. Legal duty time is within limits."
    }))
    await asyncio.sleep(2)
    
    # Judge
    await manager.broadcast(append_to_ledger({
        "event": "resolution",
        "agent": "AOG Commander",
        "framework": "Band Core",
        "role": "Orchestrator",
        "content": "Resolution Achieved. Aircraft swapped to B777. Standby crew mobilized. Delay minimized from 4 hours to 45 minutes. Immutable ledger finalized."
    }))

class AOGRequest(BaseModel):
    inject_chaos: bool = False

@app.post("/api/trigger-aog")
async def trigger_aog(request: AOGRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_aog_swarm, request.inject_chaos)
    return {"status": "started"}
