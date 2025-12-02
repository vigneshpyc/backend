from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
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
#API for Time table data insertion
@app.post("/TT_Data")
async def timeTableData(request:Request):
    if request.method == "POST":
        try:
            data = await request.json()
            client = MongoClient("mongodb://127.0.0.1:27017/")
            db = client['TTcheck']
            collection = db['TTData']
            
        except Exception as e:
            return JSONResponse({"status":"error",
                                 "message":"mogodb Db was not connected"
                                 })
        try:
            collection.insert_one({"data":data})
            return JSONResponse({"status":"success",
                                 "message":"Data Inserted Successfully"
                                 })
        except Exception as e:
            return {"Something went wrong",e}
    else:
        return "Method not Allowed"

#API for insert class data (eg:year, section)
@app.post('/class_data')
async def class_data(request:Request):
    if request.method == "POST":
        try:
            data = await request.json()
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client['TTcheck']
            collection = db['Class_datas']
           
        except Exception as e:
            return JSONResponse({"status":"error",
                                 "message":"Database was not Connected"
                                 })
        #Inert a Data into DB
        try:
            print("insertion Started")
            collection.insert_one(data)
            print("insertion completed")
            
            return JSONResponse({"status":"success",
                                 "message":"Data Inserted Successfully"
                                 })
        except Exception as e:
            return {"Something went wrong",e}
    else:
        return "Method not Allowed"

#API for get the class_data from db
@app.post("/get_class_data")
async def get_class_data(request:Request):
    if request.method == "POST":
        try:
            data = await request.json()
            year = data.get("year")
            section = data.get("section")

            #connection DB
            client = MongoClient("mongodb://127.0.0.1:27017/")
            db = client['TTcheck']
            collection = db['Class_datas']

            #data fetching
            datas = collection.find_one({"year":year,"section":section})
            if not datas:
                return JSONResponse({"status":"error",
                                     "message":"Invalid Credentials"
                                     })
            datas["_id"] = str(datas["_id"])
            return datas
        except Exception as e:
            return "Unable to retrieve a data"
    else:
        return JSONResponse({"status":"error",
                             "message":"Method not allowed"})