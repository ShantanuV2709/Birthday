import os
import sys

# Add the project root to the path so 'server' can be found
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from server.main import app

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Vercel function is reachable"}

