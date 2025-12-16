import PyPDF2

class PDFTextExtractor:
     def __init__(self, pdf_path):
         self.pdf_path = pdf_path
         self.pages_text = {}

     def extract_text(self):
         with open(self.pdf_path, 'rb') as file:
             pdf_reader = PyPDF2.PdfReader(file)
             total_pages = len(pdf_reader.pages)
             
             print(f"총 {total_pages}페이지 추출 중...\n")
             
             for page_num in range(total_pages):
                 page = pdf_reader.pages[page_num]
                 text = page.extract_text()
                 self.pages_text[page_num + 1] = text.strip()
                 
                 print(f"--- {page_num + 1} 페이지 ---")
                 print(text.strip())
