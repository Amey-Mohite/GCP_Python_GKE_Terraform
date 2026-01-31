import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="gke-fastapi-prod", version="1.0.0")

def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

if not os.getenv("ENV") or not os.getenv("SECRET1"):
    _load_env_file(Path(".env"))
    
APP_ENV = os.getenv("ENV")
APP_SECRET1 = os.getenv("SECRET1")

@app.get("/")
def root():
    """
    Basic JSON response endpoint.
    Keep it simple; avoid leaking environment or secrets.
    """
    return {
        "service": "gke-fastapi-prod",
        "message": "hello from GKE",
        "env": APP_ENV
    }

@app.get("/healthz")
def healthz():
    """
    Liveness check:
    - should return 200 if process is alive.
    - do NOT check external dependencies here (DB, APIs).
    """
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    """
    Readiness check:
    - should return 200 only if pod is ready to receive traffic.
    - minimal checks: config present, optional secret mounted, etc.
    """
    if not APP_ENV or not APP_SECRET1:
        return JSONResponse(status_code=503, content={"status": "not-ready"})
    return {"status": "ready"}
