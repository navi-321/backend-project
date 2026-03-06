from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()

# Supabase connection
SUPABASE_URL = "https://dpuvdnkvyobxbvgedkvq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRwdXZkbmt2eW9ieGJ2Z2Vka3ZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3NjIzNTEsImV4cCI6MjA4ODMzODM1MX0.B0K_FYHD8RqnNnJMYa3KURsyRL-nbXuwl5kTCyx7OMU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------
# Models
# -------------------------

class User(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


# -------------------------
# Home API
# -------------------------

@app.get("/")
def home():
    return {"message": "Backend Working"}


# -------------------------
# Register API
# -------------------------

@app.post("/register")
def register(user: User):

    data = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

    try:
        response = supabase.table("user").insert(data).execute()
        return {
            "message": "User registered successfully",
            "data": response.data
        }
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# Login API
# -------------------------

@app.post("/login")
def login(data: Login):

    try:
        response = supabase.table("user") \
            .select("*") \
            .eq("email", data.email) \
            .eq("password", data.password) \
            .execute()

        if response.data:
            return {"message": "Login Successful"}
        else:
            return {"message": "Invalid credentials"}

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# Profile Upload API
# -------------------------

@app.post("/upload-profile")
def upload_profile(file: UploadFile = File(...)):
    return {"filename": file.filename}