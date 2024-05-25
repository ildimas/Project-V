from PIL import Image
import pytesseract
import pdf2image
import sys
import os
from dotenv import load_dotenv
from text_processor import TextProcessor

text_proc = TextProcessor()

load_dotenv()
if os.getenv('CONTAINER') == 'False':
    tesseract_path = 'Tesseract-OCR/tesseract.exe'
    tessdata_dir = 'Tesseract-OCR/tessdata'
    print(os.path.isfile(tesseract_path), "tes_path_Exists ?")
    print(os.path.isdir(tessdata_dir), "tes_tessdata_Exists ?")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    tessdata_dir_config = f'--tessdata-dir "{tessdata_dir}"'

class ImageProcessor():
    def __init__(self) -> None:
        pass
    
    def extract_text_from_image(self, file_path):
        try:
            img = Image.open(file_path)
            ocr_result = pytesseract.image_to_string(img, lang='rus+eng')
            return ocr_result
        except Exception as e:
            print(f"Exception in module {__name__} error {e}")
            
    def pdf_to_img(self, pdf_file):
        return pdf2image.convert_from_path(pdf_file)
    
    def extract_text_from_pdf(self, file_path):
        try:
            res = text_proc.extract_text_from_pdf_with_fitz(file_path)
            print(type(res))
            if res == "":
                try:
                    print("ocr started")
                    res = ""
                    images = self.pdf_to_img(file_path)
                    for pg, img in enumerate(images):
                        ocr_result = pytesseract.image_to_string(img, lang='rus+eng')
                        res = res + ocr_result + "\n"
                    return res
                except Exception as e:
                    print(f"Exception in module {__name__} error at ocr pdf parcer {e}")
            return res
        except Exception as e:
                    print(f"Exception in module {__name__} error at fitz parcer {e}")
            
    
if __name__ == "__main__":
    x = ImageProcessor()
    print(x.extract_text_from_pdf(r"samples/Тяжелый договор 1.pdf"))