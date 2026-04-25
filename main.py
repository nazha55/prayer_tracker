from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.prayers import router as prayer_router
from routes.routines import router as routine_router
from routes.partner import router as partner_router
from routes.history import router as history_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(history_router, prefix="/history", tags=["History"])

app.include_router(partner_router, prefix="/partner", tags=["Partner"])
app.include_router(routine_router,prefix="/routines", tags=["Routines"])
app.include_router(prayer_router, prefix="/prayers", tags=["Prayers"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)