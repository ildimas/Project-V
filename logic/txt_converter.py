import os

class TXTconverter:
    def __init__(self, text, path_to_directory, filename_no_format):
        self.text = text
        self.path_to_directory = path_to_directory
        self.filename_no_format = filename_no_format
        self.max_capacity = 5000  
        self.create_txt_files()

    def create_txt_files(self):
        text_length = len(self.text)
        file_counter = 1
        os.makedirs(os.path.dirname(self.path_to_directory), exist_ok=True)

        for start_idx in range(0, text_length, self.max_capacity):
            chunk = self.text[start_idx:start_idx+self.max_capacity]
            filename = f"{self.filename_no_format}_{file_counter}.txt"
            file_path = os.path.join(self.path_to_directory, filename)
            try:
                with open(file_path, 'w', encoding="UTF-8") as file:
                    file.write(chunk)
                print(f"Text successfully saved to '{file_path}'")
            except Exception as e:
                print(f"Error occurred while saving file: {e}")
                return e
            file_counter += 1

if __name__ == "__main__":
    text = "Your very long text goes here"  
    path_to_directory = "docs/after/txt/"  
    filename_no_format = "test"
    TXTconverter(text, path_to_directory, filename_no_format)
