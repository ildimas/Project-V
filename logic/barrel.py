from text_processor import TextProcessor
from image_processor import ImageProcessor

import os
class Barrel():
    def __init__(self):
        self.image_proc = ImageProcessor()
        self.text_proc = TextProcessor()
        self.file_handlers = {
            '.txt': self.handle_txt,
            '.pdf': self.handle_pdf,
            '.docx': self.handle_docx,
            '.img': self.handle_img,
            '.png': self.handle_png,
            '.jpg': self.handle_jpg,
        }
    def handle_txt(self, file_path):
        print(f"Processing TXT file: {file_path}")
        return self.text_proc.extract_text_from_txt(file_path)

    def handle_pdf(self, file_path):
        print(f"Processing PDF file: {file_path}")
        return self.image_proc.extract_text_from_pdf(file_path)
    
    def handle_docx(self, file_path):
        print(f"Processing Docx file: {file_path}")
        return  self.text_proc.extract_text_from_docx(file_path)
        
    def handle_jpg(self, file_path):
        print(f"Processing jpg file: {file_path}")
        return self.image_proc.extract_text_from_image(file_path)
        
    def handle_img(self, file_path):
        print(f"Processing img file: {file_path}")
        return self.image_proc.extract_text_from_image(file_path)

    def handle_png(self, file_path):
        print(f"Processing png file: {file_path}")
        return self.image_proc.extract_text_from_image(file_path)
        
    def ProcessChoser(self, filepath):
        _, file_extension = os.path.splitext(filepath)
        handler_method = self.file_handlers[file_extension]
        return handler_method(filepath)
        
if __name__ == "__main__":
    file_processor = Barrel()
    file_paths = ["samples/example.docx"]
    for file_path in file_paths:
        print(file_processor.ProcessChoser(file_path))