import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

# Ensure the project root is in path for imports to work regardless of entry point
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.routes import auth, guests
from server.middleware.auth_middleware import auth_middleware

app = FastAPI(title="Bday Form API (Google Sheets)")

# ... (middleware stays same)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    return await auth_middleware(request, call_next)

# Include Routers (REMOVED /api prefix - Vercel handles this now)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(guests.router, prefix="/guests", tags=["Guests"])


@app.get("/")
async def root():
    return {"message": "Bday Form API (Sheets) is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
