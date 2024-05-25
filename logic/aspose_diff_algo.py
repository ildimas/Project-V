import aspose.words as aw
from datetime import datetime


#output formats: docx, pdf, txt
class AsposeCompare:
    def __init__(self):
        pass
    def process(self, before_file, after_file, output_dir, output_index, output_format):
        try:
            self.before_file = before_file
            self.after_file = after_file
            self.output_dir = output_dir
            self.output_index = output_index
            self.output_format = output_format
            #!---
            docA = aw.Document(self.before_file)
            docB = aw.Document(self.after_file)
            docA.accept_all_revisions()
            docB.accept_all_revisions()
            docA.compare(docB, "Мастер сравнения", datetime.now())
            docA.save(f"{self.output_dir}/Output_{self.output_index}.{self.output_format}")
            return f"{self.output_dir}/Output_{self.output_index}.{self.output_format}"
        except Exception as e:
            print(f"Exception in module {__name__}")
            
if __name__ == "__main__":
    x = AsposeCompare()
    x.process("samples\Договор поставки ХТС Рус- Подшипник Трейд ред. 18.04 от поставщика.docx", "samples\Договор поставки ХТС Рус- Подшипник Трейд, финал.docx",
             "docs\\results", 1, "docx" )