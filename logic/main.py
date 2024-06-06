from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import fastapi
import shutil
import os
import signal
import multiprocessing
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sys
from fastapi.responses import StreamingResponse
from shutil import move
from datetime import datetime
from dotenv import load_dotenv
from utils import *
from tarjans_algo import TarjanSCC
from CSV_module import CSVreader

load_dotenv()

app = FastAPI()

DOCS_DIR = "docs/"
RES_DIR = "res/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return JSONResponse(status_code=200, content={"everything": "is ok"})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(DOCS_DIR, exist_ok=True)
        file_path = os.path.join(DOCS_DIR, file.filename)
        FILENAME = file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename})
    except Exception as e:
        print(f"Error in upload function {e}")
        return JSONResponse(status_code=500, content={"message": "Error uploading file", "detail": str(e)})

@app.post("/delete")
async def delete_file(filename: str = Form(...)):
    try:
        file_paths = [f"{DOCS_DIR}/{file}" for file in os.listdir(f"{DOCS_DIR}")]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                return JSONResponse(status_code=404, content={"message": "File not found", "filename": file_path.split("/")[-1]})
            
        return JSONResponse(status_code=200, content={"message": "Files deleted successfully"})
        
    except Exception as e:
        print(f"exception in delete endpoint: {e}")
        return JSONResponse(status_code=500, content={"message": "Error deleting files", "detail": str(e)})
    

    
# @app.post("/shutdown")
# def shutdown():
#     print("Goodbye...")
#     os.kill(os.getpid(), signal.SIGINT)
#     return {"message": "Server is shutting down..."}

@app.post("/clear")
def clear():
    dirs = [DOCS_DIR, RES_DIR]
    for dir in dirs:
        for entry in os.listdir(dir):
            full_path = os.path.join(dir, entry)
            if os.path.isfile(full_path):
                os.remove(full_path)
    print("All clear!")
    return JSONResponse(status_code=200, content={"Storage": "cleared !"})

@app.post("/process")
def process():
    os.makedirs(RES_DIR, exist_ok=True)
    print(os.listdir(DOCS_DIR))
    csv_reader = CSVreader(os.path.join(DOCS_DIR, os.listdir(DOCS_DIR)[0]))
    graph = csv_reader.create_adjacency_list()
    
    max_node = max(max(csv_reader.df['source']), max(csv_reader.df['target']))
    graph = {i: graph.get(i, []) for i in range(max_node + 1)}

    tarjan = TarjanSCC(graph)
    tarjan.get_sccs()
    
    
@app.get("/download")
async def download():
    if not os.path.isfile(source_file := F"{RES_DIR}/{os.listdir(RES_DIR)[0]}"):
        raise HTTPException(status_code=404, content={"erorr" : "Source file does not exist."})    
    try:
        return FileResponse(source_file, filename=os.listdir(RES_DIR)[0], 
                         media_type='multipart/form-data')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # sys.stdout = open('fastAPI_logs.txt', 'w')
    uvicorn.run(app, host=os.getenv('HOST'), port=8000, workers=1)