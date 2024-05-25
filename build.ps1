# Navigate to the 'logic' directory
Set-Location -Path ".\logic"

# --clean --noconsole
# pyinstaller --collect-data "docxcompose" --onefile --paths="C:\Users\spoyi\OneDrive\Рабочий стол\pod trade stuff\Compare mechanism\File_compare_exe\logic\envi\Lib\site-packages" --add-data="Tesseract-OCR;./logic/Tesseract-OCR" main.py
pyinstaller --collect-data "docxcompose" --clean --noconsole main.py


#copy tesseract-ocr to dist folder
Copy-Item -Path ".\Tesseract-OCR" -Destination ".\dist\Tesseract-OCR" -Recurse



# Navigate to the 'interface' directory
Set-Location -Path "..\interface"

# build the Node.js application
npm run build