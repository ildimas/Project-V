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
from barrel import Barrel
from txt_converter import TXTconverter
from aspose_diff_algo import AsposeCompare
from docx_pretier import DocxPretier
from docx_pretier import DocxCompressor
from fastapi.responses import StreamingResponse
from shutil import move
from datetime import datetime
from dotenv import load_dotenv
from utils import *

load_dotenv()

app = FastAPI()
barrel = Barrel()
aspcompare = AsposeCompare()

BEFORE_DIRECTORY = "docs/before"
AFTER_DIRECTORY = "docs/after"
AFTER_TXT_DIRECTORY = "docs/after/txt"
BEFORE_TXT_DIRECTORY = "docs/before/txt"
AFTER_DOCX_DIRECTORY = "docs/after/docx"
BEFORE_DOCX_DIRECTORY = "docs/before/docx"
RESULTS_DIRECTORY = "docs/results"
COMP_RESULTS_DIRECTORY = "docs/results/compressed"

AFTER_FILENAME = ""
BEFORE_FILENAME = ""

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
async def upload_file(file: UploadFile = File(...), key: str = Form(...)):
    try:
        os.makedirs(AFTER_DIRECTORY, exist_ok=True)
        os.makedirs(BEFORE_DIRECTORY, exist_ok=True)
        os.makedirs(BEFORE_TXT_DIRECTORY, exist_ok=True)
        os.makedirs(AFTER_TXT_DIRECTORY, exist_ok=True)
        os.makedirs(BEFORE_DOCX_DIRECTORY, exist_ok=True)
        os.makedirs(AFTER_DOCX_DIRECTORY, exist_ok=True)
        if key == "b":
            file_path = os.path.join(BEFORE_DIRECTORY, file.filename)
            BEFORE_FILENAME = file.filename
        if key == "a":
            file_path = os.path.join(AFTER_DIRECTORY, file.filename)
            AFTER_FILENAME = file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        #! TXT conversion section
        if os.path.isfile(file_path):
            try:
                txt_path = "/".join(file_path.split(os.getenv('SLASH'))[:-1]) + "/txt" 
                print("txt path:", txt_path)
                file_name_no_type = file.filename.split(".")[0]
                try:
                    TXTconverter(barrel.ProcessChoser(filepath=file_path), txt_path, file_name_no_type)
                except Exception as e:
                    print(f"CRITICAL CONVERTATION ERROR {e}")
                    return JSONResponse(status_code=500, content={"error": "Convertation error"})
            except Exception as e:
                print(f"Error occurred while processing file: {e}")
        
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error uploading file", "detail": str(e)})

@app.post("/delete")
async def delete_file(filename: str = Form(...), key: str = Form(...)):
    try:
        if key == "b":
            file_paths = [f"{BEFORE_DIRECTORY}/txt/{file}" for file in os.listdir(f"{BEFORE_DIRECTORY}/txt")]
            file_paths.append(f"{BEFORE_DIRECTORY}/{filename}")
            for docx_file in os.listdir(BEFORE_DOCX_DIRECTORY):
                file_paths.append(os.path.join(BEFORE_DOCX_DIRECTORY, docx_file))
        if key == "a":
            file_paths = [f"{AFTER_DIRECTORY}/txt/{file}" for file in os.listdir(f"{AFTER_DIRECTORY}/txt")]
            file_paths.append(f"{AFTER_DIRECTORY}/{filename}")
            for docx_file in os.listdir(AFTER_DOCX_DIRECTORY):
                file_paths.append(os.path.join(AFTER_DOCX_DIRECTORY, docx_file))
            
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
    dirs = [BEFORE_DIRECTORY, AFTER_DIRECTORY, f"{AFTER_DIRECTORY}/txt" , f"{BEFORE_DIRECTORY}/txt", 
            f"{RESULTS_DIRECTORY}", f"{RESULTS_DIRECTORY}/compressed", AFTER_DOCX_DIRECTORY, BEFORE_DOCX_DIRECTORY]
    for dir in dirs:
        for entry in os.listdir(dir):
            full_path = os.path.join(dir, entry)
            if os.path.isfile(full_path):
                os.remove(full_path)
    print("All clear!")
    return JSONResponse(status_code=200, content={"Storage": "cleared !"})

