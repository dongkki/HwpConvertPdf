import fitz  # PyMuPDF

class PDFTextExtractor:
    def __init__(self, file_name, pdf_path):
        self.file_name = file_name
        self.pdf_path = pdf_path
    
    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        total_pages_arr = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 1. 페이지 내 모든 요소(텍스트, 이미지)의 위치 정보를 가져옵니다.
            # 'dict' 모드로 가져오면 블록 단위의 좌표와 내용을 알 수 있습니다.
            page_dict = page.get_text("dict")
            blocks = page_dict["blocks"]
                
            # 좌표(y0: 위쪽 좌표, x0: 왼쪽 좌표) 순서대로 블록을 정렬합니다.
            # 문서의 상단부터 하단 순으로 데이터를 읽기 위함입니다.
            blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))
            page_content = "" # 현재 페이지의 순서대로 담길 데이터
        
            #open(f'debug_blocks{page_num}.txt','w',encoding='utf-8').write(str(blocks))
            for block in blocks:
                if block["type"] == 0:  # 텍스트 블록
                    text_parts = []
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_parts.append(span["text"])
                    
                    full_text = " ".join(text_parts).strip()
                    if full_text:
                        page_content += full_text + " "
                
                elif block["type"] == 1:  # 이미지 블록
                    # 이미지 정보 추출 (VLLM으로 보낼 이미지 데이터)
                    xref = block["ext"] # 이미지 확장자 정보 등
                    image_bytes = block["image"]
                    
                    # 여기에서 VLLM 함수를 호출하거나, 나중에 호출하기 위해 바이트 정보를 담습니다.
                    page_content += "VLLM_IMAGE_DATA" + " "

            # 한 페이지의 처리가 끝나면 리스트를 합치거나 그대로 배열에 넣습니다.
            # 사용자님의 목적에 따라 "텍스트 + [추출될 텍스트] + 텍스트" 형태로 관리
            total_pages_arr.append(page_content)
            
        doc.close()
        
        for i in range(len(total_pages_arr)):
            print(f"[페이지 {i+1}] 내용 요약: {total_pages_arr[i][:100]}")
            
        return total_pages_arr