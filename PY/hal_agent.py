"""
HAL Local Agent
Provides a secure API layer between the local OpenQM environment and external tools.

Supports:
- File read/write under HAL root
- OpenQM command execution
- Health checks and structured logging
"""

import os
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body, Header
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel

# === Configuration ===
HAL_ROOT = os.getenv("HAL_ROOT", "C:\\QMSYS\\HAL")
QM_EXE = os.getenv("QM_EXE", "C:\\QMSYS\\bin\\qm.exe")
QM_ACCOUNT = os.getenv("QM_ACCOUNT", "HAL")
HAL_AUTH_TOKEN = os.getenv("HAL_AGENT_TOKEN", "CHANGEME-STRONG-TOKEN")

# Ensure directories exist
os.makedirs(HAL_ROOT, exist_ok=True)
os.makedirs(os.path.join(HAL_ROOT, "LOGS"), exist_ok=True)

app = FastAPI(title="HAL Local Agent", version="1.1")

# === Utility ===
def log_event(msg: str):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(os.path.join(HAL_ROOT, "LOGS", "hal_agent.log"), "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def auth_guard(x_auth: str):
    if x_auth != HAL_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# === Models ===
class QMCommand(BaseModel):
    cmd: str

class FileWrite(BaseModel):
    path: str
    content: str

# === Routes ===

@app.get("/health", response_class=PlainTextResponse)
def health(x_auth: str = Header(None)):
    if x_auth != HAL_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "ok"

@app.get("/list")
def list_dir(path: str = ".", x_auth: str = Header(None)):
    auth_guard(x_auth)
    full_path = os.path.join(HAL_ROOT, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"Path not found: {full_path}")
    entries = []
    for name in os.listdir(full_path):
        p = os.path.join(full_path, name)
        entries.append({"name": name, "is_dir": os.path.isdir(p), "size": os.path.getsize(p) if os.path.isfile(p) else 0})
    return {"type": "dir", "entries": entries}

@app.get("/file/read")
def read_file(path: str, x_auth: str = Header(None)):
    auth_guard(x_auth)
    full_path = os.path.join(HAL_ROOT, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    with open(full_path, "r", encoding="utf-8") as f:
        data = f.read()
    return {"path": path, "content": data}

@app.post("/file/write")
def write_file(req: FileWrite, x_auth: str = Header(None)):
    auth_guard(x_auth)
    full_path = os.path.join(HAL_ROOT, req.path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(req.content)
    log_event(f"WRITE {req.path} ({len(req.content)} bytes)")
    return {"written": req.path, "size": len(req.content)}

@app.post("/qm/run")
def qm_run(req: QMCommand, x_auth: str = Header(None)):
    auth_guard(x_auth)
    cmd = req.cmd.strip()
    log_event(f"QM RUN: {cmd}")

    if not os.path.exists(QM_EXE):
        raise HTTPException(status_code=500, detail=f"QM executable not found: {QM_EXE}")

    try:
        # Use shell=True to properly capture QM output
        # Build command string with proper quoting
        full_cmd = f'"{QM_EXE}" -account {QM_ACCOUNT} -command "{cmd}"'
        
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=30,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        out = {
            "cmd": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
        log_event(f"QM RESULT: {cmd} -> code {result.returncode}, output len: {len(result.stdout)}")
        return JSONResponse(content=out)
    except subprocess.TimeoutExpired:
        log_event(f"TIMEOUT: {cmd}")
        raise HTTPException(status_code=504, detail="QM command timed out")
    except Exception as e:
        log_event(f"ERROR: {cmd} -> {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qm/client")
def qm_client(req: QMCommand, x_auth: str = Header(None)):
    auth_guard(x_auth)
    cmd = req.cmd.strip()
    log_event(f"QM CLIENT: {cmd}")
    
    try:
        # Import QMClient Python module
        import sys
        sys.path.insert(0, "C:\\QMSYS\\bin")
        import qmclient as qm
        
        # Connect to QM
        session = qm.Connect('localhost', 4243, 'HAL', '', '')
        if not session:
            raise Exception("Failed to connect to QM")
        
        # Execute command
        qm.Execute(cmd)
        
        # Collect output
        output_lines = []
        while True:
            line = qm.ReadLine()
            if not line:
                break
            output_lines.append(line)
        
        # Disconnect
        qm.Disconnect()
        
        output = '\n'.join(output_lines)
        log_event(f"QM CLIENT RESULT: {cmd} -> {len(output)} bytes")
        
        return JSONResponse(content={
            "cmd": cmd,
            "returncode": 0,
            "stdout": output,
            "stderr": ""
        })
        
    except Exception as e:
        log_event(f"QM CLIENT ERROR: {cmd} -> {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    log_event("Starting HAL Agent on port 8766")
    uvicorn.run(app, host="127.0.0.1", port=8766, log_level="info")
