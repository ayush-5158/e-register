from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from routes.note import note
from routes.auth import auth
from pymongo import MongoClient
from starlette.staticfiles import StaticFiles
import itsdangerous

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


from starlette.middleware.sessions import SessionMiddleware
from routes.note import note  # adjust this if your route is named differently
app.include_router(note)
app.include_router(auth)



# 🔐 Add Session Middleware (change the secret key to something secure in real app)
app.add_middleware(SessionMiddleware, secret_key="anything")