@app.post("/process")
def process():
    os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
    os.makedirs(COMP_RESULTS_DIRECTORY, exist_ok=True)
    try:
        for entry in [entry for entry in os.listdir(COMP_RESULTS_DIRECTORY) if os.path.isfile(os.path.join(COMP_RESULTS_DIRECTORY, entry))]:
            os.remove(os.path.join(COMP_RESULTS_DIRECTORY, entry))
    except Exception as e:
        print("Error deleting compressed results", e)
        pass 
    if len([entry for entry in os.listdir(AFTER_DIRECTORY) if os.path.isfile(os.path.join(AFTER_DIRECTORY, entry))]) == 1 and  len([entry for entry in os.listdir(BEFORE_DIRECTORY) if os.path.isfile(os.path.join(BEFORE_DIRECTORY, entry))]) == 1:
        if len(before_list := os.listdir(BEFORE_DIRECTORY + "/txt")) != 0 and len(after_list := os.listdir(AFTER_DIRECTORY + "/txt")) != 0:
            try:
                files_before_list = []
                files_after_list = []
                # if comapre_file_fromats(get_file_with_type("docs/before"), get_file_with_type("docs/after")):
                #     try:
                #         save_each_page_as_docx(input_file=get_file_with_type("docs/before", fullpath=True), output_folder=BEFORE_DOCX_DIRECTORY)
                #         save_each_page_as_docx(input_file=get_file_with_type("docs/after", fullpath=True), output_folder=AFTER_DOCX_DIRECTORY)
                #         for i in range(1, len(os.listdir(BEFORE_DOCX_DIRECTORY)) + 1):
                #             files_before_list.append(f"{BEFORE_DOCX_DIRECTORY}/Page_{i}.docx")
                #         for i in range(1, len(os.listdir(AFTER_DOCX_DIRECTORY)) + 1):
                #             files_after_list.append(f"{AFTER_DOCX_DIRECTORY}/Page_{i}.docx")
                #     except Exception as e:
                #         print("error at docx conversion", e); return JSONResponse(status_code=500, content={"erorr" : str(e)})
                try:
                    for i in range(1, len(before_list) + 1):
                        files_before_list.append(f"{BEFORE_DIRECTORY}/txt/{before_list[0][:len(before_list[0])-5]}{i}.txt")
                    for i in range(1, len(after_list) + 1):
                        files_after_list.append(f"{AFTER_DIRECTORY}/txt/{after_list[0][:len(after_list[0])-5]}{i}.txt")    
                except Exception as e:
                    print("error at txt conversion", e); return JSONResponse(status_code=500, content={"erorr" : str(e)})
                counter = 1
                merged_list = list(zip(files_before_list, files_after_list))
                # print(merged_list)
                for before, after in merged_list:
                    # print(f"*before: {before}* \n #aftef: {after}#")
                    compared_filepath = aspcompare.process(before_file=before, after_file=after, output_dir=RESULTS_DIRECTORY, output_index=counter, output_format="docx")
                    DocxPretier(compared_filepath, compared_filepath)
                    counter += 1
                try:
                    res_list = []
                    for f in os.listdir(RESULTS_DIRECTORY):
                        if f.endswith(".docx"):
                            res_list.append(os.path.join(RESULTS_DIRECTORY, f))
                    res_list.sort()
                    print(res_list)
                    DocxCompressor(res_list, f"{COMP_RESULTS_DIRECTORY}/Обработанный файл от {datetime.now().strftime('%Y_%m_%d_%H-%M')}.docx")
                except Exception as e: return JSONResponse(status_code=501, content={"erorr" : "Docx Compression" + str(e)})
                
                for entry in res_list: os.remove(entry)
                print("comparing is sucsessfull !")
                return JSONResponse(status_code=200, content={"convertation" : "sucsess"})
            
            except Exception as e:
                print(f"Unhandled exception: {e}")
                return JSONResponse(status_code=503, content={"erorr" : str(e)})
        else:
            print("convertation chunk aren't found")
            return JSONResponse(status_code=501, content={"erorr" : "txt chunks"})
    else:
        print("Only one file provided !")
        return JSONResponse(status_code=504, content={"erorr" : "only one file provided"})
    
@app.get("/download")
async def download():
    if not os.path.isfile(source_file := F"{COMP_RESULTS_DIRECTORY}/{os.listdir(COMP_RESULTS_DIRECTORY)[0]}"):
        raise HTTPException(status_code=404, content={"erorr" : "Source file does not exist."})    
    try:
        return FileResponse(source_file, filename=os.listdir(COMP_RESULTS_DIRECTORY)[0], 
                         media_type='multipart/form-data')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # sys.stdout = open('fastAPI_logs.txt', 'w')
    uvicorn.run(app, host=os.getenv('HOST'), port=8000, workers=1)