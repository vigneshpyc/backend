from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["https://691339eac998732538914279--silly-rolypoly-675773.netlify.app"],
    allow_origins=["*"],
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in the request
)

@app.get('/')
async def home():
    return "this is home page"

@app.post('/username')
async def username(request : Request):
    data = await request.json()
    print("Received:", data)
    return {"username": data["username"]}
