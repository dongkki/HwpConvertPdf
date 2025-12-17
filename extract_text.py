import fitz  # PyMuPDF
import base64
import os

debug_dir = os.path.join(os.getcwd(), "debug_images")

class PDFTextExtractor:
    def __init__(self, file_name, pdf_path):
        self.file_name = file_name
        self.pdf_path = pdf_path
    
    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        total_pages_arr = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 페이지 내 모든 요소(텍스트, 이미지)의 위치 정보를 가져옵니다.
            # 'dict' 모드로 가져오면 블록 단위의 좌표와 내용을 알 수 있습니다.
            page_dict = page.get_text("dict")
            blocks = page_dict["blocks"]
                
            # 페이지 전체 폭 기준으로 좌우 블록을 나눕니다.
            page_width = page.rect.width
            middle_x = page_width / 2            
            left_blocks = [b for b in blocks if b["bbox"][0] < middle_x]
            right_blocks = [b for b in blocks if b["bbox"][0] >= middle_x]

            # 각 그룹 내에서만 위에서 아래로 정렬합니다.
            left_blocks.sort(key=lambda b: b["bbox"][1])
            right_blocks.sort(key=lambda b: b["bbox"][1])
            
            sorted_blocks = left_blocks + right_blocks
            page_content = "" # 현재 페이지의 순서대로 담길 데이터
        
            for block in sorted_blocks:
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
                    
                    # VLM에 보낼 이미지 데이터 생성
                    
                    ####### 디버깅 용 파일 저장 ########
                    debug_file_name = f"debug_image_page{page_num}_block{blocks.index(block)}.{xref}"
                    debug_file_path = os.path.join(debug_dir, debug_file_name)
                    with open(debug_file_path, 'wb') as img_file:
                        img_file.write(image_bytes)
                    ##################################
                    
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                    image_data_for_vlm = f"data:image/{xref};base64,{base64_image}"
                    
                    ### VLM 호출 부분 ###
                    # 여기에서 VLLM 함수를 호출하거나, 나중에 호출하기 위해 바이트 정보를 담습니다.
                    # 예시: vlm_response = call_vlm(image_data_for_vlm)
                    ####################
                    
                    page_content += "VLLM_IMAGE_DATA" + " "

            # 한 페이지의 처리가 끝나면 리스트를 합치거나 그대로 배열에 넣습니다.
            # 사용자님의 목적에 따라 "텍스트 + [추출될 텍스트] + 텍스트" 형태로 관리
            total_pages_arr.append(page_content)
            
        doc.close()
        
        for i in range(len(total_pages_arr)):
            print(f"[페이지 {i+1}] 내용 요약: {total_pages_arr[i][:100]}")
            
        return total_pages_arr