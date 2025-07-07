# backend/app/main.py

from fastapi import FastAPI
from .config      import settings
from .api.routes  import router

app = FastAPI(debug=settings.DEBUG, title="My Secure Backend")

@app.get("/")   # ← this makes GET / work
def read_root():
    return {"msg": "Backend up & secure!"}

app.include_router(router)
