---blank readme file---
command to build project in exe 

1. move to logic directory
2. create venviroment using python(3) -m venv <your venv name>
3. run pip(3) install -r requirements.txt
4. activate venb using <your venv name>\scripts\activate on widnows OR
                        source <your venv name>\bin\activate
5. make sure ypu have Tezeract-ocr installed  
6. use command pyinstaller --clean --noconsole --collect-data "docxcompose"  --add-binary "C:\Program Files\Tesseract-OCR\tesseract.exe;." --add-data "C:\Program Files\Tesseract-OCR\tessdata\*;tessdata" --onefile main.py