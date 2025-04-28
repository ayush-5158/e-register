from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import JSONResponse

from config.db import conn
from fastapi import HTTPException

from fastapi import FastAPI, Request, Depends

from starlette.middleware.sessions import SessionMiddleware

from fastapi.responses import RedirectResponse

from models.note import ChangePasswordRequest
from bson import ObjectId

auth = APIRouter()
templates = Jinja2Templates(directory="templates")



async def get_current_user_id(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@auth.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@auth.post("/signup")
async def signup(request: Request):
    form = await request.form() # form ka data recieve kiya
    uid = form.get("uid") # uid nikala
    name = form.get("name") # name nikala
    email = form.get("email") # email nikala
    password = form.get("password") # password nikala

    print("UID:", uid)
    existing_user = conn.users.users.find_one({"uid": uid})

    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "User already exists!", "uid": uid})

    conn.users.users.insert_one({"uid": uid ,"name": name ,"email": email ,"password": password,})
    print("User data :" , form)

    return templates.TemplateResponse("signup.html", {"request": request,"success": "User Created Successfully! ","uid": uid})


@auth.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@auth.post("/login")
async def login(request: Request):
    form = await request.form()
    uid = form["uid"]
    password = form["password"]
    user = conn.users.users.find_one({"uid": uid})
    name = user["name"]


    if user:
        if password == user["password"]:
            response = RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie(key="id", value=user["_id"])
            response.set_cookie(key="name", value=user["name"])
            response.set_cookie(key="uid", value=user["uid"])
            request.session["user_id"] = str(user["_id"])
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials!" ,"msg":"Please enter correct password!", "name": name})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "User Doesn't Exist!"})




@auth.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("id")
    response.delete_cookie("uid")  # Delete the uid cookie
    response.delete_cookie("name")  # Delete the username cookie
    return response


@auth.get("/change_password")
async def change_password(request: Request):
    return templates.TemplateResponse("change_password.html", {"request": request})


@auth.post("/change_password")
async def change_password(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    user_id = request.cookies.get("uid")
    # Fetch the user
    user = conn.users.users.find_one({"uid": user_id})

    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # Check if old password matches
    if user["password"] != old_password:
        # Password incorrect
        return RedirectResponse(url="/change_password?error=Incorrect%20Password", status_code=status.HTTP_302_FOUND)

    # Update password
    conn.users.users.update_one({"uid": user_id}, {"$set": {"password": new_password}})
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)