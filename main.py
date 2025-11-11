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
from fastapi.responses import JSONResponse

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return JSONResponse(
        status_code=200,
        content={"message": "Preflight OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get('/')
async def home():
    return "this is home page"

@app.post('/username')
async def username(request : Request):
    data = await request.json()
    print("Received:", data)
    return {"username": data["username"]}
