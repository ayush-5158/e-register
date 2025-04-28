from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from config.db import conn

router = APIRouter()

# Template
templates = Jinja2Templates(directory="templates")


class Announcement(BaseModel):
    title: str
    content: str


@router.post("/create_announcement")
async def create_announcement(request: Request, announcement: Announcement):
    # Insert announcement to the database
    announcement_data = {
        "title": announcement.title,
        "content": announcement.content,
        "created_at": datetime.now()
    }
    conn.notes.announcement.insert_one(announcement_data)

    # Redirect back to the dashboard after posting the announcement
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request, "message": "Announcement posted successfully!"})


@router.get("/create_announcement")
async def create_announcement_page(request: Request):
    return templates.TemplateResponse("create_announcement.html", {"request": request})
