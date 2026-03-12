from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, guests
from middleware.auth_middleware import auth_middleware
from fastapi import Request

app = FastAPI(title="Bday Form API (Google Sheets)")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT Middleware
@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    return await auth_middleware(request, call_next)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(guests.router, prefix="/api/guests", tags=["Guests"])

@app.get("/")
async def root():
    return {"message": "Bday Form API (Sheets) is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
