# Render's Start Command is `uvicorn main:app --host 0.0.0.0 --port $PORT`,
# which expects a top-level `main` module. The real FastAPI app lives in
# roxroom/token_server.py -- this just re-exports it under the name Render
# looks for, matching the requirements.txt shim above.
from roxroom.token_server import app

__all__ = ["app"]
