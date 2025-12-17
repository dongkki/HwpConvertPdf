import fitz  # PyMuPDF

def extract_page_elements(pdf_path):
    doc = fitz.open(pdf_path)
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
        
        page_content = [] # 현재 페이지의 순서대로 담길 데이터

        for block in blocks:
            if block["type"] == 0:  # 텍스트 블록
                text_parts = []
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_parts.append(span["text"])
                
                full_text = " ".join(text_parts).strip()
                if full_text:
                    page_content.append({"type": "text", "content": full_text})
            
            elif block["type"] == 1:  # 이미지 블록
                # 이미지 정보 추출 (VLLM으로 보낼 이미지 데이터)
                xref = block["ext"] # 이미지 확장자 정보 등
                image_bytes = block["image"]
                
                # 여기에서 VLLM 함수를 호출하거나, 나중에 호출하기 위해 바이트 정보를 담습니다.
                page_content.append({"type": "image", "content": image_bytes})

        # 한 페이지의 처리가 끝나면 리스트를 합치거나 그대로 배열에 넣습니다.
        # 사용자님의 목적에 따라 "텍스트 + [추출될 텍스트] + 텍스트" 형태로 관리
        total_pages_arr.append(page_content)

    return total_pages_arr

# 실행
pdf_file = 'c:\\Python\\convert\\example\\hwp\\한글문서5.pdf'
structured_data = extract_page_elements(pdf_file)

# 결과 확인 (예시: 1페이지 요소 순회)
print(f"총 페이지 수: {len(structured_data)}")
for i, element in enumerate(structured_data[0]): # 첫 페이지 확인
    print(f"[{i}] 타입: {element['type']}, 데이터 요약: {str(element['content'])[:30]}...")