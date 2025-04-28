from pyexpat.errors import messages
from urllib import request
from fastapi import Form
from fastapi import APIRouter, FastAPI, Request, status,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from jinja2 import Template
from pip._internal.network import session
from starlette.responses import JSONResponse

from models.note import NoteUpdate,ResponseModel,Announcement
from models import user
from models.note import Note,Announcement
from config.db import conn
from schema.note import notesEntity, noteEntity

from datetime import datetime, timedelta

note = APIRouter()

templates = Jinja2Templates(directory="templates")

def get_current_user(request: Request):
    uid = request.cookies.get("uid")
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cookie",
        )
    return uid;


@note.get("/",response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})



@note.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})





@note.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Access the cookies sent with the request
    admin_login = False
    id = request.cookies.get("_id")
    uid = request.cookies.get("uid")
    user_data = conn.users.users.find_one({"uid": uid})
    name = request.cookies.get("name")

    if uid == "admin":
        admin_login = True
    latest_announcement = conn.notes.announcement.find().sort("created_at", -1).limit(1)
    announcement = None
    for ann in latest_announcement:
        announcement = ann

    response = templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_data,
        "announcement": announcement,
        "admin_login": admin_login,
    })
    return response
    # user_data = conn.users.users.find_one({"uid": uid})
    # return templates.TemplateResponse("dashboard.html", {"request": request, "user": user_data})






@note.get("/create_note", response_class=HTMLResponse)
async def read_index(request: Request):
    user_data = request.cookies.get("uid")
    u_data = conn.users.users.find_one({"uid": user_data})


    return templates.TemplateResponse("create_note.html", {"request": request , "data": user_data} )
    # docs = conn.notes.notes.find({})
    # newDocs=[]
    # for doc in docs:
    #     newDocs.append({
    #         "id":doc["_id"],
    #         "uid":doc.get("uid",""),
    #         "desc":doc["desc"],
    #     })
    # response = templates.TemplateResponse("create_note.html", {"request": request, "u_data": u_data})







@note.post("/create_note")
async def create_note(request: Request):
    session_uid = request.cookies.get("uid")  # Get the uid of the logged-in user
    session_name = request.cookies.get("name")

    form = await request.form()  # Get the form that was submitted
    # Check if the logged-in user is an admin
    if session_uid == "admin":
        uid = form.get("uid")  # Get the input UID
        form_dict = dict(form)  # Convert form data to dictionary

        # Check if the UID exists in the database
        docs = conn.users.users.find_one({"uid": uid})  # Find the user by UID
        if docs:  # If user exists
            note = conn.notes.notes.insert_one(form_dict)  # Insert the note into the database
            return templates.TemplateResponse(
                "success.html", {"request": request, "note": note}
            )
        else:  # If user doesn't exist
            return templates.TemplateResponse(
                "create_note.html", {
                    "request": request,
                    "error": "UID doesn't exist",
                    "status": "error",
                    "uid": session_uid, # Pass the uid of the logged-in user
                    "name":session_name
                }
            )
    else:
        # If the user is not an admin, show a warning
        return templates.TemplateResponse(
            "create_note.html", {
                "request": request,
                "message": "Unauthorized Access",
                "status": "error",
                "uid": session_uid,  # Pass the uid of the logged-in user
                "name": session_name

            }
        )










@note.get("/mynotes", response_class=HTMLResponse)
async def my_notes(request: Request):
    session_uid = request.cookies.get("uid")  # Get the UID of the logged-in user

    if not session_uid:
        return templates.TemplateResponse(
            "login.html", {"message": "Please log in to view your notes", "status": "error"}
        )

    # Fetch notes specific to the logged-in user from the database
    notes = conn.notes.notes.find({"uid": session_uid})  # Assuming notes have 'uid' field
    notes_list = list(notes)
    notes_sorted = sorted(notes_list, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=False)


    # Assuming you have a users collection where user data is stored
    user_data = conn.users.users.find_one({"uid": session_uid})

    # If user data exists, pass it along with the notes
    if user_data:
        return templates.TemplateResponse(
            "mynotes.html",
            {
                "request": request,
                "notes": notes_sorted,
                "data": user_data  # Pass the user data (e.g. uid, name)
            }
        )
    else:
        return templates.TemplateResponse(
            "login.html",
            {"message": "User data not found", "status": "error"}
        )




# @note.get("/mynotes", response_class=HTMLResponse)
# async def show_notes(request: Request):
#     # Get all notes directly from the notes collection
#     notes = list(conn.notes.notes.find({}))  # Get all notes without user lookup
#
#     # Convert ObjectId to string and simplify structure for Jinja2
#     for note in notes:
#         note["_id"] = str(note["_id"])  # Convert ObjectId to string
#         note["uid"] = note.get("uid", "")
#         note["desc"] = note.get("activity", "")
#         note["date"] = note.get("date", "")
#
#     # Return the notes to the template
#     print(notes)
#     return templates.TemplateResponse("mynotes.html", {"request": request, "notes": notes})
#
#
#     # docs = conn.notes.notes.find({"uid": request.session["user"]})
#     # notes_list = []
#     # for doc in docs:
#     #     notes_list.append({
#     #         "id": str(doc["_id"]),
#     #         "uid": doc.get("uid"),
#     #         "desc": doc.get("desc"),
#     #         "date": doc.get("date"),
#     #     })
#     # return templates.TemplateResponse("mynotes.html", {"request": request, "notes": notes_list})
#





@note.get("/all_notes", response_class=HTMLResponse)
async def all_notes(request: Request):
    session_name = request.cookies.get("name")
    session_uid = request.cookies.get("uid")

    if session_uid == "admin":
        notes_collection = conn.notes.notes.find({})
        # Fetch all notes from the database
        notes = list(notes_collection)

        # Sort notes by date in descending order (latest first)
        notes_sorted = sorted(notes, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=False)

        # Render the template with all notes

        return templates.TemplateResponse(
            "all_notes.html", {
                "request": request,
                "notes": notes_sorted,
                "uid": session_uid,  # Pass the uid of the logged-in user
                "name": session_name
            }
        )
    else:
        return templates.TemplateResponse(
        "all_notes.html", {
            "request": request,
            "error": "Unauthorized Access",
            "status": "error",
            "uid": session_uid,  # Pass the uid of the logged-in user
            "name": session_name
        }
    )

@note.post("/edit_note/{note_id}")
async def edit_note(note_id: str, note_data: dict):
        # Perform the database update logic here
        result = conn.notes.notes.update_one({"_id": ObjectId(note_id)}, {"$set": note_data})
        if result:
            return {"success": True}
        return {"success": False}



@note.delete("/delete_note/{note_id}", response_model=ResponseModel)
async def delete_note(note_id: str):
    # Ensure the note ID is a valid ObjectId
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")

    # Try to delete the note
    result = conn.notes.notes.delete_one({"_id": ObjectId(note_id)})

    if result.deleted_count == 1:
        return {"success": True, "message": "Note deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Note not found")


