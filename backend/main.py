from fastapi import FastAPI
from typing import List 
from api.routes import auth, users, logs, alerts

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
