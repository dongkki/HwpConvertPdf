import PyPDF2

pdf_file_path = 'c:\\Python\\convert\\example\\한글문서5.pdf'
pages_text = {}
        
with open(pdf_file_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    
    print(f"총 {total_pages}페이지 추출 중...\n")
    
    for page_num in range(total_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        pages_text[page_num + 1] = text.strip()
        
        print(f"--- {page_num + 1} 페이지 ---")
        print(text.strip())