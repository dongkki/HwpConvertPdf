import os
import subprocess
import extract_text as et

def convert_hwp_to_pdf_linux(hwp_path, pdf_path):
    try:
        result = subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', pdf_path,
            hwp_path
        ], check=True, capture_output=True, text=True, timeout=60)
        
        # 변환된 PDF 파일명 생성
        base_name = os.path.splitext(os.path.basename(hwp_path))[0]
        pdf_path = os.path.join(pdf_path, f"{base_name}.pdf")
        print(f"pdf_path : {pdf_path}")
        exists = os.path.exists(pdf_path)
        print(f"exists T/F : {exists}")
        if os.path.exists(pdf_path):
            return pdf_path
        else:
            print(f"⚠️ PDF 파일이 생성되지 않음: {pdf_path}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"❌ 변환 시간 초과: {hwp_path}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ 변환 오류: {e.stderr}")
        return None
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        return None

def main():
    HWP_DIR = '/app/hwp/'  # Linux 경로로 변경
    PDF_DIR = '/app/pdf/'  # Linux 경로로 변경
    pdf_files = []
    
    print("=" * 50)
    print("HWP -> PDF 변환 시작 (Phase 1/2)")
    print("=" * 50)

    # BASE_DIR이 존재하지 않으면 에러
    if not os.path.exists(HWP_DIR):
        print(f"❌ 디렉토리가 존재하지 않습니다: {HWP_DIR}")
        return

    for file_name in os.listdir(HWP_DIR):
        print(f"\n🔄 {file_name} 변환 시작...")
        
        # HWP/HWPX 파일만 처리
        if not (file_name.lower().endswith('.hwp') or file_name.lower().endswith('.hwpx')):
            print(f"❗ {file_name} 는 한글 파일이 아니므로 건너뜁니다.")
            continue
            
        hwp_path = os.path.join(HWP_DIR, file_name)
        
        # PDF 변환
        pdf_path = convert_hwp_to_pdf_linux(hwp_path, PDF_DIR)
        
        if pdf_path:
            print(f"✓ {file_name} -> PDF 변환 완료")
            pdf_files.append(pdf_path)
        else:
            print(f"❌  {file_name} 변환 실패")

    print("\n" + "=" * 50)
    print("PDF 텍스트 추출 시작 (Phase 2/2)")
    print("=" * 50)
    
    if not pdf_files:
        print("변환된 PDF 파일이 없어 추출 작업을 건너뜁니다.")
        return

    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        print(f"\n[추출 파일]: {file_name}")
        
        try:
            extractor = et.PDFTextExtractor(file_name, pdf_path)
            extractor.extract_text()
            
        except Exception as e:
            print(f"❌ 텍스트 추출 중 오류 발생: {file_name} - {str(e)}")

    print("\n✅ 모든 작업 완료!")


if __name__ == "__main__":
    main()