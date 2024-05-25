# tests/test_main.py
from fastapi.testclient import TestClient
from main import app
import io
from functools import wraps
import os 

client = TestClient(app)
os.makedirs("tests/samples", exist_ok=True)

class ComapreDocumentsTest:
    def __init__(self, filepath1, filepath2):
        self.filepath1 = filepath1
        self.filepath2 = filepath2
    
    def filetype_chooser(self, filepath):
        self.almanac = {
            "docx" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pdf" : "application/pdf",
        }
        return self.almanac[filepath.split(".")[-1]]
        
    def main_process(self):
        with open(self.filepath1, "rb") as file:
            response = client.post(
                "/upload",
                files = {"file": (f"sample.{self.filepath1.split('.')[-1]}", file, self.filetype_chooser(self.filepath1))},
                data={"key": "b"}
            )
        with open(self.filepath2, "rb") as file:
            response = client.post(
                "/upload",
                files={"file": (f"sample.{self.filepath2.split('.')[-1]}", file, self.filetype_chooser(self.filepath2))},
                data={"key": "a"}
            )
        response = client.post("/process")
        return response
    
def clear_after_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        finally:
            client.post("/clear")
        return result
    return wrapper
    
def test_clear_endpoint():
    response = client.post("/clear")
    assert response.status_code == 200
    assert response.json() == {"Storage": "cleared !"}
        
@clear_after_test
def test_upload_clssic_docx_file():
    file_path = r"tests/samples/Classic case/Classic document.docx"
    with open(file_path, "rb") as file:
        response = client.post(
            "/upload",
            files={"file": (filename := "sample.docx", file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={"key": "b"}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "filename": filename}

@clear_after_test
def test_upload_classic_pdf_file():
    file_path = r"tests/samples/Classic case/Classic document.pdf"
    with open(file_path, "rb") as file:
        response = client.post(
            "/upload",
            files={"file": (filename := "sample.pdf", file, "application/pdf")},
            data={"key": "b"}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "filename": filename}

@clear_after_test    
def test_upload_table_docx_file():
    file_path = r"tests/samples/Table case/Table document.docx"
    with open(file_path, "rb") as file:
        response = client.post(
            "/upload",
            files={"file": (filename := "sample.docx", file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={"key": "b"}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "filename": filename}
    
@clear_after_test    
def test_upload_ocr_pdf_file():
    file_path = r"tests/samples/Ocr pdf case/Dificult document pair.pdf"
    with open(file_path, "rb") as file:
        response = client.post(
            "/upload",
            files={"file": (filename := "sample.pdf", file, "application/pdf")},
            data={"key": "b"}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "filename": filename}

@clear_after_test 
def test_compare_classic():
    comparer = ComapreDocumentsTest(r"tests/samples/Classic case/Classic document.docx", r"tests/samples/Classic case/Classic document.pdf")
    response = comparer.main_process()
    assert response.status_code == 200
    response.json() == {"convertation" : "sucsess"}

@clear_after_test 
def test_compare_classic():
    comparer = ComapreDocumentsTest(r"tests/samples/Table case/Table document.docx", r"tests/samples/Table case/Table document 2.docx")
    response = comparer.main_process()
    assert response.status_code == 200
    response.json() == {"convertation" : "sucsess"}
    
@clear_after_test 
def test_compare_ocr():
    comparer = ComapreDocumentsTest(r"tests/samples/Ocr pdf case/Dificult document pair.docx", r"tests/samples/Ocr pdf case/Dificult document pair.pdf")
    response = comparer.main_process()
    assert response.status_code == 200
    response.json() == {"convertation" : "sucsess"}


def test_delete_buton():
    file_path = r"tests/samples/Classic case/Classic document.pdf"
    with open(file_path, "rb") as file:
        client.post(
            "/upload",
            files={"file": (filename := "sample.pdf", file, "application/pdf")},
            data={"key": "b"}
        )
    response = client.post("/delete", data={"key": "b", "filename": filename })
    assert response.status_code == 200
    assert response.json() == {"message": "Files deleted successfully"}