import os
import aspose.words as aw

def comapre_file_fromats(file1, file2):
    if file1.split(".")[-1] == file2.split(".")[-1] and (file1.split(".")[-1] in ["docx",]):
        return True
    else:
        return False
    
def get_file_with_type(path, fullpath=False):
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            if fullpath:
                return os.path.join(path, entry)
            return entry

# def save_each_page_as_docx(input_file: str, output_folder: str):
#     doc = aw.Document(input_file)
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     total_pages = doc.page_count
#     page_counter = 1
#     for i in range(0, total_pages, 2):
#         # Calculate the range for the two pages
#         end_page = min(i + 2, total_pages)  # Ensure we don't go out of bounds
#         extracted_pages = doc.extract_pages(i, end_page - i)
#         output_file = os.path.join(output_folder, f"Page_{page_counter}.docx")
#         page_counter += 1
#         extracted_pages.save(output_file)
#         DocxPretier(output_file, output_file) 

        
if __name__ == "__main__":
    input_file = r"samples/Договор поставки ХТС Рус- Подшипник Трейд ред. 18.04 от поставщика.docx"
    output_folder = "docs/"

    # Run the function
    # save_each_page_as_docx(input_file, output_folder)
